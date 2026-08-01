from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "validate_problem_index.py"
spec = importlib.util.spec_from_file_location("validate_problem_index", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class ProblemIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog_ids = module.load_catalog_ids()
        cls.doc_path = ROOT / "docs" / "integration-problems.md"
        if not cls.doc_path.is_file():
            raise AssertionError("docs/integration-problems.md is missing")

    def test_live_document_passes(self) -> None:
        errors = module.validate(self.doc_path, self.catalog_ids)
        self.assertEqual(errors, [])

    def test_main_returns_zero_for_live_document(self) -> None:
        self.assertEqual(module.main(["--doc", str(self.doc_path)]), 0)

    def test_unknown_resource_id_fails(self) -> None:
        text = self.doc_path.read_text(encoding="utf-8")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
            handle.write(text.replace("[resource:orcid]", "[resource:not-a-real-id]"))
            temp_path = Path(handle.name)
        try:
            errors = module.validate(temp_path, self.catalog_ids)
            self.assertTrue(any("unknown catalog resource ID" in error for error in errors))
            self.assertEqual(module.main(["--doc", str(temp_path)]), 1)
        finally:
            temp_path.unlink(missing_ok=True)

    def test_duplicate_problem_identifier_fails(self) -> None:
        text = self.doc_path.read_text(encoding="utf-8")
        duplicate = text.replace(
            "[problem:discover-resources]",
            "[problem:identify-research-objects]",
            1,
        )
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
            handle.write(duplicate)
            temp_path = Path(handle.name)
        try:
            errors = module.validate(temp_path, self.catalog_ids)
            self.assertTrue(any("duplicate problem identifier" in error for error in errors))
            self.assertEqual(module.main(["--doc", str(temp_path)]), 1)
        finally:
            temp_path.unlink(missing_ok=True)

    def test_missing_required_problem_fails(self) -> None:
        text = self.doc_path.read_text(encoding="utf-8")
        trimmed = text.replace("[problem:validate-conformance]", "[problem:removed-problem]")
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as handle:
            handle.write(trimmed)
            temp_path = Path(handle.name)
        try:
            errors = module.validate(temp_path, self.catalog_ids)
            self.assertTrue(any("missing required problem identifiers" in error for error in errors))
            self.assertTrue(any("unexpected problem identifiers" in error for error in errors))
        finally:
            temp_path.unlink(missing_ok=True)

    def test_all_main_sections_referenced(self) -> None:
        text = self.doc_path.read_text(encoding="utf-8")
        for section in module.MAIN_SECTIONS:
            with self.subTest(section=section):
                self.assertIn(section, text)

    def test_each_problem_has_resource_markers(self) -> None:
        text = self.doc_path.read_text(encoding="utf-8")
        for problem_id in module.REQUIRED_PROBLEMS:
            marker = f"[problem:{problem_id}]"
            start = text.index(marker)
            next_problem = text.find("[problem:", start + len(marker))
            section = text[start:] if next_problem == -1 else text[start:next_problem]
            self.assertRegex(
                section,
                r"\[resource:[a-z0-9-]+\]",
                msg=f"{problem_id} has no resource markers",
            )


if __name__ == "__main__":
    unittest.main()
