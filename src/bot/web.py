"""Webhook Endpoint (architecture.md, component 1; contract C-1).

Flask app that receives Telegram webhook POSTs. This is the production entry
point under ADR-0005. It is not deployed yet: hosting checks V-2 to V-4 are
still open, so for local testing use src/bot/poll.py instead.

Run locally (for the unit tests or a tunnel):
    flask --app src.bot.web run
"""

from __future__ import annotations

import logging
import time

from flask import Flask, jsonify, request

from src.adapters import telegram
from src.bot.router import route_update

log = logging.getLogger(__name__)


def create_app(messenger=None) -> Flask:
    """Build the app. Tests pass a fake messenger; production uses Telegram."""
    app = Flask(__name__)
    app.config["MESSENGER"] = messenger

    def _messenger():
        if app.config["MESSENGER"] is None:
            app.config["MESSENGER"] = telegram.TelegramClient()
        return app.config["MESSENGER"]

    @app.post("/telegram/webhook")
    def webhook():
        started = time.monotonic()

        header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if not telegram.webhook_secret_matches(header):
            log.warning("outcome=AUTH_REJECTED")
            return jsonify(ok=False), 403

        update = request.get_json(silent=True)
        if not isinstance(update, dict) or "update_id" not in update:
            log.warning("outcome=BAD_UPDATE")
            return jsonify(ok=False), 400

        # TODO(T-30, Khumoyun; was T-27 before the task ID map, #74): skip an update_id that was already processed,
        # recorded in the same transaction as the entry (C-1).

        result = route_update(update)
        if result.chat_id is not None and result.reply:
            _messenger().send_message(result.chat_id, result.reply)

        # Outcome and timing only: no food text, no Telegram IDs (architecture.md 3, item 12).
        log.info("outcome=%s handler_ms=%d", result.outcome, (time.monotonic() - started) * 1000)
        return jsonify(ok=True), 200

    return app
