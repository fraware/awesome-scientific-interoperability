from __future__ import annotations

import importlib.util
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_expansion_candidates.py"
SPEC = importlib.util.spec_from_file_location("validate_expansion_candidates", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class ExpansionCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = module.load_registry()
        self.candidates = self.payload["candidates"]

    def test_registry_validates(self) -> None:
        self.assertEqual(module.validate(), [])

    def test_research_breadth(self) -> None:
        self.assertGreaterEqual(len(self.candidates), 40)
        self.assertEqual(
            len(self.candidates) + len(self.payload["completed_candidate_ids"]),
            self.payload["research_program_size"],
        )
        self.assertGreaterEqual(
            len({item["coverage_family"] for item in self.candidates}), 35
        )

    def test_admission_queue_is_substantive(self) -> None:
        counts = Counter(item["priority"] for item in self.candidates)
        self.assertEqual(
            counts["P0"],
            sum(item["disposition"] == "admission-pr" for item in self.candidates),
        )
        for item in self.candidates:
            if item["priority"] == "P0":
                self.assertEqual(item["disposition"], "admission-pr")
                self.assertGreaterEqual(len(item["primary_sources"]), 3)

    def test_completed_candidates_are_live_and_disjoint(self) -> None:
        live_ids, _, _ = module.live_resource_keys()
        candidate_ids = {item["id"] for item in self.candidates}
        completed = set(self.payload["completed_candidate_ids"])
        self.assertTrue(completed <= live_ids)
        self.assertFalse(completed & candidate_ids)

    def test_no_duplicate_candidate_identity(self) -> None:
        for field in ("id", "name", "official_url"):
            values = [item[field] for item in self.candidates]
            self.assertEqual(len(values), len(set(values)), field)


if __name__ == "__main__":
    unittest.main()
