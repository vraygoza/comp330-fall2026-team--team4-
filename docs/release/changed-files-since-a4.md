# Changed Files Since Assignment 4

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-11-09 |
| Compared | Tag `a4-construction-integration` (commit 0a1d54dc) to `main` |

Every file changed since the Assignment 4 baseline, what changed in it, and who owns it. Areas with no change are listed too, so a reviewer can tell the difference between "unchanged" and "overlooked".

Totals: 14 files, 547 additions, 39 deletions, from two merged pull requests.

## Pull Requests in This Window

| PR | What it delivered | Author | Reviewer | Merged |
|----|-------------------|--------|----------|--------|
| #90 | A4 integration: message to parse, lookup, save, daily total and reply | Adiya | Mazen | 2026-11-09 |
| #92 | A5 final architecture check against the integrated code | Adiya | Mazen | 2026-11-09 |

## Source Code

| File | Status Since Assignment 4 | What changed | PR | Owner |
|------|---------------------------|--------------|----|-------|
| `src/core/use_cases.py` | New, 89 lines | The Log Food use case: parse, lookup, save under the tester ID, daily total, reply. Every refusal path saves nothing (AC-6.1, AC-6.2) | #90 | Adiya |
| `src/adapters/store.py` | New, 101 lines | SQLite Entry Store. `users` and `entries` tables; every read and write takes a Telegram user ID (FR-7, AC-7.1). Schema rejects kcal <= 0 and naive timestamps | #90 | Adiya |
| `src/bot/router.py` | Changed, +23 / -6 | `/start` now registers the tester; plain text runs Log Food. Takes an optional `store` and `now_utc` so tests can inject a temporary database | #90 | Adiya |
| `src/bot/web.py` | Changed, +4 / -3 | `create_app` takes an optional `store` and passes it to the router. Nothing in production creates the app with a store yet (CC-9) | #90 | Adiya |
| `src/bot/poll.py` | Changed, +6 / -1 | Opens an `EntryStore` from `BOT_DB_PATH`, passes it to the router, closes it on exit | #90 | Adiya |
| `src/core/day.py` | Changed, +10 | Added `chicago_date_of`, which returns the Chicago calendar date for a UTC moment. Pairs with `chicago_day_bounds` and `total_for_day` from #83 | #90 | Bazid (file), Adiya (addition) |

## Tests

| File | Status Since Assignment 4 | What changed | PR | Owner |
|------|---------------------------|--------------|----|-------|
| `tests/test_log_food.py` | New, 163 lines | End-to-end tests through the router with a real store: happy path, running total, assumed serving (AC-2.2), every refusal path, Chicago midnight reset (AC-5.3), two-tester separation (AC-7.1), repeat `/start` (AC-1.2) | #90 | Adiya |
| `tests/test_store.py` | New, 90 lines | Entry Store tests: register once, repeat `/start` keeps entries, time-window reads, tester isolation, zero-calorie and naive-time refusals, entries survive reopening the file | #90 | Adiya |
| `tests/test_day.py` | Changed, +10 / -1 | Added `ChicagoDateOfTests` for the new `chicago_date_of` function | #90 | Bazid (file), Adiya (addition) |
| `tests/test_router.py` | Changed, +3 / -2 | Renamed `test_food_text_is_not_logged_yet` to `test_food_text_without_a_store_is_not_logged`, since food logging now works when a store is supplied | #90 | Adiya |

## Configuration

| File | Status Since Assignment 4 | What changed | PR | Owner |
|------|---------------------------|--------------|----|-------|
| `.env.example` | Changed, +2 | Added optional `BOT_DB_PATH`. Defaults to `bot.db` in the repo folder, which is git-ignored | #90 | Adiya |
| `src/README.md` | Changed, +10 / -4 | Python minimum raised to 3.12 (ADR-0009); Mac certificate note; run steps now cover food logging and where `bot.db` lives | #90 | Adiya |

## Documentation

| File | Status Since Assignment 4 | What changed | PR | Owner |
|------|---------------------------|--------------|----|-------|
| `docs/architecture/architecture.md` | Changed, +34 / -22 | Status column added to the Section 3 component table; as-built note in Section 4 with the actual reply text; CC-6 to CC-9 added; live-check status updated; the Section 11 TODO closed | #92 | Adiya |
| `docs/ai/ai-use-log.md` | Changed, +2 rows | Rows for the #90 integration and the #92 architecture check, both including the human verification step | #90, #92 | Khumoyun (file) |

## Areas With No Change Since Assignment 4

| Area | Why unchanged |
|------|---------------|
| `docs/requirements/` | Requirements did not move during integration. FR-1 to FR-10 and NFR-1 to NFR-5 are as accepted at A3 |
| `docs/decisions/adr-0001` to `adr-0008` | Still Proposed. Acceptance waits on the M1 vote (#56). ADR-0009 is in PR #91, not yet merged |
| `docs/architecture/api-contracts.md`, `data-context.md`, the diagram | Contracts and data boundaries did not change. Where the code differs from them it is recorded as CC-1 to CC-9 in `architecture.md` rather than by editing the contracts |
| `docs/planning/` | The planning records merged before the A4 tag. A5 updates are in PRs #93 and the schedule PR, open at the time of this comparison |
| `.github/workflows/ci.yml` | The CI workflow merged in #73 before the A4 tag and has not changed |
| `src/core/parser.py`, `src/core/food_lookup.py`, `src/adapters/telegram.py` | Merged before the A4 tag (#88, #70, #69). The integration calls them without modifying them |
| `spikes/` | The INV-01 spike is a frozen record of the A3 investigation |

## Still Open at the Time of This Comparison

| PR | Contents | Owner |
|----|----------|-------|
| #89 | Repo-wide consistency check; splits the AI log into separate files | Khumoyun |
| #91 | ADR-0009 dependency review, risk register, CI evidence | Mazen |
| #93 | Task plan: reverses the 10/30 team change | Bazid |
| #94 | Defect summary, Cycle 2 handoff, presentation index | Sohail |
| Schedule update | Schedule statuses and the team-change reversal | Bazid |

This index is regenerated against `main` before the `a5-cycle1-release` tag.

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-11-09 | Created from the `a4-construction-integration`-to-`main` comparison | Bazid |
