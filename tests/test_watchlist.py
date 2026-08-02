from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "validate_watchlist.py"
spec = importlib.util.spec_from_file_location("validate_watchlist", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

FIXTURES = ROOT / "tests" / "fixtures" / "watchlist"
LIVE_WATCHLIST = ROOT / "catalog" / "watchlist.yaml"
SCHEMA_PATH = ROOT / "schema" / "watchlist.schema.json"
PROSE_PATH = ROOT / "docs" / "watchlist.md"


class WatchlistTests(unittest.TestCase):
    def test_repository_invariants(self) -> None:
        self.assertEqual(module.validate(), [])

    def test_seed_size(self) -> None:
        watchlist = module.load_watchlist()
        prose = module.prose_entries(PROSE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(len(watchlist["items"]), 17)
        self.assertEqual(len(prose), 17)

    def test_watchlist_does_not_count_toward_main_list(self) -> None:
        import validate_catalog

        catalog, _, readme = validate_catalog.load()
        self.assertEqual(len(catalog["resources"]), 92)
        self.assertEqual(len(validate_catalog.readme_entries(readme)), 92)

    def test_no_catalog_id_overlap(self) -> None:
        watchlist = module.load_watchlist()
        catalog_ids = module.load_catalog_ids()
        watchlist_ids = {item["id"] for item in watchlist["items"]}
        self.assertFalse(watchlist_ids & catalog_ids)

    def test_prose_parity(self) -> None:
        watchlist = module.load_watchlist()
        prose = PROSE_PATH.read_text(encoding="utf-8")
        self.assertEqual(module.parity_errors(watchlist, prose), [])

    def test_valid_fixtures_pass(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        for path in sorted(FIXTURES.glob("*.valid.yaml")):
            with self.subTest(path=path.name):
                watchlist = module.load_watchlist(path)
                self.assertEqual(
                    module.validate_watchlist(watchlist, schema, check_references=False),
                    [],
                )

    def test_invalid_fixtures_fail(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        for path in sorted(FIXTURES.glob("*.invalid.yaml")):
            with self.subTest(path=path.name):
                watchlist = module.load_watchlist(path)
                self.assertTrue(
                    module.validate_watchlist(watchlist, schema, check_references=False)
                )

    def test_expired_review_fixture_fails_with_as_of(self) -> None:
        path = FIXTURES / "02-expired-review.invalid.yaml"
        watchlist = module.load_watchlist(path)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = module.validate_watchlist(
            watchlist, schema, as_of=date(2026, 8, 1), check_references=False
        )
        self.assertTrue(any("review_due_on" in error for error in errors))

    def test_unknown_section_fixture_fails(self) -> None:
        path = FIXTURES / "03-unknown-section.invalid.yaml"
        watchlist = module.load_watchlist(path)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = module.validate_watchlist(watchlist, schema)
        self.assertTrue(any("unknown candidate_section" in error for error in errors))

    def test_live_watchlist_passes_schema(self) -> None:
        watchlist = module.load_watchlist(LIVE_WATCHLIST)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = module.validate_watchlist(watchlist, schema)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
