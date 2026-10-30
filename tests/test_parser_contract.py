"""Contract tests for the K2 parser (issue #61), written before the parser exists.

They check the interface agreed in docs/reviews/a1-design-check.md, Section 3, and
the accepted forms in ADR-0004. Until src/core/parser.py is merged, every test here
is skipped, so CI stays green. When K2 merges, they run automatically.

S2 (issue #53). Run: python -m unittest discover -s tests -t .
"""

import importlib.util
import unittest

PARSER_READY = importlib.util.find_spec("src.core.parser") is not None


@unittest.skipUnless(PARSER_READY, "src/core/parser.py not merged yet (K2, #61)")
class ParserContractTests(unittest.TestCase):
    def parse(self, text):
        from src.core.parser import parse_message
        return parse_message(text)

    def assertParsed(self, text, food, quantity, unit, amount_given):
        result = self.parse(text)
        self.assertEqual(result.outcome, "PARSED", text)
        self.assertEqual(result.food, food, text)
        self.assertEqual(result.quantity, quantity, text)
        self.assertEqual(result.unit, unit, text)
        self.assertIs(result.amount_given, amount_given, text)

    # Accepted forms (ADR-0004, Section 3 examples)

    def test_count_and_food(self):
        self.assertParsed("2 tacos", "tacos", 2.0, "count", True)

    def test_decimal_count(self):
        self.assertParsed("1.5 bananas", "bananas", 1.5, "count", True)

    def test_a_or_an_is_one(self):
        self.assertParsed("an egg", "egg", 1.0, "count", True)
        self.assertParsed("a banana", "banana", 1.0, "count", True)

    def test_food_alone_assumes_one_serving(self):
        # amount_given=False is how A4 knows to say the amount was assumed (AC-2.2).
        self.assertParsed("banana", "banana", 1.0, "count", False)

    def test_grams(self):
        self.assertParsed("150g rice cooked", "rice cooked", 150.0, "g", True)
        self.assertParsed("150 grams rice cooked", "rice cooked", 150.0, "g", True)

    def test_case_and_spaces(self):
        self.assertParsed("  2   TACOS ", "tacos", 2.0, "count", True)

    # Rejected forms save nothing (AC-2.4)

    def test_unsupported_forms(self):
        for text in ["eggs 2", "1/2 banana", "a cup of rice", "2 oz chicken", "2 eggs and toast", ""]:
            with self.subTest(text=text):
                self.assertEqual(self.parse(text).outcome, "UNSUPPORTED_FORMAT")

    def test_out_of_range(self):
        for text in ["25 eggs", "0 eggs", "3000g rice cooked"]:
            with self.subTest(text=text):
                self.assertEqual(self.parse(text).outcome, "OUT_OF_RANGE")

    def test_limits_are_inclusive(self):
        self.assertEqual(self.parse("20 eggs").outcome, "PARSED")
        self.assertEqual(self.parse("2000g rice cooked").outcome, "PARSED")

    def test_message_over_100_characters_is_rejected(self):
        self.assertNotEqual(self.parse("2 " + "a" * 100).outcome, "PARSED")

    def test_refusals_carry_no_food_or_amount(self):
        result = self.parse("eggs 2")
        self.assertIsNone(result.food)
        self.assertIsNone(result.quantity)


if __name__ == "__main__":
    unittest.main()
