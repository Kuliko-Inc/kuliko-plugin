"""Validate package metadata and pinned exercise tool signatures, without live writes.

--connect-repo compares the snapshot with fetched origin/main source via AST.
This is static contract evidence, not server availability or host rendering proof.
Requires PyYAML (also used by CI).
"""
import argparse
import ast
import json
from pathlib import Path
import re
import subprocess

import yaml

try:
    from scripts.check_tool_references import public_files, ROOT
except ModuleNotFoundError:
    from check_tool_references import public_files, ROOT

FIXTURE = ROOT / "tests/fixtures/exercise-tools.json"
SOURCES = ("app/mcp/tools/exercises.py", "app/mcp/apps/exercise_widget.py")
CONSTRAINT_SOURCES = {
    "app/mcp/tools/exercises.py": {
        "SourceSelection", "Objective", "Nonblank", "Version", "DraftVersion",
        "Limit", "Offset", "_sources", "_objective", "_nonblank",
    },
    "app/mcp/exercise_types.py": {
        "ExerciseMode", "ExerciseDifficulty", "RevealKind", "AssessmentState",
        "CriterionStatus", "ExerciseEvidenceLinkState",
    },
    "app/mcp/tool_types.py": {"LearningResourceLanguage"},
}
TOOL_PATTERN = re.compile(r"(?<![a-zA-Z0-9])(?:mcp__[a-zA-Z0-9_]+__)?([a-z]+_exercise(?:s|_[a-z_]+)?)(?![a-zA-Z0-9_.])")


def source_contract(repo, ref="origin/main"):
    """Read remote-tracking source; do not import code or alter its working tree."""
    tools = {}
    for path in SOURCES:
        source = subprocess.check_output(
            ["git", "-C", str(repo), "show", f"{ref}:{path}"], text=True
        )
        for node in ast.parse(source).body:
            if not isinstance(node, ast.AsyncFunctionDef):
                continue
            if path.endswith("exercise_widget.py") and node.name != "open_exercise":
                continue
            if not node.decorator_list:
                continue
            args = node.args.args
            required = len(args) - len(node.args.defaults)
            tools[node.name] = {
                "required": [arg.arg for arg in args[:required]],
                "optional": [arg.arg for arg in args[required:]],
                "annotations": {arg.arg: ast.unparse(arg.annotation) for arg in args},
            }
    return tools


def source_constraints(repo, ref="origin/main"):
    """Capture aliases and validators behind signature annotations, without imports."""
    constraints = {}
    for path, names in CONSTRAINT_SOURCES.items():
        source = subprocess.check_output(
            ["git", "-C", str(repo), "show", f"{ref}:{path}"], text=True
        )
        found = {}
        for node in ast.parse(source).body:
            if isinstance(node, ast.FunctionDef):
                name = node.name
            elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                name = node.target.id
            else:
                continue
            if name in names:
                found[name] = ast.unparse(node)
        # Missing aliases/validators must remain detectable as source drift.
        constraints[path] = found
    return constraints


def check_links(root):
    errors = []
    for path in (root / "skills").rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            linked = (path.parent / target.split("#", 1)[0]).resolve()
            if not linked.is_relative_to(root.resolve()) or not linked.exists():
                errors.append(f"{path.relative_to(root)}: broken/outside reference {target}")
    return errors


