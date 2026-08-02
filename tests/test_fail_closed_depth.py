"""Fail-closed evidence-depth regressions (PR #39)."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib import catalog_model  # noqa: E402

validate_spec = importlib.util.spec_from_file_location(
    "validate_catalog", SCRIPTS / "validate_catalog.py"
)
validate_module = importlib.util.module_from_spec(validate_spec)
assert validate_spec and validate_spec.loader
validate_spec.loader.exec_module(validate_module)

audit_spec = importlib.util.spec_from_file_location(
    "audit_data_quality", SCRIPTS / "audit_data_quality.py"
)
audit_module = importlib.util.module_from_spec(audit_spec)
assert audit_spec and audit_spec.loader
sys.modules["audit_data_quality"] = audit_module
audit_spec.loader.exec_module(audit_module)


class FailClosedDepthTests(unittest.TestCase):
    def test_documented_tests_without_artifact_fails_validator(self) -> None:
        catalog, schema, _ = validate_module.load()
        resource = copy.deepcopy(catalog["resources"][0])
        resource["conformance_status"] = "documented-tests"
        # Keep only non-artifact technical-definition refs.
        resource["source_refs"] = [
            item
            for item in resource["source_refs"]
            if item.get("role") == "technical-definition"
        ] or [{"ref_id": resource["source_refs"][0]["ref_id"], "role": "technical-definition"}]
        catalog["resources"] = [resource]
        errors = validate_module.validate_catalog(catalog, schema, as_of=date(2026, 8, 1))
        self.assertTrue(
            any("documented-tests requires a direct conformance artifact" in error for error in errors),
            errors,
        )

    def test_homepage_as_conformance_artifact_fails(self) -> None:
        catalog, schema, _ = validate_module.load()
        references = catalog_model.load_references()
        homepage_ref = next(
            (
                ref_id
                for ref_id, ref in references.items()
                if ref.get("type") in {"governance-source", "technical-documentation"}
            ),
            None,
        )
        self.assertIsNotNone(homepage_ref)
        resource = copy.deepcopy(catalog["resources"][0])
        resource["conformance_status"] = "documented-tests"
        resource["source_refs"] = [
            {"ref_id": homepage_ref, "role": "conformance"},
            {"ref_id": resource["source_refs"][0]["ref_id"], "role": "technical-definition"},
        ]
        catalog["resources"] = [resource]
        errors = validate_module.validate_catalog(catalog, schema, as_of=date(2026, 8, 1))
        self.assertTrue(
            any("documented-tests requires a direct conformance artifact" in error for error in errors),
            errors,
        )

    def test_generic_documentation_does_not_count_as_independent_implementation(self) -> None:
        catalog, schema, _ = validate_module.load()
        resource = copy.deepcopy(
            next(
                item
                for item in catalog["resources"]
                if item["id"] == "model-context-protocol-mcp"
            )
        )
        resource["implementation_status"] = "multiple-independent"
        implementations = [
            {
                "id": "mcp-docs-a",
                "name": "MCP docs A",
                "url": "https://modelcontextprotocol.io/",
                "implements_resource_id": "model-context-protocol-mcp",
                "operator_steward_id": "model-context-protocol-project",
                "relationship": "official-implementation",
                "evidence_ref_ids": ["modelcontextprotocol-io-root"],
            },
            {
                "id": "mcp-docs-b",
                "name": "MCP docs B",
                "url": "https://modelcontextprotocol.io/specification/2026-07-28",
                "implements_resource_id": "model-context-protocol-mcp",
                "operator_steward_id": "model-context-protocol-project",
                "relationship": "official-implementation",
                "evidence_ref_ids": ["modelcontextprotocol-io-specification-2026-07-28"],
            },
        ]
        catalog["resources"] = [resource]
        errors = validate_module.validate_catalog(
            catalog,
            schema,
            as_of=date(2026, 8, 1),
            check_registries=False,
            implementations=implementations,
        )
        self.assertTrue(
            any("multiple-independent requires ≥2 distinct" in error for error in errors),
            errors,
        )

    def test_audit_fail_on_warning_passes_clean_head(self) -> None:
        code = audit_module.main(
            [
                "--as-of",
                "2026-08-01",
                "--fail-on",
                "warning",
                "--check-baseline",
                str(ROOT / "docs" / "data-quality-baseline.json"),
            ]
        )
        self.assertEqual(code, 0)

    def test_live_catalog_has_no_depth_queues(self) -> None:
        report = audit_module.build_report(as_of=date(2026, 8, 1))
        self.assertEqual(report["counts"]["integrity_errors"], 0)
        self.assertEqual(report["counts"]["multiple_independent_queue"], 0)
        self.assertEqual(report["counts"]["documented_tests_queue"], 0)


if __name__ == "__main__":
    unittest.main()
