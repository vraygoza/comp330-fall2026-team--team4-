# Known Limitations and Deferred Scope

| Field | Value |
|---|---|
| **Owner** | Khumoyun (Operations & Evidence Co-Lead) |
| **Backup** | Victoria (Team Lead) |
| **Reviewer** | Victoria (Team Lead) |
| **Last updated** | 2026-11-23 |
| **Status** | Final Release Baseline (`a6-final-release`) |

This document provides a transparent, complete record of what the Telegram calorie tracker bot **cannot do**, what architectural features were deferred during construction, and what operational constraints currently exist. It reflects the as-built state of the software at the Assignment 6 final release freeze.

---

## Executive Summary: What Works vs. What Does Not

### What Works in the Current Vertical Slice
- **Start and Registration (FR-1, C-1):** Testers send `/start` to register their unique Telegram user ID in SQLite (`bot.db`) and receive welcome instructions.
- **Single-Food Message Parsing (FR-2, C-2):** Testers log one food item per message with an explicit count (e.g., `2 eggs`, `3 tacos`) or without a count (e.g., `banana`), which defaults to 1 standard serving (AC-2.2).
- **Curated Calorie Resolution (FR-3, C-4):** Calorie values resolve against a local curated sample database of 8 foods (`egg`, `banana`, `apple`, `taco`, `rice`, `toast`, `yogurt`, `pizza slice` in `src/core/sample_foods.json`) with strict exact-name and alias matching.
- **Safe Persistence & Tester Isolation (FR-6, FR-7, C-6):** Entries are saved under the requesting tester's ID in SQLite (`src/adapters/store.py`). Testers never see or modify other testers' records (AC-7.1).
- **Chicago Daily Totals (FR-5, C-6, ADR-0007):** The bot calculates and returns today's cumulative calories based on the America/Chicago calendar day (midnight to midnight) via `src/core/day.py`.
- **Safe Logging & Error Recovery (NFR-3, NFR-4, C-8):** Lookup failures emit generic logs without recording user chat IDs or food names. Unhandled exceptions return `"Something went wrong. Please try again later."` instead of crashing.

---

## Detailed Known Limitations

### 1. Message Input & Natural Language Parsing

| Limitation | Impact on Tester | Technical Cause / Governing Decision | Planned Resolution |
|---|---|---|---|
| **Single Food Item Only** | Testers cannot send combined meals like `"2 eggs and 1 banana"` or `"burger with fries"`. | **TD-1, DF-2:** Multi-food sentence parsing introduces substantial ambiguity and failure risk. Scoped strictly to one item per message. | Deferred to Cycle 2 feature backlog (DF-2). |
| **Gram Quantities Refused** | Messages with gram units (e.g., `100g rice`, `250 g chicken`) are recognized by the parser but refused with `"Gram amounts will work once real nutrition data is connected."` | **CC-1, CC-2, CC-7:** The local sample dataset provides calories per standard serving only. Gram scaling requires USDA FoodData Central (FDC) data. | Re-enable when live FDC adapter is built (CC-1). |
| **Strict Quantity Limits** | Counts outside 1 to 20, or gram amounts outside 1 to 2000g, are rejected with `"That amount is outside what I accept"`. | **AC-2.3, ADR-0004:** Bounded range prevents nonsensical entries, integer overflow, and denial-of-service edge cases. | Intentional permanent safety bound. |
| **No Conversational Language** | Phrases like `"I had two eggs for breakfast"` or `"ate a banana"` return a formatting hint. | **ADR-0004:** The parser accepts deterministic patterns `<quantity> <food>` or `<food>` only. Natural language sentence extraction is explicitly avoided. | Deterministic parsing retained by design. |
| **No Multimedia Input** | Photos of meals, voice notes, stickers, and barcode scans are ignored or rejected with a format hint. | **DF-5, C-1:** Computer vision and audio processing require external AI/ML services, conflicting with ADR-0001 (no AI in running bot). | Deferred to Cycle 3+ or out of scope. |

---

### 2. Food Nutrition Data & Resolver Constraints

| Limitation | Impact on Tester | Technical Cause / Governing Decision | Planned Resolution |
|---|---|---|---|
| **Synthetic Sample Foods Only** | Only 8 curated foods (`egg`, `banana`, `apple`, `taco`, `rice`, `toast`, `yogurt`, `pizza slice` in `src/core/sample_foods.json`) can be logged. All other foods return `"I don't know [food] yet"`. | **CC-1, CC-4:** USDA FDC live integration was deferred until live host checks V-1 to V-6 confirm network latency and rate limits from PythonAnywhere. | Connect live FDC API via `src/adapters/fdc.py` after V-1 passes. |
| **Zero Guessing or Partial Matches** | Typing `"egg roll"` will not match `"egg"`; typing `"pizza"` will not match `"pizza slice"`. | **AC-6.2, ADR-0002:** The bot must never guess or substitute nutritional data without tester confirmation. | Curated food map with explicit aliases planned for future cycle (T-13, CC-4). |
| **Calories Only (No Macros)** | The bot reports only kilocalories (`kcal`). Protein, carbs, fats, fiber, and sodium are not tracked or saved. | **DF-1:** Adding macronutrient tracking before calories work end-to-end adds architectural risk without validating the core vertical slice. | High-priority Cycle 2 milestone (DF-1). |
| **No Manual Calorie Override** | If a food is not in the database, the tester cannot manually enter a custom calorie number (e.g., `"salad 350 kcal"`). | **O2, FR-9:** Manual override was marked optional (target, not commitment) and deferred from construction. | Re-evaluate for Cycle 2 backlog (FR-9). |

