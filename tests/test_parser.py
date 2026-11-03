"""Unit tests for the K2 message parser (issue #61).

Tests the interface from docs/reviews/a1-design-check.md Section 3
and ADR-0004 accepted message forms and limits.
"""

import unittest

from src.core.parser import (
    OUT_OF_RANGE,
    PARSED,
    UNSUPPORTED_FORMAT,
    parse_message,
)


class TestParser(unittest.TestCase):
    def parse(self, text):
        return parse_message(text)

    def assertParsed(self, text, food, quantity, unit, amount_given):
        result = self.parse(text)
        self.assertEqual(result.outcome, PARSED, text)
        self.assertEqual(result.food, food, text)
        self.assertEqual(result.item, food, text)
        self.assertEqual(result.quantity, quantity, text)
        self.assertEqual(result.unit, unit, text)
        self.assertIs(result.amount_given, amount_given, text)

    # 1. Accepted forms (ADR-0004, Section 3)

    def test_count_and_food(self):
        self.assertParsed("2 tacos", "tacos", 2.0, "count", True)

    def test_decimal_count(self):
        self.assertParsed("1.5 bananas", "bananas", 1.5, "count", True)

    def test_a_or_an_is_one(self):
        self.assertParsed("an egg", "egg", 1.0, "count", True)
        self.assertParsed("a banana", "banana", 1.0, "count", True)

    def test_food_alone_assumes_one_serving(self):
        # amount_given=False allows caller (A4) to know amount was assumed (AC-2.2, Finding 1)
        self.assertParsed("banana", "banana", 1.0, "count", False)
        self.assertParsed("taco", "taco", 1.0, "count", False)

    def test_grams(self):
        self.assertParsed("150g rice cooked", "rice cooked", 150.0, "g", True)
        self.assertParsed("150 grams rice cooked", "rice cooked", 150.0, "g", True)
        self.assertParsed("150 gram rice cooked", "rice cooked", 150.0, "g", True)
        self.assertParsed("150 g rice cooked", "rice cooked", 150.0, "g", True)

    def test_case_and_spaces(self):
        self.assertParsed("  2   TACOS ", "tacos", 2.0, "count", True)

    # 2. Limits & Ranges

    def test_limits_are_inclusive(self):
        self.assertEqual(self.parse("20 eggs").outcome, PARSED)
        self.assertEqual(self.parse("2000g rice cooked").outcome, PARSED)

    def test_out_of_range(self):
        for text in ["25 eggs", "0 eggs", "3000g rice cooked", "-1 eggs"]:
            with self.subTest(text=text):
                self.assertEqual(self.parse(text).outcome, OUT_OF_RANGE)

    # 3. Unsupported forms

    def test_unsupported_forms(self):
        for text in [
            "eggs 2",
            "1/2 banana",
            "a cup of rice",
            "2 oz chicken",
            "2 eggs and toast",
            "",
            None,
            "   ",
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.parse(text).outcome, UNSUPPORTED_FORMAT)

    def test_message_over_100_characters_is_rejected(self):
        self.assertNotEqual(self.parse("2 " + "a" * 100).outcome, PARSED)

    def test_refusals_carry_no_food_or_amount(self):
        result = self.parse("eggs 2")
        self.assertIsNone(result.food)
        self.assertIsNone(result.item)
        self.assertIsNone(result.quantity)
        self.assertIsNone(result.unit)
        self.assertIsNone(result.amount_given)


if __name__ == "__main__":
    unittest.main()
