# Assignment 6 Defect & Quality Summary

Repository: comp330-fall2026-team--team4-
Baseline Commit: 9dbc917 (main, 107 passing tests: 93 in tests/, 14 in spikes/inv-01-lookup-storage/)
Owner: Sohail Shaik (Quality & Review Lead)
Reviewer: Mazen Malas
Last Updated: 2026-11-23

---

## 1. Defect Disposition Register

| ID | Description | Severity | Disposition | Verification Evidence |
| :--- | :--- | :--- | :--- | :--- |
| DEF-01 | Unintegrated end-to-end loop returning NOT_READY | Critical | Fixed | Wired parser, lookup, store, and day totals in PR #90 (src/core/use_cases.py); verified in tests/test_log_food.py |
| DEF-02 | architecture.md out of sync with accepted ADRs | Medium | Fixed | Reconciled in PR #92 against accepted ADR-0001 through ADR-0009 (#56 vote) |
| DEF-03 | Lookup/parser failures on whitespace, casing, unmapped items | Medium | Fixed | Fixed in src/core/food_lookup.py (PR #74); verified in tests/test_food_lookup.py and tests/test_parser.py |
| DEF-04 | Router regression during integration overwrote commands | High | Fixed | Caught by CI tests (tests/test_router.py) and fixed before merge to main |
| DEF-05 | /today daily summary command unimplemented | Low | Deferred | Documented as deferred in docs/release/known-limitations.md and docs/release/final-release-notes.md |
| DEF-06 | Live USDA FoodData Central (FDC) API not connected | Medium | Deferred | Bounded to local src/core/sample_foods.json per ADR-0002 |
| DEF-07 | Multi-user SQLite isolation boundary verification | High | Fixed | Verified two-user isolation in tests/test_log_food.py and tests/test_store.py (PR #90) |
| DEF-08 | America/Chicago midnight and 23h/25h DST boundaries | Medium | Fixed (Unit) | Verified in tests/test_day.py and tests/test_day_contract.py (src/core/day.py) |
| DEF-09 | Duplicate Telegram update_id protection (T-30, PR #104) | High | Deferred (TODO) | TODO: PR #104 not merged on main at 9dbc917; tracked in docs/release/known-limitations.md |

## 2. Verification Summary
- Automated Tests: pytest passed locally on main (9dbc917): 107 passed in 2.44s (93 across the 10 files in tests/, 14 in spikes/inv-01-lookup-storage/test_investigation.py).
- CI Enforcement: .github/workflows/ci.yml runs automated tests and secret scans on pull requests.
- Residual Limitations: Unmerged items at freeze (T-30 / PR #104) and Cycle 2 features (/today, live FDC API) are documented in docs/release/known-limitations.md.
