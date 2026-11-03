"""Telegram Adapter (architecture.md, component 7; contract C-3).

The only module that holds the bot token and the webhook secret. Both are read
from environment variables, never from a file in the repo (NFR-3).

Uses the Python standard library only (ADR-0005: a thin adapter, no bot library).
"""

from __future__ import annotations

import hmac
import json
import logging
import os
import urllib.error
import urllib.request

log = logging.getLogger(__name__)

API_BASE = "https://api.telegram.org"
REQUEST_TIMEOUT_SECONDS = 10


class TelegramConfigError(RuntimeError):
    """Raised when a required environment variable is missing."""


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise TelegramConfigError(
            f"{name} is not set. Copy .env.example to .env and fill it in."
        )
    return value


def webhook_secret_matches(header_value: str | None) -> bool:
    """C-1: compare the X-Telegram-Bot-Api-Secret-Token header to our secret.

    Returns False when the secret is not configured, so a missing setting
    rejects every request instead of accepting every request.
    """
    expected = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "")
    if not expected or not header_value:
        return False
    return hmac.compare_digest(header_value.encode(), expected.encode())


class TelegramClient:
    """Calls the Bot API. Holds the token; never logs it."""

    def __init__(self, token: str | None = None):
        self._token = token or _required_env("TELEGRAM_BOT_TOKEN")

    def _call(self, method: str, payload: dict, timeout: float = REQUEST_TIMEOUT_SECONDS) -> dict:
        url = f"{API_BASE}/bot{self._token}/{method}"
        data = json.dumps(payload).encode()
        request = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as err:
            # Log the status only. The URL contains the token, so never log it.
            body = {}
            try:
                body = json.loads(err.read().decode())
            except (ValueError, OSError):
                pass
            log.warning("telegram_call_failed method=%s status=%s", method, err.code)
            return {"ok": False, "error_code": err.code, "description": body.get("description", "")}
        except (urllib.error.URLError, TimeoutError) as err:
            log.warning("telegram_call_failed method=%s error=%s", method, type(err).__name__)
            return {"ok": False, "error_code": None, "description": "network error"}

    def send_message(self, chat_id: int, text: str) -> bool:
        """C-3 sendMessage: plain text, no parse mode. No retry loop."""
        result = self._call("sendMessage", {"chat_id": chat_id, "text": text})
        if not result.get("ok"):
            log.warning("outcome=REPLY_FAILED error_code=%s", result.get("error_code"))
            return False
        return True

    def get_updates(self, offset: int | None, timeout: int = 30) -> dict:
        """Local development only (see src/bot/poll.py). Not used on the host."""
        payload = {"timeout": timeout, "allowed_updates": ["message"]}
        if offset is not None:
            payload["offset"] = offset
        return self._call("getUpdates", payload, timeout=timeout + REQUEST_TIMEOUT_SECONDS)
