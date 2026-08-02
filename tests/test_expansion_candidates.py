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
        self.active = [
            item
            for item in self.candidates
            if item["disposition"] in module.ACTIVE_DISPOSITIONS
        ]
        self.terminal = [
            item
            for item in self.candidates
            if item["disposition"] in module.TERMINAL_DISPOSITIONS
        ]

    def test_registry_validates(self) -> None:
        self.assertEqual(module.validate(), [])

    def test_research_breadth_and_conservation(self) -> None:
        self.assertGreaterEqual(self.payload["research_program_size"], 60)
        self.assertEqual(
            len(self.active)
            + len(self.payload["completed_candidate_ids"])
            + len(self.terminal),
            self.payload["research_program_size"],
        )
        family_count = len({item["coverage_family"] for item in self.active})
        minimum_family_count = (
            max(1, (4 * len(self.active) + 4) // 5) if self.active else 0
        )
        self.assertGreaterEqual(family_count, minimum_family_count)

    def test_admission_queue_rules(self) -> None:
        counts = Counter(item["priority"] for item in self.active)
        self.assertEqual(
            counts.get("P0", 0),
            sum(item["disposition"] == "admission-pr" for item in self.active),
        )
        for item in self.active:
            if item["priority"] == "P0":
                self.assertEqual(item["disposition"], "admission-pr")
                self.assertGreaterEqual(len(item["primary_sources"]), 3)
            self.assertTrue(item.get("review_due_on"))
            self.assertTrue(item["next_step"].strip())

    def test_terminal_disposition_rules(self) -> None:
        live_ids, _, _ = module.live_resource_keys()
        for item in self.terminal:
            self.assertNotEqual(item["priority"], "P0")
            self.assertNotEqual(item["disposition"], "admission-pr")
            if item["disposition"] == "rejected-represented-by":
                represented = item["represented_by_resource_ids"]
                self.assertTrue(represented)
                self.assertTrue(set(represented) <= live_ids)
            if item["disposition"] == "deferred-family-review":
                self.assertTrue(item.get("scheduled_review") or item.get("deferred_family_id"))

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
