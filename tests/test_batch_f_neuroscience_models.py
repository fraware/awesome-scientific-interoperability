from __future__ import annotations

import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def resources():
    index = yaml.safe_load((ROOT / "catalog/resources.yaml").read_text(encoding="utf-8"))
    result = {}
    for rel in index["resource_files"]:
        shard = yaml.safe_load((ROOT / "catalog" / rel).read_text(encoding="utf-8"))
        result.update({item["id"]: item for item in shard["resources"]})
    return result


class BatchFNeuroscienceModelTests(unittest.TestCase):
    def setUp(self):
        self.r = resources()

    def test_two_resources_are_admitted(self):
        self.assertTrue({"neuroml", "sonata"} <= self.r.keys())

    def test_neuroml_claims_direct_validator_without_overclaiming_independence(self):
        item = self.r["neuroml"]
        self.assertEqual(item["implementation_status"], "reference-and-others")
        self.assertEqual(item["conformance_status"], "public-validator")
        refs = {(x["ref_id"], x["role"]) for x in item["source_refs"]}
        self.assertIn(("docs-neuroml-org-userdocs-validating-neuroml-models", "conformance"), refs)
        self.assertIn(("doc-netpyne-org-neuroml-format", "implementation"), refs)
        self.assertIn("does not prove", item["boundary_note"])

    def test_sonata_claims_are_conservative(self):
        item = self.r["sonata"]
        self.assertEqual(item["implementation_status"], "reference-and-others")
        self.assertEqual(item["conformance_status"], "none-known")
        self.assertIn("No public format-wide conformance suite", item["boundary_note"])
        refs = {x["ref_id"] for x in item["source_refs"]}
        self.assertIn("github-com-alleninstitute-bmtk", refs)
        self.assertIn("doc-netpyne-org-sonata-import", refs)

    def test_complementary_boundary_is_typed(self):
        neuroml_edges = {(x["type"], x["resource_id"]) for x in self.r["neuroml"]["relations"]}
        sonata_edges = {(x["type"], x["resource_id"]) for x in self.r["sonata"]["relations"]}
        self.assertIn(("complements", "sonata"), neuroml_edges)
        self.assertIn(("complements", "neuroml"), sonata_edges)

    def test_author_review_provenance(self):
        for rid in ("neuroml", "sonata"):
            review = self.r[rid]["review"]
            self.assertEqual(review["review_type"], "author")
            self.assertEqual(review["decision_record"], "issue-44-batch-f")


if __name__ == "__main__":
    unittest.main()
