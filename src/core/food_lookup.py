"""Food lookup for the Cycle 1 slice (issue #49).

Given a food name, return its calories per serving from a small made-up list,
or a clear unknown-food result. Nothing guesses a value (AC-6.2).

This stands in for the Food Resolver (architecture.md, component 5) until live
check V-1 confirms how USDA FoodData Central data behaves. The integration code
calls only lookup(), so the FDC-backed resolver can replace this file without
changing its callers.

Core rule: imports nothing from src/bot, src/adapters, Flask, sqlite3 or urllib.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

SAMPLE_FILE = Path(__file__).with_name("sample_foods.json")
MAX_FOOD_LENGTH = 100  # ADR-0004 message limit

FOUND = "FOUND"
NOT_FOUND = "NOT_FOUND"  # C-8 outcome code


@dataclass(frozen=True)
class LookupResult:
    """Example: lookup("eggs") -> LookupResult("FOUND", "Egg", "1 large egg", 70)."""

    outcome: str
    name: str | None = None
    serving: str | None = None
    kcal_per_serving: float | None = None

    @property
    def found(self) -> bool:
        return self.outcome == FOUND


@lru_cache(maxsize=1)
def _load_foods(path: str = str(SAMPLE_FILE)) -> dict:
    with open(path, encoding="utf-8") as handle:
        foods = json.load(handle)["foods"]
    for key, item in foods.items():
        # Refuse to start with a broken entry instead of saving a bad value later.
        if not isinstance(item.get("kcal_per_serving"), (int, float)) or item["kcal_per_serving"] <= 0:
            raise ValueError(f"sample food {key!r} has no positive kcal_per_serving")
    return foods


def _normalize(food: str) -> str:
    return " ".join(food.lower().split())


def _candidates(key: str) -> list[str]:
    """The name as typed, then simple singular forms: eggs -> egg, tomatoes -> tomato."""
    forms = [key]
    if key.endswith("s"):
        forms.append(key[:-1])
    if key.endswith("es"):
        forms.append(key[:-2])
    return forms


def lookup(food: str) -> LookupResult:
    """Return calories per serving for a known food, or a NOT_FOUND result."""
    if not isinstance(food, str):
        return LookupResult(NOT_FOUND)
    key = _normalize(food)
    if not key or len(key) > MAX_FOOD_LENGTH:
        return LookupResult(NOT_FOUND)

    foods = _load_foods()
    for candidate in _candidates(key):
        item = foods.get(candidate)
        if item:
            return LookupResult(FOUND, item["name"], item["serving"], float(item["kcal_per_serving"]))
    return LookupResult(NOT_FOUND)
