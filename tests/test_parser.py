"""Unit and contract tests for the K2 parser (issue #61).

Tests the interface from docs/reviews/a1-design-check.md Section 3,
ADR-0004 accepted message forms and limits, and reply handling for:
- turns '2 tacos' into item and quantity
- missing quantity asks how many
- unknown food replies with friendly message
"""

import unittest

from src.core.parser import (
    OUT_OF_RANGE,
    PARSED,
    UNSUPPORTED_FORMAT,
    handle_food_message,
    parse_and_reply,
    parse_message,
)


class TestParserContract(unittest.TestCase):
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

    # 1. Accepted forms

    def test_count_and_food(self):
        self.assertParsed("2 tacos", "tacos", 2.0, "count", True)

    def test_decimal_count(self):
        self.assertParsed("1.5 bananas", "bananas", 1.5, "count", True)

    def test_a_or_an_is_one(self):
        self.assertParsed("an egg", "egg", 1.0, "count", True)
        self.assertParsed("a banana", "banana", 1.0, "count", True)

    def test_food_alone_assumes_one_serving(self):
        # amount_given=False allows caller to know amount was assumed (AC-2.2)
        self.assertParsed("banana", "banana", 1.0, "count", False)

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


class TestFoodMessageReplies(unittest.TestCase):
    """Tests the three cases required by Task K2."""

    def test_step_1_turns_2_tacos_into_item_and_quantity(self):
        result = parse_message("2 tacos")
        self.assertEqual(result.item, "tacos")
        self.assertEqual(result.quantity, 2.0)
        self.assertEqual(handle_food_message("2 tacos"), "2 tacos")

    def test_step_2_missing_quantity_replies_how_many(self):
        reply = handle_food_message("taco")
        self.assertEqual(reply, "How many taco?")

        reply_banana = handle_food_message("banana")
        self.assertEqual(reply_banana, "How many banana?")

    def test_step_3_unknown_food_replies_friendly_message(self):
        # 'dragonfruit' is not in sample_foods.json
        reply = handle_food_message("2 dragonfruit")
        self.assertIn("I don't know that food", reply)
        self.assertIn("dragonfruit", reply)

    def test_parse_and_reply_alias(self):
        self.assertEqual(parse_and_reply("2 tacos"), "2 tacos")


if __name__ == "__main__":
    unittest.main()

