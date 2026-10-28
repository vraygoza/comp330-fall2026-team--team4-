# A1: Design Check Before Construction

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Reviewer | Mazen |
| Issue | #47 |
| Baseline checked | Tag `a3-architecture-review` (commit `42350c6`) |
| Last updated | 2026-10-26 |

This check compares the A3 design (ADR-0001 to ADR-0008, [architecture.md](../architecture/architecture.md), [api-contracts.md](../architecture/api-contracts.md)) with the Assignment 4 task cards, and responds to the A3 instructor finding that the team needs one accepted direction for construction. It does not accept the ADRs. The team vote on D3 and ADR-0001 to ADR-0008 is issue #56 (M1). This file is the input to that vote.

## 1. Language, Library and Test Tool

| Choice | Decision for construction | Source |
|--------|---------------------------|--------|
| Language | Python 3.10 or later | ADR-0005 |
| Web framework | Flask (the only third-party runtime package) | ADR-0005 |
| Telegram | Our own thin adapter using the standard library (`urllib`). No `python-telegram-bot` | ADR-0005 |
| Test tool | Python's built-in `unittest`. Run: `python -m unittest discover -s tests -t .` | ADR-0005 evidence; same tool as the INV-01 spike |
| Layout | `src/core/`, `src/bot/`, `src/adapters/`, `tests/` | architecture.md, Section 3 |

## 2. What We Build for the Slice

A tester sends `/start`, then one food such as `2 tacos`. The bot parses it, looks up calories in a **made-up sample list**, saves the entry under the tester's Telegram user ID, and replies with today's Chicago-day total.

| Step | Task card | Owner | File |
|------|-----------|-------|------|
| Skeleton, `/start`, token from environment | A2 (#48) | Adiya | `src/bot/`, `src/adapters/telegram.py` |
| Parse `2 tacos` into food and quantity | K2 (#61) | Khumoyun | `src/core/parser.py` |
| Look up calories or return unknown | A3 (#49) | Adiya | `src/core/food_lookup.py` |
| Today's total in Chicago time | B2 (#44) | Bazid | `src/core/day.py` |
| Save, connect, reply | A4 (#50) | Adiya | `src/core/use_cases.py`, `src/adapters/store.py` |

Out of the slice: live FDC lookups, hosting and deployment, `/undo`, `/privacy`, invite codes, duplicate update protection (T-27). These stay in the plan; none are needed to show the slice working.

## 3. Interfaces So the Pieces Fit

Agreeing on these now lets K2, B2 and A3 be built in parallel and joined in A4 without rework.

**K2 parser** (`src/core/parser.py`)

```python
parse_message(text: str) -> ParseResult
# ParseResult fields: outcome, food, quantity
# outcome is one of: "PARSED", "UNSUPPORTED_FORMAT", "OUT_OF_RANGE"
# parse_message("2 tacos") -> ParseResult("PARSED", "tacos", 2.0)
# parse_message("banana")  -> ParseResult("PARSED", "banana", 1.0)   see Finding 1
```

**A3 lookup** (`src/core/food_lookup.py`, built)

```python
lookup(food: str) -> LookupResult
# LookupResult fields: outcome ("FOUND" or "NOT_FOUND"), name, serving, kcal_per_serving
```

**B2 daily total** (`src/core/day.py`)

```python
daily_total(entries, today: date) -> float
# entries: objects or dicts with kcal (float) and logged_at (timezone-aware UTC datetime)
# today: the Chicago calendar date. Sum only entries whose logged_at falls on that date
# in America/Chicago. Example: 23:30 Chicago on Oct 26 counts for Oct 26; 00:10 counts for Oct 27.
```

Core files import nothing from `src/bot/`, `src/adapters/`, Flask, `sqlite3` or `urllib` (architecture.md, Section 3). Reviewers check this on every PR.

## 4. Findings: Where the Docs and the Task Cards Disagree

| # | Finding | Recommendation | Decide at |
|---|---------|----------------|-----------|
| 1 | K2 says a message with no quantity gets "how many?" AC-2.2, ADR-0004 and C-2 say the bot uses one standard serving and says so. | Follow AC-2.2: `banana` logs one serving and the reply says it was assumed. It is already the documented requirement and needs no second message. If the team prefers asking, AC-2.2 and ADR-0004 must change in the same PR. | #56 (M1), before K2 merges |
| 2 | A3 uses a made-up food list. ADR-0002 and C-4 specify FDC with a curated map. | Build the slice on sample data now. Live check V-1 is not done, and the A3 feedback says to authorize only work that does not depend on unverified FDC behavior. `lookup()` is the seam: the FDC resolver replaces it later without changing callers. Sample values are labeled synthetic. | #56: record ADR-0002 as conditional on V-1 |
| 3 | ADR-0005 and ADR-0006 assume a webhook on PythonAnywhere. Host checks V-2 to V-4 are open, so no public webhook URL exists. | Build and unit test the webhook (`src/bot/web.py`), but run the bot locally with `src/bot/poll.py`, which uses Telegram `getUpdates`. This is a **development-only** addition not listed in C-3. Both use the same router. Do not deploy until V-2 to V-4 pass. | #56; record in A5 (#51) |
| 4 | Sample counts are per serving; ADR-0003 converts everything to grams. | Slice math is `quantity x kcal_per_serving`. Gram rules (ADR-0003) return with FDC data. | A5 (#51) |
| 5 | `.gitignore` ignores every `data/` folder, so the planned `data/food_map.json` could never be committed. | Sample file lives at `src/core/sample_foods.json`. Fix the ignore rule when the real food map arrives. | A5 (#51) |
| 6 | `zoneinfo` needs the `tzdata` package on Windows; B2 depends on `America/Chicago`. | Add `tzdata` to `requirements.txt` if any teammate runs Windows; include it in the dependency review. | M3 (#58), B2 (#44) |
| 7 | `docs/architecture/README.md` is empty; the index sits at `docs/architecture/docs/architecture/README.md`. `component-responsibilities.md` and `docs/testing/test-strategy.md` are linked but missing. (A3 feedback, Package navigation) | Move the index and fix or remove dead links. | A5 (#51) |
| 8 | `traceability.md` and `task-plan.md` give T-27 to T-29 different meanings. (A3 feedback, Traceability) | One governing ID set in `task-plan.md`; traceability updated to match. | B1 (#43), B3 (#45) |

## 5. Work That May Proceed Before the Live Checks

| May proceed now | Waits for a live check |
|-----------------|------------------------|
| Skeleton, router, webhook code and its unit tests | Deploy to the host (V-2 to V-4) |
| Parser, sample lookup, daily total, local storage | Real FDC lookups and the curated map (V-1) |
| Local end-to-end run with a test bot (A4) | FDC rate and timing checks (V-5, V-6) |

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-10-26 | Created for issue #47 | Adiya |
