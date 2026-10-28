"""Tests for the Webhook Endpoint, contract C-1 (issue #48)."""

import os
import unittest
from unittest import mock

from src.bot.router import WELCOME
from src.bot.web import create_app

SECRET = "test-secret-not-real"


class FakeMessenger:
    def __init__(self):
        self.sent = []

    def send_message(self, chat_id, text):
        self.sent.append((chat_id, text))
        return True


def start_update():
    return {
        "update_id": 1,
        "message": {"chat": {"id": 111, "type": "private"}, "from": {"id": 111}, "text": "/start"},
    }


@mock.patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": SECRET})
class WebhookTests(unittest.TestCase):
    def setUp(self):
        self.messenger = FakeMessenger()
        self.client = create_app(self.messenger).test_client()

    def post(self, body, secret=SECRET):
        headers = {"X-Telegram-Bot-Api-Secret-Token": secret} if secret else {}
        return self.client.post("/telegram/webhook", json=body, headers=headers)

    def test_valid_start_replies_once(self):
        response = self.post(start_update())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.messenger.sent, [(111, WELCOME)])

    def test_missing_secret_is_rejected_and_nothing_runs(self):
        response = self.post(start_update(), secret=None)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.messenger.sent, [])

    def test_wrong_secret_is_rejected(self):
        self.assertEqual(self.post(start_update(), secret="wrong").status_code, 403)
        self.assertEqual(self.messenger.sent, [])

    def test_body_without_update_id_is_bad_request(self):
        self.assertEqual(self.post({"message": {}}).status_code, 400)

    def test_update_without_message_sends_nothing(self):
        response = self.post({"update_id": 2, "edited_message": {}})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.messenger.sent, [])


class WebhookWithoutSecretConfigured(unittest.TestCase):
    @mock.patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": ""})
    def test_unset_secret_rejects_everything(self):
        client = create_app(FakeMessenger()).test_client()
        response = client.post(
            "/telegram/webhook",
            json=start_update(),
            headers={"X-Telegram-Bot-Api-Secret-Token": ""},
        )
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
