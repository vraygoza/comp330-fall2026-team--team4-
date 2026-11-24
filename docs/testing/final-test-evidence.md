# Final Test Evidence

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-11-23 |

The tests added after Assignment 4, the requirements they cover, and the live run that follows the demo path. Baseline: tag `a4-construction-integration` (66 tests). Code under test: integration PR #90, merged into `main` on 2026-11-09 (merge commit `957e410`). The live run used the PR at commit `14e247b`; the only later changes were a renamed test and docs, so the bot code is the same. CI details are in [CI Evidence](ci-evidence.md).

## Cycle 2 (Assignment 6)

Checked on 2026-11-23 with Python 3.12.3, the version CI uses, running `python -m unittest discover -s tests -t .`.

| Code | Tests | Result |
|------|-------|--------|
| Tag `A5Cycle1Release` (commit `8eca1b5`), the Cycle 1 release | 93 | All pass |
| `main` at commit `b789a22` | 93 | All pass. The only change since the tag is a docs file |
| PR #104 (T-30, duplicate-update protection) at commit `55de21f` | 111 | All pass |

**Correction:** the Summary below says 88 tests, the count for PR #90. K3 (#96) merged just before the Cycle 1 tag and added 5 more: 3 in `tests/test_food_lookup.py` and 2 in `tests/test_router.py`. So the Cycle 1 release has 93 tests.

