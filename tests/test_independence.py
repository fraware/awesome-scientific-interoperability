"""Tests for implementation-independence semantics (catalog v2.2)."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.independence import (  # noqa: E402
    independent_operator_stewards,
    multiple_independent_satisfied,
)

validate_spec = importlib.util.spec_from_file_location(
    "validate_catalog", SCRIPTS / "validate_catalog.py"
)
validate_module = importlib.util.module_from_spec(validate_spec)
assert validate_spec and validate_spec.loader
validate_spec.loader.exec_module(validate_module)

SCHEMA = json.loads((ROOT / "schema" / "catalog.schema.json").read_text(encoding="utf-8"))


def _resource(**overrides):
    base = {
        "id": "example-protocol",
        "name": "Example Protocol",
        "url": "https://example.org/spec",
        "section": "Foundations",
        "resource_kind": "specification",
        "interoperability_layers": ["Syntactic"],
        "connects": ["systems", "tools"],
        "mechanism": "Example mechanism text for independence fixtures",
        "summary": "Example summary that starts with an uppercase character and ends correctly.",
        "maturity": "established",
        "evidence_types": ["normative-specification", "independent-implementation"],
        "implementation_status": "multiple-independent",
        "conformance_status": "none-known",
        "steward_id": "example-steward",
        "scientific_domains": [],
        "integration_functions": [],
        "infrastructure_contexts": ["cross-domain"],
        "artifact_classes": [],
        "source_refs": [
            {"ref_id": "fixture-ref-1", "role": "technical-definition"},
            {"ref_id": "fixture-ref-2", "role": "implementation"},
        ],
        "relations": [{"type": "complements", "resource_id": "bagit"}],
        "decision_basis": "Fixture decision basis text for independence tests.",
        "boundary_note": "Fixture boundary note text for independence tests.",
        "reviewed_on": "2026-08-01",
        "review_due_on": "2027-08-01",
        "primary_source_inspected": True,
        "review": {
            "reviewed_by": "catalog-maintainers",
            "review_type": "author",
            "reviewed_on": "2026-08-01",
            "conflict_disclosure": "none",
        },
    }
    base.update(overrides)
    return base


def _catalog(resource):
    return {
        "catalog_version": "2.2.0",
        "reviewed_on": "2026-08-02",
        "north_star": "A technically competent user should identify the strongest interoperability mechanism.",
        "resources": [resource],
    }


class IndependenceUnitTests(unittest.TestCase):
    def test_same_steward_operators_do_not_count(self) -> None:
        resource = _resource(steward_id="model-context-protocol-project")
        implementations = [
            {
                "id": "mcp-a",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "model-context-protocol-project",
                "relationship": "independent-implementation",
            },
            {
                "id": "mcp-b",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "model-context-protocol-project",
                "relationship": "independent-implementation",
            },
        ]
        self.assertEqual(independent_operator_stewards(resource, implementations), [])
        self.assertFalse(multiple_independent_satisfied(resource, implementations))

    def test_official_relationship_does_not_count(self) -> None:
        resource = _resource()
        implementations = [
            {
                "id": "a",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "operator-a",
                "relationship": "official-implementation",
            },
            {
                "id": "b",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "operator-b",
                "relationship": "official-implementation",
            },
        ]
        self.assertFalse(multiple_independent_satisfied(resource, implementations))

    def test_two_distinct_independent_operators_pass(self) -> None:
        resource = _resource()
        implementations = [
            {
                "id": "a",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "operator-a",
                "relationship": "independent-implementation",
            },
            {
                "id": "b",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "operator-b",
                "relationship": "independent-implementation",
            },
        ]
        self.assertEqual(
            independent_operator_stewards(resource, implementations),
            ["operator-a", "operator-b"],
        )
        self.assertTrue(multiple_independent_satisfied(resource, implementations))


class IndependenceValidatorTests(unittest.TestCase):
    def test_mcp_pattern_fails_validation(self) -> None:
        resource = _resource(
            id="model-context-protocol-mcp",
            steward_id="model-context-protocol-project",
        )
        implementations = [
            {
                "id": "mcp-spec",
                "implements_resource_id": "model-context-protocol-mcp",
                "operator_steward_id": "model-context-protocol-project",
                "relationship": "independent-implementation",
            },
            {
                "id": "mcp-servers",
                "implements_resource_id": "model-context-protocol-mcp",
                "operator_steward_id": "model-context-protocol-project",
                "relationship": "independent-implementation",
            },
        ]
        errors = validate_module.validate_catalog(
            _catalog(resource),
            SCHEMA,
            known_ids={"model-context-protocol-mcp", "bagit"},
            check_registries=False,
            implementations=implementations,
        )
        self.assertTrue(
            any("multiple-independent requires ≥2 distinct" in error for error in errors),
            errors,
        )

    def test_missing_operator_does_not_satisfy(self) -> None:
        resource = _resource()
        implementations = [
            {
                "id": "only-one",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "operator-a",
                "relationship": "independent-implementation",
            }
        ]
        errors = validate_module.validate_catalog(
            _catalog(resource),
            SCHEMA,
            known_ids={"example-protocol", "bagit"},
            check_registries=False,
            implementations=implementations,
        )
        self.assertTrue(
            any("multiple-independent requires ≥2 distinct" in error for error in errors),
            errors,
        )

    def test_valid_two_operator_pass(self) -> None:
        resource = _resource()
        implementations = [
            {
                "id": "a",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "operator-a",
                "relationship": "independent-implementation",
            },
            {
                "id": "b",
                "implements_resource_id": "example-protocol",
                "operator_steward_id": "operator-b",
                "relationship": "independent-implementation",
            },
        ]
        errors = validate_module.validate_catalog(
            _catalog(resource),
            SCHEMA,
            known_ids={"example-protocol", "bagit"},
            check_registries=False,
            implementations=implementations,
        )
        self.assertEqual(errors, [])

    def test_live_mcp_is_not_multiple_independent(self) -> None:
        catalog, _, _ = validate_module.load()
        mcp = next(item for item in catalog["resources"] if item["id"] == "model-context-protocol-mcp")
        self.assertNotEqual(mcp["implementation_status"], "multiple-independent")

    def test_live_remaining_mi_count(self) -> None:
        catalog, _, _ = validate_module.load()
        mi = [
            item["id"]
            for item in catalog["resources"]
            if item.get("implementation_status") == "multiple-independent"
        ]
        self.assertEqual(
            sorted(mi),
            [
                "bagit",
                "common-workflow-language-cwl",
                "dicomweb",
                "ga4gh-tool-registry-service-trs",
                "optimade",
                "workflow-description-language-wdl",
            ],
        )


if __name__ == "__main__":
    unittest.main()