def check_metadata(root):
    errors = []
    try:
        manifests = [json.loads((root / p).read_text()) for p in (
            "plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"
        )]
        portable, codex, _ = manifests
        if portable.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
            errors.append("plugin.json: invalid portable schema")
        for key in ("name", "version", "description"):
            values = [m.get(key) for m in manifests]
            if not all(isinstance(v, str) and v.strip() for v in values) or len(set(values)) != 1:
                errors.append(f"manifests: inconsistent or missing {key}")
        ui = portable["extensions"]["com.openai"]["interface"]
        if ui != codex["interface"]:
            errors.append("manifests: inconsistent OpenAI interface")
        if len(ui["shortDescription"]) > 30:
            errors.append("manifest shortDescription exceeds 30 characters")
        portable_mcp = json.loads((root / "mcp.json").read_text())
        legacy_mcp = json.loads((root / ".mcp.json").read_text())
        if portable_mcp.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json":
            errors.append("mcp.json: invalid portable schema")
        for name, server in portable_mcp["mcpServers"].items():
            if server["url"] != legacy_mcp["mcpServers"][name]["url"]:
                errors.append(f"MCP endpoint mismatch: {name}")
        names = set()
        skills = list(root.glob("skills/*/SKILL.md"))
        if not skills:
            errors.append("No packaged skills")
        for path in skills:
            text = path.read_text()
            parts = text.split("---", 2)
            if len(parts) != 3 or parts[0].strip():
                errors.append(f"{path.relative_to(root)}: missing YAML frontmatter")
                continue
            data = yaml.safe_load(parts[1])
            if not isinstance(data, dict) or data.get("name") != path.parent.name:
                errors.append(f"{path.relative_to(root)}: skill name does not match directory")
                continue
            if data["name"] in names:
                errors.append("Duplicate skill name")
            names.add(data["name"])
            if not isinstance(data.get("description"), str) or not data["description"].strip():
                errors.append(f"{path.relative_to(root)}: missing description")
            metadata = path.parent / "agents/openai.yaml"
            if metadata.exists():
                agent = yaml.safe_load(metadata.read_text())
                for key in ("display_name", "short_description"):
                    value = agent.get("interface", {}).get(key)
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"{metadata.relative_to(root)}: missing {key}")
                prompt = agent.get("interface", {}).get("default_prompt")
                if prompt is not None and (not isinstance(prompt, str) or not prompt.strip()):
                    errors.append(f"{metadata.relative_to(root)}: invalid default_prompt")
    except (OSError, ValueError, KeyError, TypeError, AttributeError, yaml.YAMLError) as error:
        errors.append(f"Invalid package metadata: {error}")
    return errors


def check(root, connect_repo=None):
    errors = check_metadata(root) + check_links(root)
    snapshot = json.loads(FIXTURE.read_text())
    tools = snapshot["tools"]
    for path in public_files(root):
        text = path.read_text()
        # Inline-code tool references only: prose/data keys aren't tool calls.
        for code in re.findall(r"`([^`\n]+)`", text):
            for match in TOOL_PATTERN.finditer(code):
                if match.group(1) not in tools:
                    errors.append(f"{path.relative_to(root)}: unknown exercise tool {match.group(1)}")
    reference = root / "skills/create-learning-resources/references/exercises.md"
    if not reference.exists():
        errors.append("Missing exercise workflow reference")
    else:
        rows = {}
        for line in reference.read_text().splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) != 3:
                continue
            name = cells[0].strip("`")
            if name in tools:
                rows[name] = {
                    "required": re.findall(r"`([a-z_]+)`", cells[1]),
                    "optional": re.findall(r"`([a-z_]+)`", cells[2]),
                }
        for name, spec in tools.items():
            if name not in rows:
                errors.append(f"Exercise tool table missing {name}")
                continue
            for key in ("required", "optional"):
                if set(rows[name][key]) != set(spec[key]):
                    errors.append(f"Exercise tool table: {name} incorrect {key} inputs")
    if connect_repo:
        actual = source_contract(connect_repo)
        if actual != tools:
            errors.append("Connect origin/main tool signatures differ from pinned contract")
        elif source_constraints(connect_repo) != snapshot["constraints"]:
            errors.append("Connect origin/main enums or validators differ from pinned contract")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--connect-repo", type=Path)
    args = parser.parse_args()
    errors = check(args.root, args.connect_repo)
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: package metadata, exercise tool references and input table" +
          ("; Connect origin/main signatures, enums and validators match" if args.connect_repo else " (pinned source contract)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
