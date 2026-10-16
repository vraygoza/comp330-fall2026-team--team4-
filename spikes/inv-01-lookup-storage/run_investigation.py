"""Run the INV-01 synthetic cases and print a Markdown results table.

Offline (default):  python3 run_investigation.py
Live FDC check:     FDC_API_KEY=... python3 run_investigation.py --live

The live mode only searches FDC and prints candidates, energy nutrient, portions,
latency and the X-RateLimit headers. It never stores anything. Keep the key in your
environment or .env; never paste it into a file that is committed.

AI-assisted (Claude). Human review: Adiya (pending), second reviewer: TODO.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import calorie_core as core

HERE = Path(__file__).parent
CASES = [
    # (message, what it tests)
    ("2 eggs", "count via curated map portion"),
    ("egg", "no amount: default portion stated in reply"),
    ("150g rice", "grams, but 'rice' alone is ambiguous (raw vs cooked)"),
    ("150g rice cooked", "grams with a specific name"),
    ("1 rice cooked", "count with no usable portion: ask for grams"),
    ("banana", "default portion from curated map"),
    ("egg white", "not in map: search fallback with single portion"),
    ("120g apple", "Foundation record with Atwater energy only (2047)"),
    ("apple", "no portion data: ask for grams"),
    ("100g oats", "record has no energy value"),
    ("mystery stew", "search hits but no reliable match"),
    ("xyzfood", "no search hits"),
    ("a cup of rice", "unsupported unit"),
    ("eggs 2", "trailing amount not accepted"),
    ("1/2 banana", "fraction not accepted"),
    ("25 eggs", "count above limit"),
    ("0 eggs", "zero amount"),
    ("3000g rice cooked", "grams above limit"),
]


def offline() -> int:
    client = core.FixtureClient(HERE / "fixtures" / "fdc_synthetic.json")
    food_map = json.loads((HERE / "fixtures" / "food_map_synthetic.json").read_text())
    food_map.pop("_notice", None)
    now = datetime(2026, 10, 14, 18, 0, tzinfo=timezone.utc)
    with tempfile.TemporaryDirectory() as tmp:
        db = core.connect(os.path.join(tmp, "spike.db"))
        print("| # | Message | Tests | Outcome | Saved | Reply |")
        print("|---|---------|-------|---------|-------|-------|")
        for i, (msg, why) in enumerate(CASES, 1):
            outcome, reply, entry_id = core.handle_text(db, 111, msg, now, client, food_map)
            print(f"| {i} | `{msg}` | {why} | {outcome} | {'yes' if entry_id else 'no'} | {reply} |")
        failing = core.FixtureClient(HERE / "fixtures" / "fdc_synthetic.json", fail=True)
        outcome, reply, entry_id = core.handle_text(db, 111, "150g rice cooked", now, failing, food_map)
        print(f"| {len(CASES) + 1} | `150g rice cooked` | lookup timeout (simulated) | {outcome} | "
              f"{'yes' if entry_id else 'no'} | {reply} |")
        rows = db.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
        print(f"\nEntries saved: {rows}. Fixture lookups made: {client.calls}.")
    return 0


def live(foods: list[str]) -> int:
    key = os.environ.get("FDC_API_KEY")
    if not key:
        print("Set FDC_API_KEY in your environment first.", file=sys.stderr)
        return 2
    base = "https://api.nal.usda.gov/fdc/v1/foods/search"
    for food in foods:
        params = {"api_key": key, "query": food, "pageSize": 5,
                  "dataType": "Foundation,SR Legacy"}
        url = base + "?" + urllib.parse.urlencode(params)
        start = time.perf_counter()
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                body = json.load(resp)
                remaining = resp.headers.get("X-RateLimit-Remaining")
                limit = resp.headers.get("X-RateLimit-Limit")
        except Exception as exc:  # record every failure, do not hide it
            print(f"\n## {food}\nFAILED after {time.perf_counter() - start:.2f}s: {exc!r}")
            continue
        ms = (time.perf_counter() - start) * 1000
        print(f"\n## {food}  ({ms:.0f} ms, totalHits={body.get('totalHits')}, "
              f"rate limit {remaining}/{limit})")
        for f in body.get("foods", []):
            kcal, nid = core.energy_kcal_per_100g(f)
            measures = [(m.get("disseminationText"), m.get("gramWeight"))
                        for m in f.get("foodMeasures", [])][:3]
            print(f"- {f['fdcId']} | {f['dataType']} | {f['description']} | "
                  f"kcal/100g={kcal} (nutrient {nid}) | measures={measures}")
    return 0


if __name__ == "__main__":
    if "--live" in sys.argv:
        default = ["egg", "eggs", "banana", "rice", "rice cooked", "apple", "chicken breast",
                   "oatmeal", "bread", "peanut butter"]
        extra = [a for a in sys.argv[1:] if a != "--live"]
        sys.exit(live(extra or default))
    sys.exit(offline())
