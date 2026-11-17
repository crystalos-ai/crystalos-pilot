import unittest
from datetime import date

from screening.rules import (
    best_match,
    format_review_date,
    is_sanctions_hit,
    name_similarity,
)

WATCHLIST = ["Orrin Vexmoor", "Quillon Example Trading Ltd", "Dmitri Nullsworth"]


class ThresholdTest(unittest.TestCase):
    def test_strong_match_is_hit(self):
        self.assertTrue(is_sanctions_hit(0.90))

    def test_weak_match_is_not_hit(self):
        self.assertFalse(is_sanctions_hit(0.80))

    def test_threshold_itself_is_hit(self):
        self.assertTrue(is_sanctions_hit(0.85))


class NameMatchTest(unittest.TestCase):
    def test_accents_and_case_are_ignored(self):
        self.assertEqual(name_similarity("ORRIN VEXMÖOR", "Orrin Vexmoor"), 1.0)

    def test_close_spelling_is_hit(self):
        name, score = best_match("Orin Vexmoor", WATCHLIST)
        self.assertEqual(name, "Orrin Vexmoor")
        self.assertTrue(is_sanctions_hit(score))

    def test_unrelated_name_is_not_hit(self):
        _, score = best_match("Priya Mockridge", WATCHLIST)
        self.assertFalse(is_sanctions_hit(score))


class ReviewDateTest(unittest.TestCase):
    def test_review_date_is_iso(self):
        self.assertEqual(format_review_date(date(2026, 11, 16)), "2026-11-16")


if __name__ == "__main__":
    unittest.main()
