"""INV-01 spike: parsing, food resolution, quantity conversion, storage and the Chicago day.

Throwaway investigation code, not the Cycle 1 implementation. It exists to test the
rules proposed in docs/architecture/investigations/inv-01-lookup-storage.md before the
team accepts them as ADRs. Standard library only.

AI-assisted (Claude). Human review: Adiya (pending), second reviewer: TODO.
"""
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

CHICAGO = ZoneInfo("America/Chicago")

# Limits proposed for Cycle 1 (see api-contracts.md, C-1).
MAX_MESSAGE_CHARS = 100
MAX_COUNT = 20
MAX_GRAMS = 2000
# Two matched candidates whose kcal per 100 g differ by more than this ratio are
# treated as ambiguous (for example raw rice versus cooked rice).
AMBIGUITY_RATIO = 1.25
# Energy nutrients in order of preference. 1008 is "Energy (kcal)". Some Foundation
# records report only the Atwater variants (2047 general, 2048 specific).
ENERGY_NUTRIENT_IDS = (1008, 2047, 2048)
PORTION_PREFERENCE = ("medium", "large", "serving")

UNSUPPORTED_UNITS = {
    "cup", "cups", "oz", "ounce", "ounces", "lb", "lbs", "pound", "pounds",
    "tbsp", "tablespoon", "tablespoons", "tsp", "teaspoon", "teaspoons",
    "ml", "l", "liter", "liters", "slice", "slices", "piece", "pieces",
    "bowl", "bowls", "handful", "plate", "kg",
}


# ---------------------------------------------------------------- outcomes
class Outcome:
    LOGGED = "LOGGED"
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    NOT_FOUND = "NOT_FOUND"
    AMBIGUOUS = "AMBIGUOUS"
    NEEDS_GRAMS = "NEEDS_GRAMS"
    NO_ENERGY_VALUE = "NO_ENERGY_VALUE"
    LOOKUP_FAILED = "LOOKUP_FAILED"


# ---------------------------------------------------------------- parsing
@dataclass
class Parsed:
    food: str
    quantity: float
    unit: str  # "count", "g", or "default"


_GRAMS = re.compile(r"^(\d+(?:\.\d+)?)\s*(?:g|gram|grams)\s+(.+)$")
_COUNT = re.compile(r"^(\d+(?:\.\d+)?)\s+(.+)$")
_ARTICLE = re.compile(r"^(?:a|an)\s+(.+)$")


def parse_message(text: str) -> tuple[str, Parsed | None]:
    """Return (outcome, parsed). Outcome is "OK" when parsing succeeded."""
    t = " ".join(text.strip().lower().split())
    if not t or len(t) > MAX_MESSAGE_CHARS or t.startswith("/"):
        return Outcome.UNSUPPORTED_FORMAT, None
    # Fractions ("1/2 banana") and trailing amounts ("eggs 2") are not accepted:
    # the only digits allowed are the leading amount.
    if "/" in t or re.search(r"\d", _food_part(t)):
        return Outcome.UNSUPPORTED_FORMAT, None
    m = _GRAMS.match(t)
    if m:
        qty, food = float(m.group(1)), m.group(2)
        if qty <= 0 or qty > MAX_GRAMS:
            return Outcome.OUT_OF_RANGE, None
        return _check_food(food, qty, "g")
    m = _COUNT.match(t)
    if m:
        qty, food = float(m.group(1)), m.group(2)
        if qty <= 0 or qty > MAX_COUNT:
            return Outcome.OUT_OF_RANGE, None
        return _check_food(food, qty, "count")
    m = _ARTICLE.match(t)
    if m:
        return _check_food(m.group(1), 1.0, "count")
    return _check_food(t, 1.0, "default")


def _food_part(t: str) -> str:
    m = _GRAMS.match(t) or _COUNT.match(t)
    return m.group(2) if m else t


def _check_food(food: str, qty: float, unit: str) -> tuple[str, Parsed | None]:
    words = food.split()
    if not words or words[0] in UNSUPPORTED_UNITS or "of" in words[:2]:
        return Outcome.UNSUPPORTED_FORMAT, None
    if not re.fullmatch(r"[a-z][a-z \-']*", food):
        return Outcome.UNSUPPORTED_FORMAT, None
    return "OK", Parsed(food=food, quantity=qty, unit=unit)


# ---------------------------------------------------------------- resolution
def singular(word: str) -> str:
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("oes") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word


def tokens(text: str) -> set[str]:
    return {singular(w) for w in re.findall(r"[a-z]+", text.lower())}


def energy_kcal_per_100g(food: dict) -> tuple[float | None, int | None]:
    by_id = {n.get("nutrientId"): n for n in food.get("foodNutrients", [])}
    for nid in ENERGY_NUTRIENT_IDS:
        n = by_id.get(nid)
        if n and str(n.get("unitName", "")).upper() == "KCAL" and n.get("value") is not None:
            return float(n["value"]), nid
    return None, None


