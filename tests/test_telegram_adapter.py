"""Tests for the Telegram Adapter (issue #48): token handling and failure paths."""

import io
import os
import unittest
import urllib.error
from unittest import mock

from src.adapters import telegram

FAKE_TOKEN = "123456:FAKE-TOKEN-FOR-TESTS"


class TelegramAdapterTests(unittest.TestCase):
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_missing_token_gives_clear_error(self):
        with self.assertRaises(telegram.TelegramConfigError):
            telegram.TelegramClient()

    def test_failed_send_returns_false_and_never_logs_token(self):
        client = telegram.TelegramClient(token=FAKE_TOKEN)
        error = urllib.error.HTTPError(
            "https://api.telegram.org/bot" + FAKE_TOKEN + "/sendMessage",
            400, "Bad Request", {}, io.BytesIO(b'{"ok":false,"description":"chat not found"}'),
        )
        with mock.patch("urllib.request.urlopen", side_effect=error):
            with self.assertLogs("src.adapters.telegram", level="WARNING") as logs:
                self.assertFalse(client.send_message(111, "hi"))
        self.assertNotIn(FAKE_TOKEN, "\n".join(logs.output))
        self.assertIn("REPLY_FAILED", "\n".join(logs.output))

    def test_network_error_returns_false(self):
        client = telegram.TelegramClient(token=FAKE_TOKEN)
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
            with self.assertLogs("src.adapters.telegram", level="WARNING"):
                self.assertFalse(client.send_message(111, "hi"))

    @mock.patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": "abc"})
    def test_secret_check(self):
        self.assertTrue(telegram.webhook_secret_matches("abc"))
        self.assertFalse(telegram.webhook_secret_matches("abd"))
        self.assertFalse(telegram.webhook_secret_matches(None))


if __name__ == "__main__":
    unittest.main()
