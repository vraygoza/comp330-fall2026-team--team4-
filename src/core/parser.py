"""Message Parser for the Cycle 1 slice (component 4; issue #61, K2).

Turns a user's food message into food words, quantity, unit, and whether an
amount was explicitly given, or returns an outcome code (PARSED,
UNSUPPORTED_FORMAT, OUT_OF_RANGE) per ADR-0004 and docs/reviews/a1-design-check.md.

Core rule: imports nothing from src/bot, src/adapters, Flask, sqlite3, or urllib.
Parser does not import resolver/lookup; reply generation belongs to use cases (A4).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Limits from ADR-0004 and api-contracts.md C-1
MAX_MESSAGE_CHARS = 100
MAX_COUNT = 20
MAX_GRAMS = 2000

# Outcome codes (C-8)
PARSED = "PARSED"
UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
OUT_OF_RANGE = "OUT_OF_RANGE"

# Units not supported in Cycle 1 (ADR-0004)
UNSUPPORTED_UNITS = {
    "cup", "cups", "oz", "ounce", "ounces", "lb", "lbs", "pound", "pounds",
    "tbsp", "tablespoon", "tablespoons", "tsp", "teaspoon", "teaspoons",
    "ml", "l", "liter", "liters", "slice", "slices", "piece", "pieces",
    "bowl", "bowls", "handful", "plate", "kg",
}

_GRAMS = re.compile(r"^(-?\d+(?:\.\d+)?)\s*(?:g|grams?)\s+(.+)$", re.IGNORECASE)
_COUNT = re.compile(r"^(-?\d+(?:\.\d+)?)\s+(.+)$", re.IGNORECASE)
_ARTICLE = re.compile(r"^(?:a|an)\s+(.+)$", re.IGNORECASE)


@dataclass(frozen=True)
class ParseResult:
    """Outcome and parsed details for a food message.

    Fields agreed in docs/reviews/a1-design-check.md Section 3:
      outcome: "PARSED", "UNSUPPORTED_FORMAT", or "OUT_OF_RANGE"
      food: the food name (singular/plural as typed, normalized to lowercase)
      quantity: float amount (e.g. 2.0, 1.5, 150.0) or None
      unit: "count" or "g" (None unless PARSED)
      amount_given: True if typed, False if default serving was assumed
    """

    outcome: str
    food: str | None = None
    quantity: float | None = None
    unit: str | None = None
    amount_given: bool | None = None

    @property
    def item(self) -> str | None:
        """Alias for food to satisfy task description ('item tacos and quantity 2')."""
        return self.food


def _clean_text(text: str) -> str | None:
    if not isinstance(text, str):
        return None
    raw = text.strip()
    if not raw or len(raw) > MAX_MESSAGE_CHARS:
        return None
    if raw.startswith("/"):
        return None
    if "/" in raw:  # fractions like 1/2 banana
        return None
    return " ".join(raw.lower().split())


def _check_food_words(food: str) -> str | None:
    candidate = " ".join(food.strip().split())
    if not candidate:
        return None
    # No digits in the food part (e.g. 'eggs 2')
    if any(char.isdigit() for char in candidate):
        return None
    # Food words use letters, spaces, apostrophes and hyphens only
    if not re.fullmatch(r"[a-z][a-z \-']*", candidate):
        return None
    words = candidate.split()
    if not words or words[0] in UNSUPPORTED_UNITS:
        return None
    # 'a cup of rice' -> words[:2] contains 'of'
    if "of" in words[:2]:
        return None
    # Multiple foods like '2 eggs and toast' are not supported
    if "and" in words:
        return None
    return candidate


def parse_message(text: str) -> ParseResult:
    """Turn a message like '2 tacos' into ParseResult per ADR-0004.

    Examples:
      parse_message("2 tacos")          -> ParseResult("PARSED", "tacos", 2.0, "count", True)
      parse_message("an egg")           -> ParseResult("PARSED", "egg", 1.0, "count", True)
      parse_message("banana")           -> ParseResult("PARSED", "banana", 1.0, "count", False)
      parse_message("150g rice cooked") -> ParseResult("PARSED", "rice cooked", 150.0, "g", True)
      parse_message("eggs 2")           -> ParseResult("UNSUPPORTED_FORMAT", None, None, None, None)
      parse_message("25 eggs")          -> ParseResult("OUT_OF_RANGE", None, None, None, None)
    """
    cleaned = _clean_text(text)
    if cleaned is None:
        return ParseResult(UNSUPPORTED_FORMAT)

    # 1. Gram input: <number>g <food> or <number> grams <food>
    m_grams = _GRAMS.match(cleaned)
    if m_grams:
        qty = float(m_grams.group(1))
        if qty <= 0 or qty > MAX_GRAMS:
            return ParseResult(OUT_OF_RANGE)
        food = _check_food_words(m_grams.group(2))
        if food is None:
            return ParseResult(UNSUPPORTED_FORMAT)
        return ParseResult(PARSED, food, qty, "g", True)

    # 2. Count input: <number> <food>
    m_count = _COUNT.match(cleaned)
    if m_count:
        qty = float(m_count.group(1))
        if qty <= 0 or qty > MAX_COUNT:
            return ParseResult(OUT_OF_RANGE)
        food = _check_food_words(m_count.group(2))
        if food is None:
            return ParseResult(UNSUPPORTED_FORMAT)
        return ParseResult(PARSED, food, qty, "count", True)

    # 3. Article input: a <food> or an <food>
    m_art = _ARTICLE.match(cleaned)
    if m_art:
        food = _check_food_words(m_art.group(1))
        if food is None:
            return ParseResult(UNSUPPORTED_FORMAT)
        return ParseResult(PARSED, food, 1.0, "count", True)

    # 4. Food alone: <food>
    food = _check_food_words(cleaned)
    if food is None:
        return ParseResult(UNSUPPORTED_FORMAT)
    return ParseResult(PARSED, food, 1.0, "count", False)
