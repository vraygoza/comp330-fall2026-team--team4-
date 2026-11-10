# Deferred Scope and Tradeoff Decisions

| Field | Value |
|---|---|
| Owner | Khumoyun (Operations & Evidence Co-Lead) |
| Backup | Mazen (Operations & Evidence Lead) |
| Last updated | 2026-11-09 |

## Deferred Features

| ID | Feature | Reason for Deferral | Earliest Cycle | Backlog Issue |
|---|---|---|---|---|
| DF-1 | Macro tracking (protein, carbs, fats, fiber) | Depends on a working calorie path first. Adding macros before calories work end-to-end adds risk with no user benefit. | Cycle 2 | Backlog-DF-1 (GitHub issue to be created at next team meeting) |
| DF-2 | Multiple foods in one message ("eggs and toast") | Parsing multiple items is a major technical risk. One item per message keeps Cycle 1 bounded and estimable. | Cycle 2 | Backlog-DF-2 (GitHub issue to be created at next team meeting) |
| DF-3 | History beyond today, weekly summaries, charts | Not needed to prove the vertical slice. The `/today` command covers the minimum useful case. | Cycle 2+ | Backlog-DF-3 (GitHub issue to be created at next team meeting) |
| DF-4 | Calorie goals, reminders, notifications | New feature category unrelated to the core log-and-lookup path. | Cycle 2+ | Backlog-DF-4 (GitHub issue to be created at next team meeting) |
| DF-5 | Photo or barcode food recognition | High effort, high uncertainty, and requires a separate ML/vision service. | Cycle 3+ or never | Backlog-DF-5 (GitHub issue to be created at next team meeting) |
| DF-6 | Web dashboard or any interface outside Telegram | Adds a second front end. Cycle 1 is strictly Telegram-only. | Cycle 2+ | Backlog-DF-6 (GitHub issue to be created at next team meeting) |
| DF-7 | Editing any entry other than the last one | `/undo` (optional O1) covers the most common mistake case. Full edit adds database complexity. | Cycle 2+ | Backlog-DF-7 (GitHub issue to be created at next team meeting) |
| DF-8 | Gram-based food logging with live USDA FDC data (CC-1, CC-2, CC-7) | Sample dataset has calories per serving only. Live FDC API connection and gram calculation deferred until live checks V-1 to V-6 confirm host network behavior. | Cycle 2 | Backlog-DF-8 |
| DF-9 | Standalone `/today` summary command (CC-8, T-15) | Construction prioritized the end-to-end meal logging path. Daily total is returned with meal logging; standalone query command deferred. | Cycle 2 | Backlog-DF-9 |
| DF-10 | `/privacy` command and tester invite check (CC-8, T-29) | Data collection notice text and tester whitelist check deferred to dedicated compliance task. | Cycle 2 / Pre-test | Backlog-DF-10 |
| DF-11 | `/undo` command for removing the last entry (O1, CC-8) | Optional target dropped to maintain Cycle 1 schedule commitments. | Cycle 2 | Backlog-DF-11 |

## Optional Items (Targets, Not Commitments)

These were defined in the scope statement as "Optional" (O1, O2). Both were dropped from Cycle 1 construction to ensure the core vertical slice was completed and tested on time.

| ID | Feature | Status in Cycle 1 | Reason Dropped |
|---|---|---|---|
| O1 | `/undo` — remove the last entry (FR-8) | Deferred to Cycle 2 (DF-11) | Prioritized parser, SQLite store, and Chicago day calculations. |
| O2 | Manual calorie entry when food not found (FR-9) | Deferred to Cycle 2 | Dependent on O1 completion; deferred to keep scope bounded. |

## Tradeoff Decisions

| ID | Decision | Alternatives Considered | Rationale | Date |
|---|---|---|---|---|
| TD-1 | One food item per message only | Multi-food parsing ("eggs and toast") | Parsing is a major risk (Risk 3). Single-item keeps scope bounded and lets us ship. Testers send multiple messages instead. | 2026-09-29 |
| TD-2 | "Today" means midnight-to-midnight Central time | Per-tester time zones | Testers are assumed to be in the Central time zone (see Assumption 3 in [Scope Statement](../planning/scope.md)). This is an explicit assumption, not a confirmed fact. If a tester is in a different zone, OQ-7 reopens and the assumption must be revised. | 2026-09-29 |
| TD-3 | Default to one standard serving when no amount given | Reject messages without an amount | Better user experience — requiring exact amounts makes the bot harder to use. The reply tells the tester what was assumed (AC-2.2). | 2026-09-29 |
| TD-4 | Free tiers only for all services | Paid APIs or hosting | Course constraint: no paid services. Limits data source and hosting choices but keeps cost at zero (NFR-5, Risk 5). | 2026-09-29 |

## Accepted Technical Debt

| ID | Debt | Why We Accept It | Plan to Address |
|---|---|---|---|
| ATD-1 | Automated CI/CD pipeline | Addressed in Assignment 4: GitHub Actions CI workflow implemented in PR #73 (`.github/workflows/ci.yml`). | Resolved for Cycle 1. |
| ATD-2 | No automated **acceptance** test framework | Automated unit tests for parsing, storage, and day calculations are merged. End-to-end automated acceptance testing against a live Telegram server remains manual. | Implement once host checks V-2 to V-4 are complete. |
| ATD-3 | Hardcoded "Central time" for daily reset | Proper per-user time zone handling deferred (TD-2). Central time is an explicit assumption. | Revisit in Cycle 2 if any tester is confirmed outside Central time. |
| ATD-4 | Duplicate `update_id` check in Webhook (CC-5, T-30) | Telegram webhooks may retry delivery on network timeouts. Recording `update_id` in SQLite within the same transaction as entry saving is deferred from A4 integration. **The bot is not deployed until T-30 merges.** | Khumoyun to implement T-30 before live host deployment. |
| ATD-5 | Production Webhook deployment on PythonAnywhere (CC-3, CC-9) | Live cloud deployment deferred pending live host verification checks V-2 to V-4. Development runner `poll.py` (`getUpdates`) is accepted for local testing and review. | Complete V-2 to V-4 and deploy with EntryStore. |

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-10-01 | Created deferred scope document based on scope.md and planning evidence | Khumoyun |
| 2026-10-14 | Fixed D1 status contradiction; labelled backlog placeholders; fixed ATD-2 vs quality-plan contradiction; replaced inaccurate LMU reference in TD-2 | Khumoyun |
| 2026-11-09 | Updated deferred scope and technical debt following Assignment 4 construction: added DF-8 to DF-11, ATD-4, ATD-5, noted CI completion in ATD-1 | Khumoyun |
