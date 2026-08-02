from __future__ import annotations

import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def resources():
    index = yaml.safe_load((ROOT / "catalog/resources.yaml").read_text())
    result = {}
    for rel in index["resource_files"]:
        shard = yaml.safe_load((ROOT / "catalog" / rel).read_text())
        result.update({item["id"]: item for item in shard["resources"]})
    return result

class BatchCGenomicsTests(unittest.TestCase):
    def setUp(self):
        self.r = resources()

    def test_four_resources_are_admitted(self):
        expected = {
            "ga4gh-variation-representation-specification-vrs",
            "ga4gh-phenopackets",
            "ga4gh-htsget",
            "ga4gh-refget-sequences",
        }
        self.assertTrue(expected <= self.r.keys())

    def test_vrs_claim_is_conservative(self):
        item = self.r["ga4gh-variation-representation-specification-vrs"]
        self.assertEqual(item["implementation_status"], "single-known")
        self.assertEqual(item["conformance_status"], "documented-tests")

    def test_phenopackets_has_direct_validator(self):
        item = self.r["ga4gh-phenopackets"]
        self.assertEqual(item["conformance_status"], "public-validator")
        self.assertIn("github-com-phenopackets-phenopacket-tools", {x["ref_id"] for x in item["source_refs"]})

    def test_htsget_is_distinct_from_drs(self):
        item = self.r["ga4gh-htsget"]
        self.assertEqual(item["conformance_status"], "none-known")
        self.assertIn({"type": "complements", "resource_id": "ga4gh-data-repository-service-drs"}, item["relations"])

    def test_refget_has_independent_operators_and_suite(self):
        item = self.r["ga4gh-refget-sequences"]
        self.assertEqual(item["implementation_status"], "multiple-independent")
        self.assertEqual(item["conformance_status"], "public-suite")

if __name__ == "__main__":
    unittest.main()
