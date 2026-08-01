"""Tests for decision-guide validation."""

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

MODULE_PATH = SCRIPTS / "validate_decision_guides.py"
spec = importlib.util.spec_from_file_location("validate_decision_guides", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

RESOURCE_MARKER_RE = module.RESOURCE_MARKER_RE
collect_markers = module.collect_markers
validate_guides = module.validate_guides

GUIDES_DIR = ROOT / "docs" / "decision-guides"


class TestResourceMarkerPattern(unittest.TestCase):
    def test_matches_catalog_style_ids(self) -> None:
        text = "See [resource:ro-crate] and [resource:workflow-run-ro-crate]."
        self.assertEqual(
            RESOURCE_MARKER_RE.findall(text),
            ["ro-crate", "workflow-run-ro-crate"],
        )


class TestValidateDecisionGuides(unittest.TestCase):
    def test_repo_guides_pass_validation(self) -> None:
        if not GUIDES_DIR.is_dir():
            self.skipTest("decision guides not present in this checkout")
        self.assertEqual(validate_guides(GUIDES_DIR), [])

    def test_unknown_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            guides_dir = Path(tmp)
            guide = guides_dir / "example.md"
            guide.write_text("Broken reference: [resource:not-a-real-id]\n", encoding="utf-8")
            errors = validate_guides(guides_dir)
            self.assertEqual(len(errors), 1)
            self.assertIn("not-a-real-id", errors[0])

    def test_known_id_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            guides_dir = Path(tmp)
            guide = guides_dir / "example.md"
            guide.write_text("Valid reference: [resource:ro-crate]\n", encoding="utf-8")
            self.assertEqual(validate_guides(guides_dir), [])

    def test_collect_markers_reports_line_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            guide = Path(tmp) / "guide.md"
            guide.write_text("Line one\n[resource:bagit]\n", encoding="utf-8")
            markers = collect_markers(guide)
            self.assertEqual(markers, [(2, "bagit")])


if __name__ == "__main__":
    unittest.main()
