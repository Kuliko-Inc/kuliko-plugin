import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts.check_exercise_contract import check, check_metadata, source_contract, source_constraints, ROOT, FIXTURE


class ExerciseContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "package"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def test_current_package(self):
        self.assertEqual(check(self.root), [])

    def test_unknown_tool_with_host_prefix_is_rejected(self):
        path = self.root / "skills/teach-it-back/SKILL.md"
        path.write_text(path.read_text() + "\nUse `mcp__kuliko__grade_exercise_answer`.\n")
        self.assertTrue(any("unknown exercise tool grade_exercise_answer" in e for e in check(self.root)))

    def test_ordinary_exercise_fields_are_not_tool_references(self):
        path = self.root / "README.md"
        path.write_text(path.read_text() + "\n`exercise_id` and `exercise_ids` are IDs; `tests/test_exercises.py` is a file.\n")
        self.assertEqual(check(self.root), [])

    def test_generation_table_rejects_singular_source(self):
        path = self.root / "skills/create-learning-resources/references/exercises.md"
        lines = path.read_text().splitlines()
        lines = [line.replace("`source_ids`", "`source_id`") if line.startswith("| `generate_exercise`") else line for line in lines]
        path.write_text("\n".join(lines))
        self.assertTrue(any("generate_exercise incorrect required" in e for e in check(self.root)))

    def test_missing_reference_fails(self):
        (self.root / "skills/create-learning-resources/references/exercises.md").unlink()
        self.assertTrue(any("Missing exercise workflow reference" in e for e in check(self.root)))

    def test_manifest_version_mismatch_fails(self):
        path = self.root / ".claude-plugin/plugin.json"
        data = json.loads(path.read_text())
        data["version"] = "0.0.0"
        path.write_text(json.dumps(data))
        self.assertIn("manifests: inconsistent or missing version", check_metadata(self.root))

    def test_yaml_type_error_fails(self):
        path = self.root / "skills/teach-it-back/agents/openai.yaml"
        path.write_text("interface:\n  display_name: [invalid]\n  short_description: fine\n")
        self.assertTrue(any("missing display_name" in e for e in check_metadata(self.root)))

    def test_broken_skill_reference_fails(self):
        path = self.root / "skills/teach-it-back/SKILL.md"
        path.write_text(path.read_text() + "\n[Workflow](references/missing.md)\n")
        self.assertTrue(any("broken/outside reference" in e for e in check(self.root)))

    def test_ast_extracts_required_optional_and_annotations(self):
        source = '@_tool()\nasync def get_exercise(exercise_id: KulikoId, limit: int = 20): pass\n'
        widget = '@mcp.tool()\nasync def open_exercise(exercise_id: KulikoId): pass\n'
        with patch("scripts.check_exercise_contract.subprocess.check_output", side_effect=[source, widget]):
            result = source_contract(Path("/unused"))
        self.assertEqual(result["get_exercise"], {
            "required": ["exercise_id"], "optional": ["limit"],
            "annotations": {"exercise_id": "KulikoId", "limit": "int"},
        })
        self.assertEqual(result["open_exercise"]["required"], ["exercise_id"])

    def test_remote_signature_drift_fails(self):
        tools = json.loads(FIXTURE.read_text())["tools"]
        tools["generate_exercise"]["required"].append("count")
        with patch("scripts.check_exercise_contract.source_contract", return_value=tools):
            self.assertIn("Connect origin/main tool signatures differ from pinned contract", check(self.root, Path("/unused")))

    def test_broken_nested_reference_fails(self):
        path = self.root / "skills/create-learning-resources/references/exercises.md"
        path.write_text(path.read_text() + "\n[Contract](nested/missing.md)\n")
        self.assertTrue(any("broken/outside reference nested/missing.md" in e for e in check(self.root)))

    def test_constraint_ast_captures_enum_and_validator_bodies(self):
        sources = [
            "SourceSelection = list[str]\ndef _sources(value):\n    if len(set(value)) > 10: raise ValueError('too many')\n    return value\n",
            "ExerciseMode = Literal['apply', 'analyse']\n",
            "LearningResourceLanguage = Literal['english', 'arabic']\n",
        ]
        with patch("scripts.check_exercise_contract.subprocess.check_output", side_effect=sources):
            constraints = source_constraints(Path("/unused"))
        self.assertIn("> 10", constraints["app/mcp/tools/exercises.py"]["_sources"])
        self.assertIn("'analyse'", constraints["app/mcp/exercise_types.py"]["ExerciseMode"])
        self.assertIn("'arabic'", constraints["app/mcp/tool_types.py"]["LearningResourceLanguage"])

    def test_changed_bounds_and_language_aliases_fail(self):
        snapshot = json.loads(FIXTURE.read_text())
        changes = (
            ("app/mcp/tools/exercises.py", "_sources", "> 10", "> 20"),
            ("app/mcp/tools/exercises.py", "_objective", "> 2000", "> 4000"),
            ("app/mcp/exercise_types.py", "ExerciseMode", "'analyse'", "'analyze'"),
            ("app/mcp/tool_types.py", "LearningResourceLanguage", "'french'", "'fr'"),
        )
        for path, name, old, new in changes:
            with self.subTest(name=name):
                constraints = json.loads(json.dumps(snapshot["constraints"]))
                self.assertIn(old, constraints[path][name])
                constraints[path][name] = constraints[path][name].replace(old, new)
                with patch("scripts.check_exercise_contract.source_contract", return_value=snapshot["tools"]), patch(
                    "scripts.check_exercise_contract.source_constraints", return_value=constraints
                ):
                    self.assertIn("Connect origin/main enums or validators differ from pinned contract", check(self.root, Path("/unused")))


if __name__ == "__main__":
    unittest.main()
