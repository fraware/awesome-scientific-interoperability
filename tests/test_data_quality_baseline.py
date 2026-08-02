"""CI gate: checked-in data-quality baseline matches live audit."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "audit_data_quality.py"
spec = importlib.util.spec_from_file_location("audit_data_quality", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules["audit_data_quality"] = module
spec.loader.exec_module(module)

BASELINE_JSON = ROOT / "docs" / "data-quality-baseline.json"
BASELINE_MD = ROOT / "docs" / "data-quality-baseline.md"
AS_OF = date(2026, 8, 1)


class DataQualityBaselineTests(unittest.TestCase):
    def test_checked_in_baseline_matches_live_report(self) -> None:
        self.assertTrue(BASELINE_JSON.is_file(), f"missing {BASELINE_JSON}")
        report = module.build_report(as_of=AS_OF)
        mismatches = module.check_baseline(report, BASELINE_JSON)
        self.assertEqual(mismatches, [], msg="; ".join(mismatches))

    def test_baseline_markdown_exists_beside_json(self) -> None:
        self.assertTrue(BASELINE_MD.is_file(), f"missing {BASELINE_MD}")
        text = BASELINE_MD.read_text(encoding="utf-8")
        snapshot = json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
        counts = snapshot["counts"]
        self.assertIn(f"{counts['references']} references", text)
        self.assertIn(f"{counts['stewards']} stewards", text)
        self.assertIn(f"{counts.get('implementations', 0)} implementations", text)
        self.assertIn(
            f"| Unsupported `multiple-independent` | {counts['multiple_independent_queue']} |",
            text,
        )
        self.assertIn(
            f"| Unsupported `documented-tests` | {counts['documented_tests_queue']} |",
            text,
        )

    def test_check_baseline_cli_passes(self) -> None:
        code = module.main(
            ["--as-of", AS_OF.isoformat(), "--check-baseline", str(BASELINE_JSON)]
        )
        self.assertEqual(code, 0)

    def test_check_baseline_detects_drift(self) -> None:
        report = module.build_report(as_of=AS_OF)
        snapshot = module.baseline_snapshot(report)
        snapshot["counts"]["references"] = snapshot["counts"]["references"] + 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data-quality-baseline.json"
            path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
            mismatches = module.check_baseline(report, path)
            self.assertTrue(any(item.startswith("counts.references:") for item in mismatches))
            code = module.main(
                ["--as-of", AS_OF.isoformat(), "--check-baseline", str(path)]
            )
            self.assertEqual(code, 1)

    def test_write_baseline_round_trip(self) -> None:
        report = module.build_report(as_of=AS_OF)
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "data-quality-baseline.json"
            module.write_baseline(report, json_path)
            self.assertTrue(json_path.is_file())
            self.assertTrue(json_path.with_suffix(".md").is_file())
            self.assertEqual(module.check_baseline(report, json_path), [])


if __name__ == "__main__":
    unittest.main()
