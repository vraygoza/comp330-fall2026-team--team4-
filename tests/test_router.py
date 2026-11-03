"""Tests for the Command Router (issue #48). Run: python -m unittest discover -s tests -t ."""

import unittest

from src.bot.router import DIRECT_ONLY, FORMAT_HINT, WELCOME, route_update


def private_update(text, update_id=1, user_id=111):
    message = {
        "message_id": 5,
        "chat": {"id": user_id, "type": "private"},
        "from": {"id": user_id, "is_bot": False},
        "date": 1761500000,
    }
    if text is not None:
        message["text"] = text
    return {"update_id": update_id, "message": message}


class RouterTests(unittest.TestCase):
    def test_start_replies_with_welcome(self):
        result = route_update(private_update("/start"))
        self.assertEqual(result.outcome, "STARTED")
        self.assertEqual(result.chat_id, 111)
        self.assertEqual(result.reply, WELCOME)

    def test_start_is_case_and_space_tolerant(self):
        self.assertEqual(route_update(private_update("  /START  ")).outcome, "STARTED")

    def test_start_with_bot_username(self):
        self.assertEqual(route_update(private_update("/start@team4_test_bot")).outcome, "STARTED")

    def test_group_chat_gets_direct_only_reply(self):
        update = private_update("/start")
        update["message"]["chat"]["type"] = "group"
        result = route_update(update)
        self.assertEqual(result.outcome, "NOT_PRIVATE")
        self.assertEqual(result.reply, DIRECT_ONLY)

    def test_message_without_text_gets_format_hint(self):
        result = route_update(private_update(None))  # photo or sticker
        self.assertEqual(result.outcome, "UNSUPPORTED_FORMAT")
        self.assertEqual(result.reply, FORMAT_HINT)

    def test_update_without_message_is_ignored(self):
        result = route_update({"update_id": 9, "edited_message": {}})
        self.assertEqual(result.outcome, "IGNORED")
        self.assertIsNone(result.chat_id)

    def test_food_text_is_not_logged_yet(self):
        # Food logging arrives with the integration PR (issue #50).
        self.assertEqual(route_update(private_update("2 eggs")).outcome, "NOT_READY")


if __name__ == "__main__":
    unittest.main()
