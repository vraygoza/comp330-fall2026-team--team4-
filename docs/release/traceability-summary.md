# Cycle 1 Traceability Summary

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-11-09 |
| Baseline | Tag `a4-construction-integration` (commit 0a1d54dc) to `main` |

One row per requirement, traced from the requirement through the issue, pull request, CI run, test and demo step to the release note. Requirements come from [Requirements](../requirements/requirements.md); the task-level mapping is in [Traceability](../planning/traceability.md).

This summary records what is demonstrated, not what is planned. A requirement with no merged PR and no passing test is marked **Not demonstrated** regardless of how much design exists for it.

## Must Requirements

| Requirement | Issue | PR | CI | Test | Demo step | Release note | Status |
|---|---|---|---|---|---|---|---|
| FR-1 Start the bot (AC-1.1) | #48 | #69 merged | TODO: run link from ci-evidence.md | `tests/test_router.py`, `tests/test_web.py`, `tests/test_log_food.py` | TODO: demo-script.md | TODO: release-notes.md | Demonstrated |
| FR-1 Repeat `/start` is safe (AC-1.2) | #48, #50 | #69, #90 merged | TODO: run link | `tests/test_store.py`, `tests/test_log_food.py` | TODO | TODO | Demonstrated |
| FR-2 Log a food item (AC-2.1) | #61, #50 | #88, #90 merged | TODO: run link | `tests/test_log_food.py`, `tests/test_store.py` | TODO | TODO | Demonstrated against synthetic data |
| FR-2 Assumed serving stated (AC-2.2) | #61, #50 | #88, #90 merged | TODO: run link | `tests/test_log_food.py` | TODO | TODO | Demonstrated |
| FR-3 Look up calories (AC-3.1) | #49 | #70 merged | TODO: run link | `tests/test_food_lookup.py`, `tests/test_log_food.py` | TODO | TODO | Demonstrated against the sample list, not FDC |
| FR-3 Hand-check 20 foods (AC-3.2) | T-13 | None | None | None | Not in the demo | TODO | Not demonstrated. Needs V-1, the live FDC run |
| FR-4 Running total (AC-4.1) | #44, #50 | #83, #90 merged | TODO: run link | `tests/test_day.py`, `tests/test_log_food.py` | TODO | TODO | Demonstrated end to end |
| FR-5 View today's log (AC-5.1, AC-5.2) | T-15, T-16 | None | None | None | Not in the demo | TODO | Not demonstrated. `/today` is not built (CC-8) |
| FR-5 Chicago day cutoff (AC-5.3) | #44, #50 | #83, #90 merged | TODO: run link | `tests/test_day.py` (Nov 1 2026, Mar 14 2027), `tests/test_log_food.py` midnight reset | TODO | TODO | Demonstrated |
| FR-6 Unknown foods save nothing (AC-6.1, AC-6.2) | #49, #50 | #70, #90 merged | TODO: run link | `tests/test_food_lookup.py`, `tests/test_log_food.py`, `tests/test_store.py` kcal <= 0 refused | TODO | TODO | Demonstrated |
| FR-7 Separate data per tester (AC-7.1) | #50 | #90 merged | TODO: run link | `tests/test_store.py`, `tests/test_log_food.py` two-tester tests | TODO | TODO | Demonstrated |

## Should Requirements

| Requirement | Issue | PR | CI | Test | Demo step | Release note | Status |
|---|---|---|---|---|---|---|---|
| FR-8 Undo last entry | T-20 | None | None | None | Not in the demo | TODO | Deferred to Cycle 2 |
| FR-9 Manual calories | T-21 | None | None | None | Not in the demo | TODO | Deferred to Cycle 2 |

## Proposed Requirement

| Requirement | Issue | PR | CI | Test | Demo step | Release note | Status |
|---|---|---|---|---|---|---|---|
| FR-10 Tester access and `/privacy` | T-29 | None | None | None | Not in the demo | TODO | Not started. T-29 is unowned (CC-8) |

## Non-Functional Requirements

| Requirement | Issue | PR | CI | Test | Demo step | Release note | Status |
|---|---|---|---|---|---|---|---|
| NFR-1 Reply within 5 seconds | T-23 | None | None | None | TODO | TODO | Not measured |
| NFR-2 Supports 15 testers | T-24 | None | None | Synthetic 15-tester check in the INV-01 spike only | Not in the demo | TODO | Not demonstrated with real testers |
| NFR-3 No secrets in the repo | M2 | #73 merged | Secrets check runs on every PR | CI secrets check; `.gitignore`, `.env.example`; `tests/test_telegram_adapter.py` asserts the token never reaches the log | Not in the demo | TODO | Demonstrated |
| NFR-4 Store only what is needed | T-27 | #90 merged | TODO: run link | Mazen's T-27 check on #90: the store holds fewer fields than C-6 lists (architecture.md CC-6) | Not in the demo | TODO | Reviewed on #90; T-27 not formally closed |
| NFR-5 Free tiers only | #58 | #91 open | CI on #91 | pip-audit on Flask 3.1.3, clean | Not in the demo | TODO | Documented in ADR-0009, pending merge |

## What Is Not Covered

- **Live services.** No live Telegram deployment and no live USDA FoodData Central calls. Food values come from `src/core/sample_foods.json` and are synthetic. The bot runs by local polling (`src/bot/poll.py`); the webhook is built and unit tested but not deployed (CC-3), and nothing creates it with a store yet (CC-9).
- **Gram amounts** are parsed but refused with `NEEDS_GRAMS` and save nothing, because the sample list is per serving (CC-7).
- **Duplicate update protection (T-30)** is not built. Per architecture.md CC-5 the bot is not deployed until it merges.
- **Verification tasks V-1 to V-6** have not run and are deferred to Cycle 2, so hosting, rate limits and real FDC field behavior remain assumptions.
- **ADR-0001 to ADR-0008** are Proposed. The M1 vote (#56) has not happened, so no requirement traces to a formally accepted decision.

## One Live Run

Mazen ran the integrated bot against his own Telegram test bot at commit `14e247b` as part of his #90 review: `/start`, `2 eggs`, `Banana`, `100g rice` and `25 eggs` all produced the expected replies, with screenshots in the review. This is a local developer run, not a deployment, and not evidence of FDC integration.

## Columns Still Pending

| Column | Source | Owner | Needed by |
|---|---|---|---|
| CI | `docs/testing/ci-evidence.md` | Mazen | PR #91 merge |
| Demo step | `docs/release/demo-script.md` | Victoria | Not yet written |
| Release note | `docs/release/release-notes.md` | Khumoyun | Not yet written |

These three columns are filled in once those files are on `main`. This document is re-checked against `main` before the `a5-cycle1-release` tag.

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-11-09 | Created for Assignment 5, after PRs #90 and #92 merged | Bazid |