**New in Cycle 2:** `tests/test_duplicate_updates.py` (#104) adds 18 tests: a Telegram resend with the same `update_id` saves one entry and sends one reply, the same text with a new `update_id` is a real second meal, two copies at the same moment save once, refusals and errors are not recorded so a resend can still succeed, and processed IDs survive a restart and are removed after 48 hours (C-1, T-30, Risk 23). #104 also gives each message in `tests/test_log_food.py` its own `update_id`. All 93 Cycle 1 tests still pass with #104.

**No new live run in Cycle 2.** The live run below (2026-11-09) is the latest; the bot code it ran is unchanged on `main`.

## Summary
- **Automated:** 88 tests, all passing. CI #31 ran them on PR #90; 66 of them were already on `main` at the A4 tag (CI #29).
- **New since Assignment 4:** 22 tests, all in PR #90.
- **Manual:** a live run with a real Telegram test bot on 2026-11-09. All five steps matched.

## New Tests Since Assignment 4
| File | Tests | What it checks | Requirements |
|------|-------|----------------|--------------|
| `tests/test_log_food.py` | 13 | The whole Log Food path: parse, look up, save, daily total, reply. Refused messages save nothing; repeat `/start`; two testers; the Chicago midnight reset | FR-1 to FR-4, FR-6, FR-7, AC-5.3 |
| `tests/test_store.py` | 8 | The SQLite Entry Store: a tester is registered once, entries need a registered tester, tester A never sees tester B, entries survive reopening the file, zero or negative calories are refused | FR-1, FR-7, AC-6.2, NFR-4 |
| `tests/test_day.py` | 1 more | An evening entry after UTC midnight still counts as Chicago "today" | AC-5.3 |

## Requirement Coverage (Cycle 1 Must Requirements)
| Requirement | Automated tests | Live run | Result |
|-------------|-----------------|----------|--------|
| FR-1 Start the bot | `test_start_registers_and_welcomes`, `test_repeat_start_keeps_the_total`, `test_register_creates_once`, router tests | `/start` | Tested (AC-1.1, AC-1.2) |
| FR-2 Log a food item | `test_logs_food_and_replies_with_total`, `test_no_amount_assumes_one_serving_and_says_so`, 22 parser tests | `2 eggs`, `Banana`, `25 eggs` | Tested for counts and no amount; gram entries save nothing until FDC (CC-2) |
| FR-3 Look up calories | 8 food lookup tests | `2 eggs` = 140 kcal | Partly: sample data only. AC-3.1 and AC-3.2 need FDC (V-1, T-13) |
| FR-4 Running total | `test_running_total_adds_up` | 140, then 245 | Tested |
| FR-5 View today's log | 20 day tests and `test_total_resets_at_chicago_midnight` | — | AC-5.3 tested. `/today` is not built, so AC-5.1 and AC-5.2 are not tested |
| FR-6 Unknown foods | `test_unknown_food_saves_nothing`, `test_partial_word_does_not_match`, `test_zero_or_negative_calories_are_refused` | — | AC-6.1 and AC-6.2 tested. AC-6.3 and AC-6.4 need FDC |
| FR-7 Separate data | `test_two_testers_have_separate_totals`, `test_tester_a_never_sees_tester_b` | — | Tested in automated tests only |
| FR-10 Tester access | — | — | Not built (T-29) |
| NFR-3 No secrets in repo | CI secrets check on every PR; `test_failed_send_returns_false_and_never_logs_token` | — | Tested ([CI Evidence](ci-evidence.md)) |
| NFR-4 Store only what is needed | T-27 table check, recorded on PR #90 | — | Passed |
| NFR-1, NFR-2 | — | — | Not tested: both need a deployed bot (ADR-0008) |

## Planned Test Cases
How the cases in [Test Cases](test-cases.md) map to automated tests. Exact reply wording differs from the planned text; the meaning matches.

| Case | Covered by | Result |
|------|------------|--------|
| TC-01 First `/start` | `test_start_registers_and_welcomes` | Pass |
| TC-02 Repeat `/start` | `test_repeat_start_keeps_the_total` | Pass |
| TC-03 Standard log | `test_logs_food_and_replies_with_total` | Pass |
| TC-04 Missing amount | `test_no_amount_assumes_one_serving_and_says_so` | Pass |
| TC-05 Unknown food | `test_unknown_food_saves_nothing` | Pass |
| TC-06 Empty daily total (`/today`) | — | Not tested: `/today` is not built |
| TC-07 Chicago midnight | `test_total_resets_at_chicago_midnight` | Pass |
| TC-08 Two testers | `test_two_testers_have_separate_totals` (checks totals in log replies, since `/today` is not built) | Pass |

## Live Run (Demo Path)
Run by Mazen on 2026-11-09 on macOS with Python 3.12.0, PR #90 at commit `14e247b`, using his own BotFather test bot and the local runner (`python -m src.bot.poll`). Screenshots are in Mazen's review on PR #90.

| Sent | Bot reply | Result | Checks |
|------|-----------|--------|--------|
| `/start` | Welcome message with an example | Pass | FR-1 |
| `2 eggs` | Logged 2 x Egg = 140 kcal. Today's total: 140 kcal | Pass | FR-2, FR-3, FR-4 |
| `Banana` | Logged 1 x Banana (assumed because no amount was given) = 105 kcal. Today's total: 245 kcal | Pass | AC-2.2, FR-4 |
| `100g rice` | Gram amounts will work once real nutrition data is connected | Pass (expected limit) | CC-2 |
| `25 eggs` | That amount is outside what I accept: 1 to 20 items, or 1 to 2000 grams | Pass | AC-2.3 |

**Setup finding:** on a Mac with Python from python.org, the bot could not reach Telegram (`CERTIFICATE_VERIFY_FAILED`) until Python's "Install Certificates.command" was run. This is a setup step, not a bot defect; it was reported on PR #90 and is now in the `src/README.md` run steps.

## Not Tested Yet
- `/today` (AC-5.1, AC-5.2), real FDC data (AC-3.1, AC-3.2, AC-6.3, AC-6.4), gram entries (AC-2.5, AC-2.6), tester access (FR-10).
- Duplicate updates (T-30), the live webhook (V-3), reply time (NFR-1) and 15-tester capacity (NFR-2): all need a deployed bot. Update 2026-11-23: duplicate updates are now tested in #104; a real Telegram retry still needs a deployed bot.
- Two testers and restart persistence were tested automatically, not in the live run.

Owners and next actions for these are in the [Risk Register](../planning/risk-register.md).

## Run the Tests
From the repository root: `python -m unittest discover -s tests -t .`

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-11-09 | Created for Assignment 5: tests since A4, requirement coverage, planned test cases, live run | Mazen |
| 2026-11-23 | Assignment 6: added the Cycle 2 section (93 tests at the Cycle 1 tag and on `main`, 111 with #104), the 88-to-93 correction, and the T-30 note under Not Tested Yet | Mazen |