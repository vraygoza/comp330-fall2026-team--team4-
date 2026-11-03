"""Tests for the food lookup (issue #49). Data is the made-up sample file."""

import json
import tempfile
import unittest

from src.core import food_lookup
from src.core.food_lookup import FOUND, NOT_FOUND, lookup


class LookupTests(unittest.TestCase):
    def test_known_food_returns_calories(self):
        result = lookup("banana")
        self.assertEqual(result.outcome, FOUND)
        self.assertTrue(result.found)
        self.assertEqual(result.name, "Banana")
        self.assertGreater(result.kcal_per_serving, 0)

    def test_case_and_extra_spaces_are_ignored(self):
        self.assertEqual(lookup("  BaNaNa ").name, "Banana")
        self.assertEqual(lookup("pizza   slice").name, "Pizza slice")

    def test_plural_forms_match(self):
        self.assertEqual(lookup("eggs").name, "Egg")
        self.assertEqual(lookup("tacos").name, "Taco")
        self.assertEqual(lookup("pizza slices").name, "Pizza slice")

    def test_unknown_food_is_not_found_with_no_calories(self):
        result = lookup("dragonfruit")
        self.assertEqual(result.outcome, NOT_FOUND)
        self.assertFalse(result.found)
        self.assertIsNone(result.kcal_per_serving)

    def test_empty_and_bad_input_are_not_found(self):
        for value in ["", "   ", None, 42, "x" * 101]:
            with self.subTest(value=value):
                self.assertEqual(lookup(value).outcome, NOT_FOUND)

    def test_partial_word_does_not_match(self):
        # "egg roll" must not silently log as "egg" (no guessing, AC-6.2).
        self.assertEqual(lookup("egg roll").outcome, NOT_FOUND)
        self.assertEqual(lookup("pizza").outcome, NOT_FOUND)

    def test_sample_file_has_5_to_10_foods_all_positive(self):
        foods = food_lookup._load_foods()
        self.assertGreaterEqual(len(foods), 5)
        self.assertLessEqual(len(foods), 10)

    def test_bad_data_file_is_refused(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump({"foods": {"rock": {"name": "Rock", "serving": "1", "kcal_per_serving": 0}}}, handle)
        with self.assertRaises(ValueError):
            food_lookup._load_foods.__wrapped__(handle.name)


if __name__ == "__main__":
    unittest.main()
