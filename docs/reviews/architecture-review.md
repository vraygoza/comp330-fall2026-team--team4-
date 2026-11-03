# Architecture and ADR Review Record

| Field | Detail |
|---|---|
| Review Date | 2026-10-29 |
| Reviewer | Sohail Shaik (Quality & Review Lead) |
| Author / Lead Contact | Adiya (Architecture & Development Lead) |
| Scope Evaluated | Scope Decision D3, ADR-0001 through ADR-0008, API Contracts C-1 to C-8 |
| Baseline Tag / Commit | `a3-architecture-review` (`42350c6`) |

---

## 1. Review Summary & Purpose

During Assignment 3, architecture proposals and decision records ADR-0001 through ADR-0008 alongside scope decision D3 were drafted but were marked as `Proposed`. Furthermore, PR #23 and PR #29 were merged without an independent peer review. This document reviews and accepts those decisions so construction can start safely.

As Quality & Review Lead, this independent review evaluates the technical assumptions, interface boundaries, and failure cases to transition these records from `Proposed` to `Accepted` (or `Accepted with Conditions`) before the Cycle 1 implementation.

---

## 2. Decision Log & ADR Dispositions

| ID | Title | Prior Status | Disposition | Notes & Construction Conditions |
|---|---|---|---|---|
| D3 | Cycle 1 MVP Scope (Calorie-only) | Proposed | Accepted | Scope strictly bounded to single food entry logging, daily total, and `/today`. Macro tracking deferred to Cycle 2. |
| ADR-0001 | Non-AI Core Runtime Boundary | Proposed | Accepted | Deterministic parsing and USDA FDC API matching only; no LLM in the core loop. |
| ADR-0002 | Food Resolution via USDA FDC | Proposed | Accepted with Conditions | Condition: Bot must fail cleanly with user-facing refusal on zero matches or ambiguous multi-matches (no arbitrary fallback). |
| ADR-0003 | Serving & Quantity Parsing | Proposed | Accepted with Conditions | Condition: Missing quantity defaults to 1.0 standard serving as defined by FDC portion, with explicit disclosure in reply message. |
| ADR-0004 | Text-Based Bot Interface | Proposed | Accepted | Standard Telegram messages; custom UI keyboards deferred. |
| ADR-0005 | Telegram Webhook vs Long Polling | Proposed | Accepted | Webhook architecture approved for production; local dev may use polling if isolated by environment flag. |
| ADR-0006 | SQLite with Per-User Isolation | Proposed | Accepted with Conditions | Condition: All queries must filter by `telegram_user_id`. Synthetic tests must run concurrent assertions across two user IDs. |
| ADR-0007 | Chicago Midnight Boundary Calculation | Proposed | Accepted with Conditions | Condition: Date boundary must explicitly anchor to `America/Chicago` (handling CST/CDT shifts), preventing UTC midnight misattribution. |
| ADR-0008 | Synthetic vs Live Performance Targets | Proposed | Accepted | Offline synthetic benchmarks accepted for A3/A4; 15-tester live concurrency checks deferred to deployment gate. |

---

## 3. Substantive Challenges & Risk Findings

### Finding 1: Food-Matching Negative Case & Refusal Behavior (ADR-0002)
* Risk Identified: When USDA FoodData Central returns no results, returns low confidence scores, or times out, the bot must not crash or log an unverified calorie count.
* Review Challenge: If a user submits an unknown item (e.g., "1 serving flurbo"), how does the system reject it?
* Author Resolution / Agreement: C-2 contract updated. The parser and adapter will return an explicit `FOOD_NOT_FOUND` status code. The bot will send a friendly refusal ("Could not find calories for 'flurbo'. Please check spelling or try a simpler name.") and write zero records to the SQLite database.

### Finding 2: Cross-User Data Isolation in Shared SQLite DB (ADR-0006)
* Risk Identified: Multi-tenant leakage where Tester A accidentally views or aggregates food logged by Tester B.
* Review Challenge: Single SQLite database file must enforce complete logical isolation.
* Author Resolution / Agreement: Every insert and select statement in the storage adapter requires a parameterized `telegram_user_id`. A dedicated automated test case (`test_user_isolation`) must create two distinct user fixtures and verify that User B’s `/today` summary is strictly 0 after User A logs 500 kcal.

### Finding 3: Chicago Day Boundary & Daylight Saving Rollover (ADR-0007)
* Risk Identified: Telegram timestamps arrive in UTC. Entries logged between 7:00 PM and 11:59 PM CST would roll over into the next day if evaluated against UTC midnight.
* Review Challenge: Calculations must resolve timestamps in the `America/Chicago` timezone before grouping by calendar date.
* Author Resolution / Agreement: Timezone conversion logic is centralized in the core domain service (`services/day_calculator.py`), converting UTC epoch times to `America/Chicago` before extracting `YYYY-MM-DD`.

---

## 4. Construction Gate Approval

With the conditions above documented:
1. ADR-0001 through ADR-0008 and D3 are approved for implementation.
2. The team may proceed with Cycle 1 construction under the accepted interface contracts C-1 through C-8.