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

class BatchEStandardsTests(unittest.TestCase):
    def setUp(self):
        self.r = resources()

    def test_two_resources_are_admitted(self):
        expected = {
            "oxford-common-file-layout-ocfl",
            "data-package-standard",
        }
        self.assertTrue(expected <= self.r.keys())

    def test_ocfl_is_reference_and_others_with_public_validator(self):
        item = self.r["oxford-common-file-layout-ocfl"]
        self.assertEqual(item["implementation_status"], "reference-and-others")
        self.assertEqual(item["conformance_status"], "public-validator")
        refs = {x["ref_id"] for x in item["source_refs"]}
        self.assertIn("ocfl-io-1-1-validation-codes", refs)
        self.assertIn("github-com-ocfl-ocfl-java", refs)

    def test_data_package_encodes_migration_and_validator_boundary(self):
        item = self.r["data-package-standard"]
        self.assertEqual(item["implementation_status"], "reference-and-others")
        self.assertEqual(item["conformance_status"], "public-validator")
        self.assertIn("migrating unevenly", item["boundary_note"])
        self.assertIn("does not prove", item["boundary_note"])
        refs = {x["ref_id"] for x in item["source_refs"]}
        self.assertIn("framework-frictionlessdata-io-validating-data", refs)
        self.assertIn("datapackage-org-blog-2024-06-26-v2-release", refs)

    def test_author_review_provenance(self):
        for rid in ("oxford-common-file-layout-ocfl", "data-package-standard"):
            review = self.r[rid]["review"]
            self.assertEqual(review["review_type"], "author")
            self.assertEqual(review["decision_record"], "issue-44-batch-e")

if __name__ == "__main__":
    unittest.main()
