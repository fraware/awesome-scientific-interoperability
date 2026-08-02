"""Review provenance and CWL family role-bucket coverage."""

from __future__ import annotations

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

query_spec = importlib.util.spec_from_file_location("query_catalog", SCRIPTS / "query_catalog.py")
query_module = importlib.util.module_from_spec(query_spec)
assert query_spec and query_spec.loader
query_spec.loader.exec_module(query_module)


class ReviewProvenanceTests(unittest.TestCase):
    def test_all_resources_have_review_block(self) -> None:
        for resource in catalog_model.load_catalog_resources():
            review = resource.get("review")
            self.assertIsInstance(review, dict, msg=resource["id"])
            self.assertIn(review["review_type"], {"author", "maintainer", "independent"})
            self.assertEqual(review["reviewed_on"], resource["reviewed_on"])

    def test_review_type_queryable(self) -> None:
        resources = query_module.load_resources()
        authors = query_module.apply_filters(
            resources,
            section=None,
            layer=None,
            domain=None,
            connects=None,
            evidence=None,
            resource_id=None,
            review_type="author",
        )
        self.assertEqual(len(authors), 109)
        independent = query_module.apply_filters(
            resources,
            section=None,
            layer=None,
            domain=None,
            connects=None,
            evidence=None,
            resource_id=None,
            review_type="independent",
        )
        self.assertEqual(independent, [])


if __name__ == "__main__":
    unittest.main()
