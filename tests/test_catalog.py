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

MODULE_PATH = SCRIPTS / "validate_catalog.py"
spec = importlib.util.spec_from_file_location("validate_catalog", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

FIXTURES = ROOT / "tests" / "fixtures" / "v2"
LIVE_INDEX = ROOT / "catalog" / "resources.yaml"
SCHEMA_PATH = ROOT / "schema" / "catalog.schema.json"


def known_ids_for(catalog: dict) -> set[str]:
    live_ids = module.load_all_live_ids()
    catalog_ids = {
        resource_id for resource in catalog["resources"] if (resource_id := resource.get("id"))
    }
    return live_ids | catalog_ids


class CatalogTests(unittest.TestCase):
    def test_repository_invariants(self) -> None:
        self.assertEqual(module.validate(), [])

    def test_seed_size(self) -> None:
        catalog, _, readme = module.load()
        self.assertEqual(len(catalog["resources"]), 87)
        self.assertEqual(len(module.readme_entries(readme)), 87)

    def test_catalog_version_is_v2(self) -> None:
        catalog, _, _ = module.load()
        self.assertEqual(catalog["catalog_version"], "2.0.0")

    def test_every_section_has_resources(self) -> None:
        catalog, _, _ = module.load()
        sections = {resource["section"] for resource in catalog["resources"]}
        expected = {
            "Foundations",
            "Identifiers and Discovery",
            "Metadata and Semantics",
            "Data and Digital Objects",
            "Research Software and Environments",
            "Workflows and Execution",
            "Provenance and Evidence",
            "Knowledge Systems and Publications",
            "Instruments and Laboratories",
            "Agents, Access, and Policy",
            "Validation and Conformance",
        }
        self.assertEqual(sections, expected)

    def test_catalog_index_is_complete(self) -> None:
        import yaml

        index_path = ROOT / "catalog" / "resources.yaml"
        index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        self.assertEqual(len(index["resource_files"]), 11)
        for relative_path in index["resource_files"]:
            self.assertTrue((index_path.parent / relative_path).is_file())

    def test_fixture_directory_has_at_least_thirteen_cases(self) -> None:
        fixtures = list(FIXTURES.glob("*.yaml"))
        self.assertGreaterEqual(len(fixtures), 13)

    def test_valid_fixtures_pass(self) -> None:
        import json

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        for path in sorted(FIXTURES.glob("*.valid.yaml")):
            with self.subTest(path=path.name):
                catalog = module.load_catalog_document(path)
                self.assertEqual(
                    module.validate_catalog(catalog, schema, known_ids=known_ids_for(catalog)),
                    [],
                )

    def test_invalid_fixtures_fail(self) -> None:
        import json

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        for path in sorted(FIXTURES.glob("*.invalid.yaml")):
            with self.subTest(path=path.name):
                catalog = module.load_catalog_document(path)
                self.assertTrue(
                    module.validate_catalog(catalog, schema, known_ids=known_ids_for(catalog))
                )

    def test_expired_review_fixture_fails_with_as_of(self) -> None:
        import json

        path = FIXTURES / "14-expired-review.invalid.yaml"
        catalog = module.load_catalog_document(path)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = module.validate_catalog(
            catalog,
            schema,
            known_ids=known_ids_for(catalog),
            as_of=date(2026, 8, 1),
        )
        self.assertTrue(any("review_due_on" in error for error in errors))

    def test_live_catalog_passes_v2(self) -> None:
        import json

        catalog = module.load_catalog_from_index(LIVE_INDEX)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = module.validate_catalog(catalog, schema, known_ids=known_ids_for(catalog))
        self.assertEqual(errors, [])

    def test_no_legacy_fields_in_live_shards(self) -> None:
        catalog, _, _ = module.load()
        legacy = {"evidence_level", "maintenance_signal", "north_star_utility", "description"}
        for resource in catalog["resources"]:
            present = sorted(legacy & set(resource))
            self.assertEqual(present, [], msg=f"{resource.get('id')}: legacy fields {present}")


class ReviewFreshnessTests(unittest.TestCase):
    def test_live_catalog_fresh_as_of_migration_date(self) -> None:
        import check_review_freshness

        catalog = module.load_catalog_from_index(LIVE_INDEX)
        errors = check_review_freshness.review_freshness_errors(
            catalog["resources"],
            as_of=date(2026, 8, 1),
        )
        self.assertEqual(errors, [])

    def test_expired_fixture_fails_freshness_check(self) -> None:
        import check_review_freshness

        catalog = module.load_catalog_document(FIXTURES / "14-expired-review.invalid.yaml")
        errors = check_review_freshness.review_freshness_errors(
            catalog["resources"],
            as_of=date(2026, 8, 1),
        )
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
