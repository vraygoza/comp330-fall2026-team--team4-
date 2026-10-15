# Deferred Scope and Tradeoff Decisions

| Field | Value |
|-------|-------|
| Owner | Khumoyun (Operations & Evidence Co-Lead) |
| Backup | Mazen (Operations & Evidence Lead) |
| Last updated | 2026-10-14 |

## Deferred Features

| ID | Feature | Reason for Deferral | Earliest Cycle | Backlog Issue |
|----|---------|---------------------|----------------|---------------|
| DF-1 | Macro tracking (protein, carbs, fats, fiber) | Depends on a working calorie path first. Adding macros before calories work end-to-end adds risk with no user benefit. | Cycle 2 | Backlog-DF-1 (GitHub issue to be created at next team meeting) |
| DF-2 | Multiple foods in one message ("eggs and toast") | Parsing multiple items is a major technical risk. One item per message keeps Cycle 1 bounded and estimable. | Cycle 2 | Backlog-DF-2 (GitHub issue to be created at next team meeting) |
| DF-3 | History beyond today, weekly summaries, charts | Not needed to prove the vertical slice. The `/today` command covers the minimum useful case. | Cycle 2+ | Backlog-DF-3 (GitHub issue to be created at next team meeting) |
| DF-4 | Calorie goals, reminders, notifications | New feature category unrelated to the core log-and-lookup path. | Cycle 2+ | Backlog-DF-4 (GitHub issue to be created at next team meeting) |
| DF-5 | Photo or barcode food recognition | High effort, high uncertainty, and requires a separate ML/vision service. | Cycle 3+ or never | Backlog-DF-5 (GitHub issue to be created at next team meeting) |
| DF-6 | Web dashboard or any interface outside Telegram | Adds a second front end. Cycle 1 is strictly Telegram-only. | Cycle 2+ | Backlog-DF-6 (GitHub issue to be created at next team meeting) |
| DF-7 | Editing any entry other than the last one | `/undo` (optional O1) covers the most common mistake case. Full edit adds database complexity. | Cycle 2+ | Backlog-DF-7 (GitHub issue to be created at next team meeting) |

## Optional Items (Targets, Not Commitments)

These are in the scope statement as "Optional" (O1, O2). They are the first to be dropped if the schedule slips.

| ID | Feature | Condition to Include | Drop Trigger |
|----|---------|----------------------|--------------|
| O1 | `/undo` — remove the last entry (FR-8) | All committed items S1–S8 pass acceptance criteria with time remaining | Schedule slips past Week 3 of Cycle 1, or any committed item is still failing |
| O2 | Manual calorie entry when food not found (FR-9) | O1 is done and time remains | Same as O1, or O1 is dropped |

## Tradeoff Decisions

| ID | Decision | Alternatives Considered | Rationale | Date |
|----|----------|------------------------|-----------|------|
| TD-1 | One food item per message only | Multi-food parsing ("eggs and toast") | Parsing is a major risk (Risk 3). Single-item keeps scope bounded and lets us ship. Testers send multiple messages instead. | 2026-09-29 |
| TD-2 | "Today" means midnight-to-midnight Central time | Per-tester time zones | Testers are assumed to be in the Central time zone (see Assumption 3 in [Scope Statement](../planning/scope.md)). This is an explicit assumption, not a confirmed fact. If a tester is in a different zone, OQ-7 reopens and the assumption must be revised. | 2026-09-29 |
| TD-3 | Default to one standard serving when no amount given | Reject messages without an amount | Better user experience — requiring exact amounts makes the bot harder to use. The reply tells the tester what was assumed (AC-2.2). | 2026-09-29 |
| TD-4 | Free tiers only for all services | Paid APIs or hosting | Course constraint: no paid services. Limits data source and hosting choices but keeps cost at zero (NFR-5, Risk 5). | 2026-09-29 |

## Accepted Technical Debt

| ID | Debt | Why We Accept It | Plan to Address |
|----|------|------------------|-----------------|
| ATD-1 | No automated CI/CD pipeline | Setting up CI is not part of the vertical slice and adds setup time. | Evaluate for Cycle 2 once the codebase is established. |
| ATD-2 | No automated **acceptance** test framework | Automated unit tests for parsing and calorie math are planned (see [Quality Plan](../planning/quality-plan.md) §3). What is deferred is an end-to-end acceptance test framework, which requires OQ-3 (language and library) to close first. Near-term verification is: unit tests for pure logic + manual walkthrough of acceptance criteria before each merge. | Implement once OQ-3 is closed and language/framework is confirmed. |
| ATD-3 | Hardcoded "Central time" for daily reset | Proper time zone handling deferred (TD-2). Central time is an explicit assumption (see Scope Statement), not a confirmed fact about all testers. | Revisit if any tester is confirmed to be outside Central time. |


## Change Log

| Date | Change | By |
|------|--------|-----|
| 2026-10-01 | Created deferred scope document based on scope.md and planning evidence | Khumoyun |
| 2026-10-14 | Fixed D1 status contradiction; labelled backlog placeholders; fixed ATD-2 vs quality-plan contradiction; replaced inaccurate LMU reference in TD-2; | Khumoyun |