def pick_portion(food: dict) -> tuple[str, float] | None:
    portions = [p for p in food.get("foodPortions", []) if p.get("amount") == 1 and p.get("gramWeight")]
    if len(portions) == 1 and not portions[0]["modifier"].startswith("cup"):
        return "1 " + portions[0]["modifier"], float(portions[0]["gramWeight"])
    for word in PORTION_PREFERENCE:
        for p in portions:
            if p["modifier"].lower().startswith(word):
                return "1 " + p["modifier"].split(" (")[0], float(p["gramWeight"])
    return None


@dataclass
class Resolution:
    outcome: str
    food: dict | None = None
    kcal_per_100g: float | None = None
    energy_nutrient_id: int | None = None
    portion: tuple[str, float] | None = None  # (label, grams) for count or default
    route: str = ""  # "map" or "search"
    candidates: list[str] | None = None


def resolve(parsed: Parsed, client, food_map: dict) -> Resolution:
    """Find one reliable FDC record for the parsed food, or explain why not."""
    key = " ".join(singular(w) for w in parsed.food.split())
    try:
        if key in food_map:
            entry = food_map[key]
            food = client.get_food(entry["fdc_id"])
            kcal, nid = energy_kcal_per_100g(food)
            if kcal is None:
                return Resolution(Outcome.NO_ENERGY_VALUE, food=food, route="map")
            return Resolution(Outcome.LOGGED, food, kcal, nid,
                              (entry["portion_label"], float(entry["portion_grams"])), "map")
        results = client.search(parsed.food)
    except LookupError:
        return Resolution(Outcome.LOOKUP_FAILED)

    wanted = tokens(parsed.food)
    matched = [f for f in results
               if f.get("dataType") in ("Foundation", "SR Legacy")
               and wanted <= tokens(f["description"])
               and singular(f["description"].split(",")[0].strip().lower().split()[0]) in wanted]
    if not matched:
        return Resolution(Outcome.NOT_FOUND, route="search")
    with_energy = [(f, *energy_kcal_per_100g(f)) for f in matched]
    with_energy = [x for x in with_energy if x[1] is not None]
    if not with_energy:
        return Resolution(Outcome.NO_ENERGY_VALUE, food=matched[0], route="search")
    top = with_energy[:3]
    values = [x[1] for x in top]
    if len(top) > 1 and max(values) / min(values) > AMBIGUITY_RATIO:
        return Resolution(Outcome.AMBIGUOUS, route="search",
                          candidates=[x[0]["description"] for x in top])
    food, kcal, nid = top[0]
    return Resolution(Outcome.LOGGED, food, kcal, nid, pick_portion(food), "search")


def to_grams(parsed: Parsed, res: Resolution) -> tuple[float | None, str]:
    """Convert the tester's amount to grams. Returns (grams, explanation)."""
    if parsed.unit == "g":
        return parsed.quantity, f"{parsed.quantity:g} g"
    if res.portion is None:
        return None, ""
    label, grams = res.portion
    total = parsed.quantity * grams
    if parsed.unit == "default":
        return total, f"{label} ({grams:g} g, assumed because no amount was given)"
    return total, f"{parsed.quantity:g} x {label} ({grams:g} g each) = {total:g} g"


