"""Command Router (architecture.md, component 2; contracts C-1 and C-2).

Turns one Telegram Update into one reply. It does not send anything and does
not know about Flask or HTTP, so the webhook (web.py) and the local runner
(poll.py) share the same behavior.

Skeleton (issue #48): /start and the C-1 filtering rules.
Integration (issue #50, A4): /start registers the tester, and any other text runs
the Log Food use case. The store is passed in, so tests use a temporary database.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from src.core import use_cases

log = logging.getLogger(__name__)

WELCOME = (
    "Welcome to the Team 4 calorie tracker test.\n"
    "Send one food per message, for example: 2 eggs\n"
    "Calories come from a small sample list during this test."
)
DIRECT_ONLY = "Please message me directly."
FORMAT_HINT = (
    "Send one food per message, like: 2 eggs, or: banana\n"
    "Send /start to see the instructions again."
)
NOT_READY = "Food logging is not switched on yet. Send /start to see the instructions."
ERROR_REPLY = "Something went wrong. Please try again later."


@dataclass(frozen=True)
class RouteResult:
    outcome: str                # C-8 style outcome code, safe to log
    chat_id: int | None = None  # None means: do not reply
    reply: str | None = None


def route_update(update: dict, store=None, now_utc=None) -> RouteResult:
    """Decide the reply for one Update. Reads only the C-1 fields."""
    try:
        message = update.get("message")
        if not isinstance(message, dict):
            return RouteResult("IGNORED")  # edited message, channel post, other

        chat = message.get("chat") or {}
        chat_id = chat.get("id")
        if chat_id is None:
            return RouteResult("BAD_UPDATE")

        if chat.get("type") != "private":
            return RouteResult("NOT_PRIVATE", chat_id, DIRECT_ONLY)

        text = message.get("text")
        if not isinstance(text, str) or not text.strip():
            return RouteResult("UNSUPPORTED_FORMAT", chat_id, FORMAT_HINT)

        command = text.strip().split()[0].lower()
        if command == "/start" or command.startswith("/start@"):
            return RouteResult("STARTED", chat_id, WELCOME)

        return RouteResult("NOT_READY", chat_id, NOT_READY)
    except Exception:
        log.exception("Unexpected error routing update")
        chat_id = None
        try:
            chat_id = ((update.get("message") or {}).get("chat") or {}).get("id")
        except Exception:
            pass
        return RouteResult("INTERNAL_ERROR", chat_id, ERROR_REPLY)
