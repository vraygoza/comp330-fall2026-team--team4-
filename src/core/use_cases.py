"""Use Cases (architecture.md, component 3): run one request end to end.

Log Food is the Cycle 1 vertical slice (issue #50, A4):
message -> parse (K2) -> lookup (A3) -> save under the tester ID -> daily total (B2) -> reply.

Core rule: no Telegram, Flask, HTTP or SQL here. The store is passed in and only
needs register, is_registered, add_entry and entries_between (src/adapters/store.py).
Any refusal saves nothing (AC-6.1, AC-6.2).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.core.day import chicago_date_of, chicago_day_bounds, total_for_day
from src.core.food_lookup import lookup
from src.core.parser import OUT_OF_RANGE, PARSED, UNSUPPORTED_FORMAT, parse_message

NOT_REGISTERED_REPLY = "Send /start first."
FORMAT_REPLY = (
    "I can read one food per message, like:\n"
    "2 eggs\n"
    "banana"
)
RANGE_REPLY = "That amount is outside what I accept: 1 to 20 items, or 1 to 2000 grams."
GRAMS_REPLY = (
    "Gram amounts will work once real nutrition data is connected. "
    "For now, send a count, like: 2 eggs"
)
NOT_FOUND_REPLY = "I don't know \"{food}\" yet, so nothing was saved. Try another food, like: banana"


@dataclass(frozen=True)
class Outcome:
    code: str   # C-8 outcome code, safe to log (no food text, no IDs)
    reply: str


def _kcal_text(value: float) -> str:
    return f"{value:g}" if value != int(value) else f"{int(value)}"


def register(store, user_id: int, now_utc: datetime) -> Outcome:
    created = store.register(user_id, now_utc)
    return Outcome("REGISTERED" if created else "ALREADY_REGISTERED", "")


def log_food(store, user_id: int, text: str, now_utc: datetime) -> Outcome:
    if not store.is_registered(user_id):
        return Outcome("NOT_REGISTERED", NOT_REGISTERED_REPLY)

    parsed = parse_message(text)
    if parsed.outcome == UNSUPPORTED_FORMAT:
        return Outcome(UNSUPPORTED_FORMAT, FORMAT_REPLY)
    if parsed.outcome == OUT_OF_RANGE:
        return Outcome(OUT_OF_RANGE, RANGE_REPLY)
    if parsed.outcome != PARSED:
        return Outcome(UNSUPPORTED_FORMAT, FORMAT_REPLY)

    # The sample list has calories per serving only (architecture.md CC-2).
    if parsed.unit == "g":
        return Outcome("NEEDS_GRAMS", GRAMS_REPLY)

    found = lookup(parsed.food)
    if not found.found:
        return Outcome("NOT_FOUND", NOT_FOUND_REPLY.format(food=parsed.food))

    kcal = parsed.quantity * found.kcal_per_serving
    store.add_entry(
        user_id,
        food_text=parsed.food,
        matched_description=found.name,
        quantity=parsed.quantity,
        unit="count" if parsed.amount_given else "default",
        kcal=kcal,
        source="sample",
        now_utc=now_utc,
    )

    today = chicago_date_of(now_utc)
    start, end = chicago_day_bounds(today)
    total = total_for_day(store.entries_between(user_id, start, end), today)

    amount = f"{parsed.quantity:g} x {found.name} ({found.serving} each)"
    if not parsed.amount_given:
        amount = f"1 x {found.name} ({found.serving}, assumed because no amount was given)"
    reply = f"Logged {amount} = {_kcal_text(kcal)} kcal.\nToday's total: {_kcal_text(total)} kcal."
    return Outcome("LOGGED", reply)
