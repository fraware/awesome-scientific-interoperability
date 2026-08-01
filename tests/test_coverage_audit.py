from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "audit_coverage.py"
spec = importlib.util.spec_from_file_location("audit_coverage", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules["audit_coverage"] = module
spec.loader.exec_module(module)

POLICY_PATH = ROOT / "config" / "coverage-policy.yaml"
FIXTURES = ROOT / "tests" / "fixtures" / "coverage"


class CoverageAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.resources = module.load_resources()
        if len(cls.resources) < 75:
            raise AssertionError(f"expected at least 75 resources, got {len(cls.resources)}")

    def test_live_catalog_integrity(self) -> None:
        policy = module.load_policy(POLICY_PATH)
        failures = module.check_integrity(self.resources, policy, as_of=date(2026, 8, 1))
        self.assertEqual(failures, [])

    def test_live_metrics_reproducible(self) -> None:
        policy = module.load_policy(POLICY_PATH)
        as_of = date(2026, 8, 1)
        first = module.compute_metrics(self.resources, policy, as_of=as_of)
        second = module.compute_metrics(self.resources, policy, as_of=as_of)
        self.assertEqual(first, second)
        self.assertEqual(first["total_entries"], 75)

    def test_live_report_deterministic(self) -> None:
        as_of = date(2026, 8, 1)
        first = module.build_report(as_of=as_of, policy_path=POLICY_PATH)
        second = module.build_report(as_of=as_of, policy_path=POLICY_PATH)
        self.assertEqual(first, second)

    def test_required_metric_sections_present(self) -> None:
        policy = module.load_policy(POLICY_PATH)
        metrics = module.compute_metrics(self.resources, policy, as_of=date(2026, 8, 1))
        for key in (
            "entries_per_section",
            "domains_per_entry",
            "entries_per_domain",
            "interoperability_layers",
            "resource_types",
            "maturity_states",
            "evidence_types",
            "implementation_status",
            "conformance_status",
            "stewardship_types",
            "review_schedule",
            "implementations_per_family",
            "general_purpose_substrates",
        ):
            with self.subTest(key=key):
                self.assertIn(key, metrics)

    def test_warnings_do_not_block_successful_exit(self) -> None:
        code = module.main(["--as-of", "2026-08-01"])
        self.assertEqual(code, 0)

    def test_invalid_review_date_is_blocking(self) -> None:
        policy = module.load_policy(POLICY_PATH)
        broken = dict(self.resources[0])
        broken["review_due_on"] = "2020-01-01"
        broken["reviewed_on"] = "2021-01-01"
        failures = module.check_integrity([broken], policy, as_of=date(2026, 8, 1))
        self.assertIn("review-window-invalid", {failure.code for failure in failures})

    def test_unknown_family_member_is_blocking(self) -> None:
        policy = module.load_policy(POLICY_PATH)
        broken_policy = json.loads(json.dumps(policy))
        broken_policy["standard_families"]["broken"] = ["does-not-exist"]
        failures = module.check_integrity(self.resources, broken_policy, as_of=date(2026, 8, 1))
        self.assertIn("unknown-standard-family-member", {failure.code for failure in failures})

    def test_fixture_warnings(self) -> None:
        with (FIXTURES / "catalog.yaml").open(encoding="utf-8") as handle:
            resources = yaml.safe_load(handle)["resources"]
        policy = module.load_policy(FIXTURES / "policy.yaml")
        metrics = module.compute_metrics(resources, policy, as_of=date(2026, 8, 1))
        warning_codes = {warning.code for warning in module.build_warnings(resources, policy, metrics)}
        self.assertTrue(
            {
                "section-underrepresented",
                "domain-concentration",
                "substrate-concentration",
                "implementation-family-concentration",
                "isolated-entries",
                "evidence-without-source",
            }.issubset(warning_codes)
        )

    def test_json_and_markdown_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = Path(tmpdir) / "report.json"
            markdown_path = Path(tmpdir) / "report.md"
            code = module.main(
                [
                    "--as-of",
                    "2026-08-01",
                    "--json-report",
                    str(json_path),
                    "--markdown-report",
                    str(markdown_path),
                ]
            )
            self.assertEqual(code, 0)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            markdown = markdown_path.read_text(encoding="utf-8")
            self.assertEqual(payload["metrics"]["total_entries"], 75)
            self.assertIn("# Coverage Audit Report", markdown)
            self.assertIn("does not assign quality scores", markdown)


if __name__ == "__main__":
    unittest.main()
