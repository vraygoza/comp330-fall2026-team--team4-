# Cycle 1 Scope Statement

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Last updated | 2026-09-29 |

## Cycle 1 Vertical Slice
A tester sends the bot one food item in a text message. The bot finds the calories, saves the entry under that tester's account, and replies with the tester's calorie total for the day.

This one path touches every layer of the system: the Telegram interface, message parsing, the nutrition data lookup, storage, and the reply. If this path works end to end for real testers, Cycle 1 is a success.

Requirement details and acceptance criteria are in [Requirements](../requirements/requirements.md).

## In Scope (Committed)
| ID | Item | Requirement |
|----|------|-------------|
| S1 | `/start` command that registers the tester and explains how to log a meal | FR-1 |
| S2 | Log one food item per message and save it | FR-2 |
| S3 | Look up calories from one nutrition data source | FR-3 |
| S4 | Reply with the running daily total after each log | FR-4 |
| S5 | `/today` command that lists today's entries and total | FR-5 |
| S6 | Clear reply when a food cannot be found | FR-6 |
| S7 | Each tester sees only their own data | FR-7 |
| S8 | Bot token and API keys kept out of the repository | NFR-3 |

## Optional (Only If Committed Work Is Done)
These are targets, not commitments. They are dropped first if the schedule slips.

| ID | Item | Requirement |
|----|------|-------------|
| O1 | `/undo` command that removes the last entry | FR-8 |
| O2 | Tester enters calories manually when a food is not found | FR-9 |

## Out of Scope for Cycle 1
| Item | Reason |
|------|--------|
| Macro tracking (protein, carbs, fats, fiber) | Planned for a later cycle; depends on a working calorie path first |
| Several foods in one message ("eggs and toast") | Parsing is a major risk; one item per message keeps Cycle 1 bounded |
| History beyond the current day, weekly summaries, charts | Not needed to prove the vertical slice |
| Calorie goals, reminders, notifications | New features; go to the backlog |
| Photo or barcode food recognition | High effort and high uncertainty |
| Web dashboard or any interface outside Telegram | Adds a second front end |
| Editing an entry other than the last one | Undo (O1) covers the common case |

Out of scope items are recorded as backlog Issues, not deleted. Moving an item into Cycle 1 requires team agreement and a Decision Log entry, per [Planning](planning.md).

## Decisions Needed Before Implementation
Cycle 1 cannot start building until these open questions are closed. Full list in [Open Questions](../requirements/open-questions.md).

| Question | Why it blocks |
|----------|---------------|
| OQ-1: Which added features, if any, belong in Cycle 1? | The 2026-09-16 meeting asked the team to expand the scope; no decision is recorded |
| OQ-2: Which nutrition data source? | Every calorie number depends on it (Risk 4) |
| OQ-3: Which language and bot library? | Needed before any task can be estimated honestly |
| OQ-4: Where is data stored? | Needed for FR-2, FR-5, FR-7 |
| OQ-5: Where does the bot run during testing? | Testers cannot use a bot that only runs on one laptop |

## Assumptions
These are working assumptions, not commitments. If one proves wrong, the scope is revisited and the change is recorded in [Re-estimation Notes](reestimation.md).

- Testers already use Telegram.
- Testers log foods in English.
- All testers are in the Central time zone, so "today" means midnight to midnight Chicago time.
- A free tier of the chosen data source and hosting is enough for 15 testers.

## Cycle 1 Definition of Done
- Every committed item (S1 to S8) meets its acceptance criteria.
- At least 3 testers outside the development team have logged meals successfully.
- Code is merged through reviewed pull requests.
- Acceptance tests are recorded in `/docs/testing/`.