---

### 3. User Commands & Interaction Workflows

| Limitation | Impact on Tester | Technical Cause / Governing Decision | Planned Resolution |
|---|---|---|---|
| **No Standalone `/today` Command** | Sending `/today` currently returns a format hint. Today's calorie total is visible only upon logging a meal. | **CC-8, T-15:** Router and use cases currently implement `/start` and text meal logging only. | TODO: Dedicated `/today` query use case deferred to Cycle 2 (T-15). |
| **No `/undo` Command** | If a tester accidentally logs a food twice or types the wrong amount, the entry cannot be deleted or undone. | **O1, DF-7, CC-8:** `/undo` was an optional target dropped when schedule prioritized the core vertical slice. | Priority Cycle 2 feature (O1 / DF-7 / T-20). |
| **No Historical Logs or Trends** | Testers cannot view yesterday's food log, weekly calorie summaries, or nutritional charts. | **DF-3:** Not needed for the initial vertical slice proof. | Deferred to Cycle 2+ reporting backlog. |
| **No Calorie Goals or Reminders** | The bot does not support target calorie budgets, daily deficit/surplus goals, or meal reminders. | **DF-4:** Out of scope for the core logging loop. | Deferred to Cycle 2+ feature backlog. |
| **No `/privacy` Reply Command** | The bot does not yet provide an automated `/privacy` command displaying the data collection notice. | **T-29, CC-8:** Deferred to follow-up privacy and compliance task. | TODO: Implement T-29 before public open testing. |
| **Telegram Only** | No web interface, mobile app, or export functionality (e.g., CSV/JSON download). | **DF-6:** Strictly Telegram-only. | Telegram remains primary interface. |

---

### 4. Hosting, Operational & Security Constraints

| Limitation | Impact on System / Tester | Technical Cause / Governing Decision | Planned Resolution |
|---|---|---|---|
| **Local Polling Runner Only** | The bot runs via `src/bot/poll.py` (`getUpdates`) on local development machines, not on an active cloud server. | **CC-3, P-7:** PythonAnywhere hosting checks V-2 to V-4 remain open; public HTTPS webhook URL is not active. | Deploy webhook to PythonAnywhere once V-2 to V-4 pass. |
| **Duplicate Update Protection Status** | Multiple identical webhook requests from Telegram network retries could theoretically log a meal twice. | **CC-5, T-30, Risk 23:** Implemented in PR #104 by Adiya with atomic `processed_updates` recording. **If PR #104 merges before the release tag, this limitation is resolved; if PR #104 is unmerged at freeze, T-30 remains deferred and the bot cannot be deployed publicly.** | Adiya to finish review/merge of PR #104. |
| **Hardcoded Central Timezone** | All daily totals reset at midnight America/Chicago. Testers in other time zones cannot configure their local day boundary. | **TD-2, ATD-3, ADR-0007:** Explicit simplifying assumption for Cycle 1 testers. | Per-user timezone preference in Cycle 2 (OQ-7). |
| **Single-Host Local SQLite File** | Entries reside in a local `bot.db` file without automated backup or cross-region replication. | **ATD-1, T-35:** PythonAnywhere free tier constraint. Nightly `.backup` script is planned but not automated. | TODO: Implement T-35 automated backup script. |

---

## Traceability to Governing Project Records

The limitations documented above trace directly to project decisions, risk assessments, and architecture records:

- **Architecture Construction Changes:** [docs/architecture/architecture.md](../architecture/architecture.md), Section 11 (CC-1 to CC-9).
- **Deferred Scope Decisions:** [docs/decisions/deferred-scope.md](../decisions/deferred-scope.md) (DF-1 to DF-7, O1, O2).
- **Accepted Technical Debt:** [docs/decisions/deferred-scope.md](../decisions/deferred-scope.md) (ATD-1 to ATD-3).
- **Architectural Decision Records:** [docs/decisions/adr-0001-no-ai-in-bot.md](../decisions/adr-0001-no-ai-in-bot.md) through [adr-0009-dependencies.md](../decisions/adr-0009-dependencies.md).
- **Risk Register:** [docs/planning/risk-register.md](../planning/risk-register.md) (Risks 1, 3, 5, 8, 14, 17, 23).
- **Final Release Notes:** [docs/release/final-release-notes.md](final-release-notes.md).
- **Operations Runbook:** [docs/operations/runbook.md](../operations/runbook.md).
- **Defects & Postmortem:** Cross-referenced with `docs/quality/defect-summary.md` and `docs/operations/postmortem-cycle1.md` (in PR #105).
