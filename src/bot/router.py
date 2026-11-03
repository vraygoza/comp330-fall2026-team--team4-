"""Command Router (architecture.md, component 2; contracts C-1 and C-2).

Turns one Telegram Update into one reply. It does not send anything and does
not know about Flask or HTTP, so the webhook (web.py) and the local runner
(poll.py) share the same behavior.

Skeleton scope (issue #48): /start and the C-1 filtering rules. Food logging
is wired in by the integration PR (issue #50).
"""

from __future__ import annotations

from dataclasses import dataclass

WELCOME = (
    "Welcome to the Team 4 calorie tracker test.\n"
    "Send one food per message, for example: 2 eggs\n"
    "Send /today to see what you logged today."
)
DIRECT_ONLY = "Please message me directly."
FORMAT_HINT = (
    "Send one food per message, like: 2 eggs, or: banana\n"
    "Send /start to see the instructions again."
)
NOT_READY = "Food logging is not switched on yet. Send /start to see the instructions."


@dataclass(frozen=True)
class RouteResult:
    outcome: str                # C-8 style outcome code, safe to log
    chat_id: int | None = None  # None means: do not reply
    reply: str | None = None


def route_update(update: dict) -> RouteResult:
    """Decide the reply for one Update. Reads only the C-1 fields."""
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
