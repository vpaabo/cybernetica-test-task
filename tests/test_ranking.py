import unittest
from ranking.models import Candidate, RankingConfig
from ranking.engine import run_phase1
from ranking.phase3 import run_phase3


class TestRankingPhases(unittest.TestCase):

    # -------------------------------------------------
    # Utility
    # -------------------------------------------------
    def make_basic_candidates(self):
        return [
            Candidate("Alice", "T1", 10),
            Candidate("Bob", "T2", 8),
            Candidate("Charlie", "T3", 5),
            Candidate("David", "T4", 0),
        ]

    # -------------------------------------------------
    # PHASE 1 TESTS
    # -------------------------------------------------
    def test_phase1_separates_zero_votes(self):
        ranked, tie_groups, zero_votes = run_phase1(self.make_basic_candidates())

        self.assertEqual([c.name for c in ranked], ["Alice", "Bob", "Charlie"])
        self.assertEqual([c.name for c in zero_votes], ["David"])
        self.assertEqual(tie_groups, [])

    def test_phase1_detects_ties(self):
        candidates = [
            Candidate("A", "T1", 10),
            Candidate("B", "T2", 10),
            Candidate("C", "T3", 5),
        ]

        ranked, tie_groups, _ = run_phase1(candidates)

        self.assertEqual([c.name for c in ranked], ["A", "B", "C"])
        self.assertEqual(tie_groups, [(0, 1)])

    def test_phase1_all_zero_votes(self):
        candidates = [
            Candidate("A", "T1", 0),
            Candidate("B", "T2", 0),
        ]

        ranked, tie_groups, zero_votes = run_phase1(candidates)

        self.assertEqual(ranked, [])
        self.assertEqual(len(zero_votes), 2)
        self.assertEqual(tie_groups, [])

    # -------------------------------------------------
    # PHASE 3 CORE BEHAVIOR
    # -------------------------------------------------
    def test_basic_election_flow(self):
        candidates = self.make_basic_candidates()
        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=4, open_position_count=2)

        result = run_phase3(ranked, config)

        self.assertEqual(len(result.elected), 2)
        self.assertTrue(all(c.status == "ELECTED" for c in result.elected))
        self.assertTrue(all(c.status == "ALTERNATE" for c in result.alternates))

    def test_no_more_elected_than_seats(self):
        candidates = self.make_basic_candidates()
        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=4, open_position_count=1)

        result = run_phase3(ranked, config)

        self.assertLessEqual(len(result.elected), 1)

    def test_no_duplicate_elections(self):
        candidates = self.make_basic_candidates()
        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=4, open_position_count=3)

        result = run_phase3(ranked, config)

        names = [c.name for c in result.elected]
        self.assertEqual(len(names), len(set(names)))

    def test_zero_votes_never_elected(self):
        candidates = self.make_basic_candidates()
        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=4, open_position_count=3)

        result = run_phase3(ranked, config)

        self.assertNotIn("David", [c.name for c in result.elected])

    # -------------------------------------------------
    # EDGE CASES
    # -------------------------------------------------
    def test_no_candidates(self):
        ranked, _, _ = run_phase1([])
        config = RankingConfig(team_seat_count=0, open_position_count=3)
        result = run_phase3(ranked, config)

        self.assertEqual(result.elected, [])
        self.assertEqual(result.alternates, [])

    def test_all_same_team(self):
        candidates = [
            Candidate("A", "T1", 10),
            Candidate("B", "T1", 9),
            Candidate("C", "T1", 8),
        ]

        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=1, open_position_count=2)

        result = run_phase3(ranked, config)

        self.assertEqual(len(result.elected), 2)

    def test_zero_seats(self):
        candidates = self.make_basic_candidates()
        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=4, open_position_count=0)

        result = run_phase3(ranked, config)

        self.assertEqual(len(result.elected), 0)
        self.assertEqual(len(result.alternates), len(ranked))

    def test_more_seats_than_candidates(self):
        candidates = [
            Candidate("A", "T1", 5),
            Candidate("B", "T2", 4),
        ]

        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=2, open_position_count=5)

        result = run_phase3(ranked, config)

        self.assertEqual(len(result.elected), 2)
        self.assertEqual(len(result.alternates), 0)

    def test_large_tie_group(self):
        candidates = [
            Candidate(f"C{i}", f"T{i}", 100) for i in range(10)
        ]

        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=10, open_position_count=3)

        result = run_phase3(ranked, config)

        self.assertEqual(len(result.elected), 3)
        self.assertEqual(
            [c.name for c in result.elected],
            ["C0", "C1", "C2"]
        )

    # -------------------------------------------------
    # STATUS INVARIANTS
    # -------------------------------------------------
    def test_status_consistency(self):
        candidates = self.make_basic_candidates()
        ranked, _, _ = run_phase1(candidates)
        config = RankingConfig(team_seat_count=4, open_position_count=2)

        result = run_phase3(ranked, config)

        for c in result.elected:
            self.assertEqual(c.status, "ELECTED")

        for c in result.alternates:
            self.assertEqual(c.status, "ALTERNATE")

        elected_names = {c.name for c in result.elected}
        alternate_names = {c.name for c in result.alternates}

        self.assertTrue(elected_names.isdisjoint(alternate_names))

    # -------------------------------------------------
    # NEGATIVE INPUT
    # -------------------------------------------------
    def test_negative_votes_raises(self):
        with self.assertRaises(ValueError):
            Candidate("Invalid", "T1", -1)


if __name__ == "__main__":
    unittest.main()