# ---------------------------------------------------------------- storage
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    telegram_user_id INTEGER PRIMARY KEY,
    created_at_utc   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS entries (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_user_id    INTEGER NOT NULL REFERENCES users(telegram_user_id),
    food_text           TEXT NOT NULL,
    fdc_id              INTEGER,
    matched_description TEXT,
    quantity            REAL NOT NULL,
    unit                TEXT NOT NULL CHECK (unit IN ('count','g','default')),
    grams               REAL NOT NULL CHECK (grams > 0),
    kcal                REAL NOT NULL CHECK (kcal > 0),
    source              TEXT NOT NULL CHECK (source IN ('fdc','manual')),
    logged_at_utc       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_entries_user_time ON entries(telegram_user_id, logged_at_utc);
"""

TS = "%Y-%m-%d %H:%M:%S"


def connect(path: str) -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(SCHEMA)
    return db


def ensure_user(db, user_id: int, now_utc: datetime) -> bool:
    """Create the tester if new. Returns True when a row was created (AC-1.2 safe)."""
    cur = db.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", (user_id, now_utc.strftime(TS)))
    db.commit()
    return cur.rowcount == 1


def add_entry(db, user_id, parsed, res, grams, kcal, now_utc) -> int:
    cur = db.execute(
        "INSERT INTO entries (telegram_user_id, food_text, fdc_id, matched_description, quantity,"
        " unit, grams, kcal, source, logged_at_utc) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (user_id, parsed.food, res.food["fdcId"], res.food["description"], parsed.quantity,
         parsed.unit, grams, kcal, "fdc", now_utc.astimezone(timezone.utc).strftime(TS)))
    db.commit()
    return cur.lastrowid


def chicago_day_window(day: date) -> tuple[str, str]:
    """UTC [start, end) for one Chicago calendar day. Handles 23 and 25 hour days."""
    start = datetime.combine(day, time(0), CHICAGO).astimezone(timezone.utc)
    end = datetime.combine(day + timedelta(days=1), time(0), CHICAGO).astimezone(timezone.utc)
    return start.strftime(TS), end.strftime(TS)


def chicago_today(now_utc: datetime) -> date:
    return now_utc.astimezone(CHICAGO).date()


def entries_for_day(db, user_id: int, day: date):
    start, end = chicago_day_window(day)
    return db.execute(
        "SELECT food_text, matched_description, grams, kcal, logged_at_utc FROM entries"
        " WHERE telegram_user_id = ? AND logged_at_utc >= ? AND logged_at_utc < ?"
        " ORDER BY logged_at_utc, id", (user_id, start, end)).fetchall()


def total_for_day(db, user_id: int, day: date) -> float:
    start, end = chicago_day_window(day)
    (total,) = db.execute(
        "SELECT COALESCE(SUM(kcal), 0) FROM entries WHERE telegram_user_id = ?"
        " AND logged_at_utc >= ? AND logged_at_utc < ?", (user_id, start, end)).fetchone()
    return float(total)


# ---------------------------------------------------------------- full path
REPLIES = {
    Outcome.UNSUPPORTED_FORMAT: "I couldn't read that. Send one food with a number or grams, like \"2 eggs\" or \"150g rice\".",
    Outcome.OUT_OF_RANGE: "That amount looks off. Use 1 to 20 items or 1 to 2000 grams.",
    Outcome.NOT_FOUND: "I couldn't find \"{food}\". Nothing was saved. Try a simpler name, like \"apple\" or \"rice cooked\".",
    Outcome.AMBIGUOUS: "\"{food}\" matches foods with very different calories ({options}). Nothing was saved. Please be more specific.",
    Outcome.NEEDS_GRAMS: "I found {desc} but don't know how much one serving weighs. Nothing was saved. Send it in grams, like \"150g {food}\".",
    Outcome.NO_ENERGY_VALUE: "The data source has no calorie value for {desc}. Nothing was saved. Try a similar food.",
    Outcome.LOOKUP_FAILED: "The food database isn't responding right now. Nothing was saved. Please try again in a minute.",
}


def handle_text(db, user_id: int, text: str, now_utc: datetime, client, food_map: dict):
    """Run one message through the whole slice. Returns (outcome, reply, entry_id or None)."""
    status, parsed = parse_message(text)
    if status != "OK":
        return status, REPLIES[status], None
    res = resolve(parsed, client, food_map)
    desc = res.food["description"] if res.food else ""
    if res.outcome != Outcome.LOGGED:
        options = "; ".join(res.candidates or [])
        return res.outcome, REPLIES[res.outcome].format(food=parsed.food, desc=desc, options=options), None
    grams, how = to_grams(parsed, res)
    if grams is None:
        return Outcome.NEEDS_GRAMS, REPLIES[Outcome.NEEDS_GRAMS].format(food=parsed.food, desc=desc), None
    kcal = res.kcal_per_100g * grams / 100
    ensure_user(db, user_id, now_utc)
    entry_id = add_entry(db, user_id, parsed, res, grams, kcal, now_utc)
    total = total_for_day(db, user_id, chicago_today(now_utc))
    reply = (f"Logged {desc}: {how} = {kcal:.0f} kcal. "
             f"Today's total: {total:.0f} kcal.")
    return Outcome.LOGGED, reply, entry_id


# ---------------------------------------------------------------- clients
class FixtureClient:
    """Offline stand-in for FDC built from fixtures/fdc_synthetic.json."""

    def __init__(self, path: str, fail: bool = False):
        with open(path, encoding="utf-8") as fh:
            self.foods = json.load(fh)["foods"]
        self.fail = fail
        self.calls = 0

    def search(self, query: str) -> list[dict]:
        self.calls += 1
        if self.fail:
            raise LookupError("simulated timeout")
        q = tokens(query)
        return [f for f in self.foods if q & tokens(f["description"])]

    def get_food(self, fdc_id: int) -> dict:
        self.calls += 1
        if self.fail:
            raise LookupError("simulated timeout")
        for f in self.foods:
            if f["fdcId"] == fdc_id:
                return f
        raise LookupError(f"fdcId {fdc_id} not found")
