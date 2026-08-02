from __future__ import annotations

import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "query_catalog.py"
spec = importlib.util.spec_from_file_location("query_catalog", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class QueryCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.resources = module.load_resources()
        if len(cls.resources) < 87:
            raise AssertionError(f"expected at least 87 resources, got {len(cls.resources)}")

    def run_query(self, *args: str) -> tuple[int, str]:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = module.main(list(args))
        return code, buffer.getvalue()

    def resource_ids(self, output: str) -> list[str]:
        payload = json.loads(output)
        return [item["id"] for item in payload]

    def test_section_filter(self) -> None:
        code, output = self.run_query("--section", "Workflows and Execution", "--format", "json")
        self.assertEqual(code, 0)
        ids = self.resource_ids(output)
        self.assertTrue(ids)
        for resource in json.loads(output):
            self.assertEqual(resource["section"], "Workflows and Execution")

    def test_layer_filter(self) -> None:
        code, output = self.run_query("--layer", "Operational", "--format", "json")
        self.assertEqual(code, 0)
        for resource in json.loads(output):
            self.assertIn("Operational", resource["interoperability_layers"])

    def test_domain_filter(self) -> None:
        code, output = self.run_query("--domain", "genomics", "--format", "json")
        self.assertEqual(code, 0)
        ids = self.resource_ids(output)
        self.assertIn("ga4gh-data-repository-service-drs", ids)
        for resource in json.loads(output):
            tags = [
                tag.casefold()
                for field in (
                    "scientific_domains",
                    "integration_functions",
                    "infrastructure_contexts",
                    "artifact_classes",
                )
                for tag in resource.get(field) or []
            ]
            self.assertIn("genomics", tags)

    def test_connects_filter(self) -> None:
        code, output = self.run_query("--connects", "workflow registry", "--format", "json")
        self.assertEqual(code, 0)
        ids = self.resource_ids(output)
        self.assertIn("workflowhub", ids)
        for resource in module.apply_filters(
            self.resources,
            section=None,
            layer=None,
            domain=None,
            connects="workflow registry",
            evidence=None,
            resource_id=None,
        ):
            self.assertTrue(module.matches_connects(resource, "workflow registry"))

    def test_evidence_filter(self) -> None:
        code, output = self.run_query("--evidence", "conformance-suite", "--format", "json")
        self.assertEqual(code, 0)
        for resource in json.loads(output):
            self.assertIn("conformance-suite", resource["evidence_types"])

    def test_id_filter(self) -> None:
        code, output = self.run_query("--id", "ro-crate", "--format", "json")
        self.assertEqual(code, 0)
        payload = json.loads(output)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["id"], "ro-crate")

    def test_combined_filters(self) -> None:
        code, output = self.run_query(
            "--section",
            "Workflows and Execution",
            "--layer",
            "Operational",
            "--domain",
            "genomics",
            "--format",
            "json",
        )
        self.assertEqual(code, 0)
        payload = json.loads(output)
        self.assertTrue(payload)
        for resource in payload:
            self.assertEqual(resource["section"], "Workflows and Execution")
            self.assertIn("Operational", resource["interoperability_layers"])
            tags = [
                tag.casefold()
                for field in (
                    "scientific_domains",
                    "integration_functions",
                    "infrastructure_contexts",
                    "artifact_classes",
                )
                for tag in resource.get(field) or []
            ]
            self.assertIn("genomics", tags)

    def test_no_results(self) -> None:
        code, markdown = self.run_query("--id", "does-not-exist", "--format", "markdown")
        self.assertEqual(code, 0)
        self.assertIn("No catalog resources matched the query.", markdown)

        code, output = self.run_query("--id", "does-not-exist", "--format", "json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output), [])

    def test_json_stability(self) -> None:
        _, first = self.run_query("--layer", "Evidentiary", "--format", "json")
        _, second = self.run_query("--layer", "Evidentiary", "--format", "json")
        self.assertEqual(first, second)
        payload = json.loads(first)
        expected_ids = [resource["id"] for resource in module.sort_resources(
            [resource for resource in self.resources if "Evidentiary" in resource.get("interoperability_layers", [])]
        )]
        self.assertEqual([item["id"] for item in payload], expected_ids)

    def test_markdown_includes_boundary_and_relations(self) -> None:
        _, markdown = self.run_query("--id", "ro-crate", "--format", "markdown")
        self.assertIn("Boundary note:", markdown)
        self.assertIn("Relations:", markdown)
        self.assertIn("bagit", markdown)

    def test_ro_crate_family_typed_edges(self) -> None:
        by_id = {resource["id"]: resource for resource in self.resources}
        profiles = {
            item["resource_id"]
            for item in by_id["workflow-ro-crate"].get("relations", [])
            if item["type"] == "profile-of"
        }
        self.assertIn("ro-crate", profiles)
        validates = {
            item["resource_id"]
            for item in by_id["ro-crate-validator"].get("relations", [])
            if item["type"] == "validates"
        }
        self.assertIn("ro-crate", validates)

    def test_invalid_section(self) -> None:
        code, _ = self.run_query("--section", "Not A Section", "--format", "json")
        self.assertEqual(code, 2)

    def test_invalid_evidence(self) -> None:
        code, _ = self.run_query("--evidence", "not-an-evidence-type", "--format", "json")
        self.assertEqual(code, 2)

    def test_empty_connects_query_does_not_match(self) -> None:
        matched = module.apply_filters(
            self.resources,
            section=None,
            layer=None,
            domain=None,
            connects="   ",
            evidence=None,
            resource_id=None,
        )
        self.assertEqual(matched, [])


if __name__ == "__main__":
    unittest.main()
