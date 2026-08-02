"""Tests for catalog v2.1 provenance registries and semantic guards."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib import catalog_model

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


class ProvenanceV21Tests(unittest.TestCase):
    def test_taxonomy_counts(self) -> None:
        taxonomy = catalog_model.load_taxonomy()
        self.assertEqual(len(taxonomy["resource_kinds"]), 14)
        self.assertEqual(len(taxonomy["scientific_domains"]), 26)
        self.assertEqual(len(taxonomy["integration_functions"]), 14)
        self.assertEqual(len(taxonomy["infrastructure_contexts"]), 5)
        self.assertEqual(len(taxonomy["artifact_classes"]), 2)
        self.assertEqual(len(taxonomy["claim_roles"]), 8)
        self.assertEqual(len(catalog_model.domain_ids()), 47)

    def test_registries_load(self) -> None:
        references = catalog_model.load_references()
        stewards = catalog_model.load_stewards()
        implementations = catalog_model.load_implementations()
        self.assertGreaterEqual(len(references), 200)
        self.assertGreaterEqual(len(stewards), 60)
        self.assertGreaterEqual(len(implementations), 12)

    def test_live_resources_use_controlled_kinds_and_domains(self) -> None:
        kinds = catalog_model.resource_kind_ids()
        dimensions = catalog_model.taxonomy_dimension_ids()
        for resource in catalog_model.load_catalog_resources():
            self.assertIn(resource["resource_kind"], kinds)
            for field, allowed in dimensions.items():
                for tag in resource.get(field) or []:
                    self.assertIn(tag, allowed)
            self.assertTrue(catalog_model.resource_dimension_tags(resource))

    def test_all_source_refs_resolve(self) -> None:
        references = catalog_model.load_references()
        roles = catalog_model.claim_role_ids()
        for resource in catalog_model.load_catalog_resources():
            for item in resource["source_refs"]:
                self.assertIn(item["ref_id"], references)
                self.assertIn(item["role"], roles)

    def test_all_stewards_resolve(self) -> None:
        stewards = catalog_model.load_stewards()
        for resource in catalog_model.load_catalog_resources():
            self.assertIn(resource["steward_id"], stewards)

    def test_zero_isolates(self) -> None:
        isolates = [
            resource["id"]
            for resource in catalog_model.load_catalog_resources()
            if not resource.get("relations")
        ]
        self.assertEqual(isolates, [])

    def test_relation_types_controlled(self) -> None:
        allowed = catalog_model.relation_type_ids()
        self.assertIn("profile-of", allowed)
        self.assertIn("validates", allowed)
        for resource in catalog_model.load_catalog_resources():
            for item in resource.get("relations") or []:
                self.assertIn(item["type"], allowed)

    def test_public_conformance_requires_artifact_class(self) -> None:
        references = catalog_model.load_references()
        artifacts = catalog_model.conformance_artifact_types()
        for resource in catalog_model.load_catalog_resources():
            if resource["conformance_status"] not in {"public-suite", "public-validator"}:
                continue
            ok = False
            for item in resource["source_refs"]:
                ref = references[item["ref_id"]]
                if ref["type"] in artifacts and item["role"] in {
                    "conformance",
                    "interoperability-testing",
                }:
                    ok = True
                    break
            self.assertTrue(ok, msg=resource["id"])

    def test_ogc_coverages_correction(self) -> None:
        resource = next(
            item
            for item in catalog_model.load_catalog_resources()
            if item["id"] == "ogc-api-coverages"
        )
        self.assertEqual(resource["maturity"], "emerging")
        self.assertEqual(resource["implementation_status"], "reference-and-others")
        self.assertEqual(resource["conformance_status"], "none-known")
        self.assertNotIn("conformance-suite", resource["evidence_types"])

    def test_no_generic_placeholder_references(self) -> None:
        for ref in catalog_model.load_references().values():
            url = ref["url"].casefold()
            self.assertNotIn("example.com", url)
            self.assertNotIn("example.org", url)

    def test_reference_steward_and_implementation_schemas(self) -> None:
        from jsonschema import Draft202012Validator, FormatChecker

        for name in ("references", "stewards", "implementations"):
            payload = yaml.safe_load((ROOT / "catalog" / f"{name}.yaml").read_text(encoding="utf-8"))
            schema = json.loads((ROOT / "schema" / f"{name}.schema.json").read_text(encoding="utf-8"))
            errors = sorted(
                Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(payload),
                key=lambda item: list(item.absolute_path),
            )
            self.assertEqual(errors, [], msg=name)

    def test_audit_report_structure(self) -> None:
        report = audit_module.build_report(as_of=date(2026, 8, 1))
        self.assertEqual(report["counts"]["integrity_errors"], 0)
        self.assertIn("multiple_independent", report["queues"])
        self.assertIn("documented_tests", report["queues"])
        self.assertGreaterEqual(report["counts"]["multiple_independent_queue"], 0)

    def test_audit_fail_on_error_with_clean_integrity(self) -> None:
        code = audit_module.main(
            [
                "--as-of",
                "2026-08-01",
                "--fail-on",
                "error",
            ]
        )
        self.assertEqual(code, 0)

    def test_unknown_domain_rejected(self) -> None:
        catalog, schema, _ = validate_module.load()
        catalog["resources"] = [dict(catalog["resources"][0])]
        catalog["resources"][0]["scientific_domains"] = ["not-a-real-domain"]
        errors = validate_module.validate_catalog(catalog, schema, as_of=date(2026, 8, 1))
        self.assertTrue(any("unknown scientific_domains value" in error for error in errors))

    def test_unknown_kind_rejected(self) -> None:
        catalog, schema, _ = validate_module.load()
        catalog["resources"] = [dict(catalog["resources"][0])]
        catalog["resources"][0]["resource_kind"] = "not-a-kind"
        errors = validate_module.validate_catalog(catalog, schema, as_of=date(2026, 8, 1))
        self.assertTrue(any("resource_kind" in error for error in errors))

    def test_unresolved_ref_rejected(self) -> None:
        catalog, schema, _ = validate_module.load()
        catalog["resources"] = [dict(catalog["resources"][0])]
        catalog["resources"][0]["source_refs"] = [
            {"ref_id": "does-not-exist-ref", "role": "technical-definition"}
        ]
        errors = validate_module.validate_catalog(catalog, schema, as_of=date(2026, 8, 1))
        self.assertTrue(any("unresolved ref_id" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
