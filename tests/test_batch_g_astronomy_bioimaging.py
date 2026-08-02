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

class BatchGAstronomyBioimagingTests(unittest.TestCase):
    def setUp(self): self.r = resources()
    def test_four_boundary_resources_are_admitted(self):
        expected={"ome-data-model-and-ome-tiff","ivoa-observation-core-obscore","ivoa-simple-application-messaging-protocol-samp","advanced-scientific-data-format-asdf"}
        self.assertTrue(expected <= self.r.keys())
    def test_ome_tiff_validator_scope_is_bounded(self):
        item=self.r["ome-data-model-and-ome-tiff"]
        self.assertEqual(item["implementation_status"],"reference-and-others")
        self.assertEqual(item["conformance_status"],"public-validator")
        self.assertIn("does not prove TIFF layout consistency",item["boundary_note"])
    def test_obscore_is_typed_as_tap_profile(self):
        item=self.r["ivoa-observation-core-obscore"]
        self.assertEqual(item["implementation_status"],"multiple-independent")
        edges={(e["type"],e["resource_id"]) for e in item["relations"]}
        self.assertIn(("profile-of","ivoa-table-access-protocol-tap"),edges)
        self.assertIn(("serializes","ivoa-votable"),edges)
    def test_samp_has_independent_implementations_without_suite_claim(self):
        item=self.r["ivoa-simple-application-messaging-protocol-samp"]
        self.assertEqual(item["implementation_status"],"multiple-independent")
        self.assertEqual(item["conformance_status"],"none-known")
        refs={x["ref_id"] for x in item["source_refs"]}
        self.assertTrue({"pyvo-readthedocs-io-samp","star-bris-ac-uk-jsamp"} <= refs)
    def test_asdf_claims_one_verified_full_implementation(self):
        item=self.r["advanced-scientific-data-format-asdf"]
        self.assertEqual(item["implementation_status"],"single-known")
        self.assertEqual(item["conformance_status"],"public-validator")
        self.assertIn("extension manifests",item["boundary_note"])
    def test_all_batch_g_records_disclose_author_review(self):
        for rid in ("ome-data-model-and-ome-tiff","ivoa-observation-core-obscore","ivoa-simple-application-messaging-protocol-samp","advanced-scientific-data-format-asdf"):
            review=self.r[rid]["review"]
            self.assertEqual(review["review_type"],"author")
            self.assertEqual(review["decision_record"],"issue-44-batch-g")
if __name__ == "__main__": unittest.main()
