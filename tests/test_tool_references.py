from pathlib import Path
import tempfile
import unittest

from scripts.check_tool_references import check, RETIRED_TOOLS, ROOT


class ToolReferenceTests(unittest.TestCase):
    def test_current_package(self):
        _, errors = check(ROOT)
        self.assertEqual(errors, [])

    def test_rejects_each_retired_name_across_public_surfaces(self):
        surfaces = (
            "plugin.json", "mcp.json", ".mcp.json", "README.md",
            ".codex-plugin/plugin.json", ".claude-plugin/plugin.json",
            "skills/example/SKILL.md", "skills/example/agents/openai.yaml",
            "skills/example/references/nested/example.md",
            "examples/review.json", "docs/review.md", "assets/example.svg",
        )
        for surface in surfaces:
            for name in RETIRED_TOOLS:
                with self.subTest(surface=surface, name=name), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "plugin.json").write_text("{}")
                    skill = root / "skills/example/SKILL.md"
                    skill.parent.mkdir(parents=True)
                    skill.write_text("Use `generate_study_guide`.\n")
                    target = root / surface
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(f"Example\nUse `mcp__kuliko__{name}`.\n")
                    _, errors = check(root)
                    self.assertEqual(len(errors), 1)
                    self.assertIn(f"{surface}:2: retired {name}", errors[0])

    def test_supported_names_and_non_tool_prefixes_are_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "plugin.json").write_text("{}")
            skill = root / "skills/example/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "generate_study_guide open_study_guide_generator create_subject "
                "generate_resources generate_learning_resources "
                "create_documents create_documentation recreate_document"
            )
            self.assertEqual(check(root)[1], [])

    def test_empty_package_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(check(Path(tmp))[1])

    def test_invalid_utf8_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "plugin.json").write_bytes(b"\xff")
            skill = root / "skills/example/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("generate_study_guide")
            self.assertIn("cannot read public text", check(root)[1][0])


if __name__ == "__main__":
    unittest.main()
