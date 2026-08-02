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

class BatchDStandardsTests(unittest.TestCase):
    def setUp(self):
        self.r = resources()

    def test_five_resources_are_admitted(self):
        expected = {
            "minimum-information-about-any-sequence-mixs",
            "ecological-metadata-language-eml",
            "hupo-psi-mzml",
            "omop-common-data-model",
            "cdisc-operational-data-model-odm",
        }
        self.assertTrue(expected <= self.r.keys())

    def test_mixs_claim_is_conservative(self):
        item = self.r["minimum-information-about-any-sequence-mixs"]
        self.assertEqual(item["implementation_status"], "single-known")
        self.assertEqual(item["conformance_status"], "documented-tests")

    def test_eml_has_direct_validator(self):
        item = self.r["ecological-metadata-language-eml"]
        self.assertEqual(item["conformance_status"], "public-validator")
        self.assertIn("eml-ecoinformatics-org-validation", {x["ref_id"] for x in item["source_refs"]})

    def test_mzml_has_independent_operators(self):
        item = self.r["hupo-psi-mzml"]
        self.assertEqual(item["implementation_status"], "multiple-independent")
        self.assertEqual(item["conformance_status"], "public-validator")

    def test_omop_validator_scope_is_explicit(self):
        item = self.r["omop-common-data-model"]
        self.assertEqual(item["conformance_status"], "public-validator")
        self.assertIn("analytical model", item["boundary_note"])

    def test_odm_does_not_inflate_conformance(self):
        item = self.r["cdisc-operational-data-model-odm"]
        self.assertEqual(item["implementation_status"], "single-known")
        self.assertEqual(item["conformance_status"], "none-known")

if __name__ == "__main__":
    unittest.main()
