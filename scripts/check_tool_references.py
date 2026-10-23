"""Reject retired creation-tool names in the plugin's public text surfaces.

Standard library only. This is a static regression guard, not schema validation
or evidence that a connected client can execute the workflow.
"""

import argparse
from pathlib import Path
import re


RETIRED_TOOLS = {
    "create_text_document": "generate_study_guide",
    "create_document": "generate_study_guide",
    "generate_study_document": "open_study_guide_generator",
}
# Allow host namespace prefixes ending in underscores, but not longer names.
RETIRED_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(RETIRED_TOOLS) + r")(?![A-Za-z0-9_])"
)
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".html", ".svg"}
PUBLIC_DIRECTORIES = (
    "skills", "assets", "examples", "docs", ".codex-plugin", ".claude-plugin"
)
ROOT = Path(__file__).resolve().parents[1]


def public_files(root):
    """Include hidden manifests, nested references, and future public examples.

    Test fixtures and this denylist are intentionally outside these surfaces.
    Extend this inventory if the package gains another content directory/format.
    """
    files = {p for p in root.iterdir() if p.is_file()}
    for directory in PUBLIC_DIRECTORIES:
        path = root / directory
        if path.is_dir():
            files.update(p for p in path.rglob("*") if p.is_file())
    return sorted(p for p in files if p.suffix.lower() in TEXT_SUFFIXES)


def check(root):
    files = public_files(root)
    errors = []
    if not (root / "plugin.json").is_file() or not list(root.glob("skills/*/SKILL.md")):
        errors.append("Expected plugin.json and skills/*/SKILL.md; refusing an empty audit")
    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            errors.append(f"{path.relative_to(root)}: cannot read public text: {error}")
            continue
        for number, line in enumerate(content.splitlines(), 1):
            for match in RETIRED_PATTERN.finditer(line):
                name = match.group(1)
                errors.append(
                    f"{path.relative_to(root)}:{number}: retired {name}; "
                    f"use {RETIRED_TOOLS[name]}"
                )
    return files, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Plugin directory to audit")
    args = parser.parse_args()
    files, errors = check(args.root.resolve())
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: no retired creation-tool references in {len(files)} public text files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
