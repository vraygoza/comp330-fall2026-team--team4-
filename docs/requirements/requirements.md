# Cycle 1 Requirements

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Last updated | 2026-09-29 |

This package covers Cycle 1 only. Scope boundaries are in the [Scope Statement](../planning/scope.md). Unresolved items are in [Open Questions](open-questions.md).

Priority: **Must** = committed for Cycle 1. **Should** = optional, done only if Must items are finished. **Later** = backlog.

## Users
| User | Description |
|------|-------------|
| Tester | One of 10 to 15 friends or classmates who logs meals through Telegram |
| Developer | A Team 4 member who runs and maintains the bot |

## Functional Requirements

### FR-1: Start the bot (Must)
As a tester, I want to start the bot and see how to use it, so that I can log my first meal without help.
- **AC-1.1** Given a new tester, when they send `/start`, then the bot creates their account and replies with a short example of how to log a meal.
- **AC-1.2** Given an existing tester, when they send `/start` again, then no duplicate account is created and their past entries are kept.

### FR-2: Log a food item (Must)
As a tester, I want to text the bot what I ate, so that it is recorded without extra steps.
- **AC-2.1** Given a registered tester, when they send one food item with an amount (for example, "2 eggs"), then the bot saves an entry with the food, amount, calories, and time.
- **AC-2.2** Given a message with no amount (for example, "banana"), then the bot uses one standard serving and says so in the reply.

### FR-3: Look up calories (Must)
As a tester, I want the bot to find the calories for me, so that I do not have to look them up.
- **AC-3.1** Given a food that exists in the data source, when it is logged, then the saved calories match the data source value for that amount.
- **AC-3.2** Calorie values for a test set of 20 common foods are checked by hand against the data source before Cycle 1 ends. (Addresses Risk 4.)

### FR-4: See the running total (Must)
As a tester, I want to see my total after each log, so that I know where I stand for the day.
- **AC-4.1** Given a successful log, then the reply shows the calories for that item and the tester's total for today.

### FR-5: View today's log (Must)
As a tester, I want to see everything I logged today, so that I can check it.
- **AC-5.1** Given a tester with entries today, when they send `/today`, then the bot lists each entry and the total.
- **AC-5.2** Given a tester with no entries today, when they send `/today`, then the bot says nothing is logged yet.
- **AC-5.3** Entries from before midnight Central time are not included in today's total.

### FR-6: Handle unknown foods (Must)
As a tester, I want a clear answer when the bot does not recognize a food, so that I know to try again.
- **AC-6.1** Given a food not found in the data source, then nothing is saved and the bot asks the tester to rephrase.
- **AC-6.2** The bot never saves an entry with a guessed or zero calorie value.

### FR-7: Keep each tester's data separate (Must)
As a tester, I want only my entries in my log, so that my food data stays private.
- **AC-7.1** Given two testers, when each sends `/today`, then each sees only their own entries.

### FR-8: Undo the last entry (Should)
As a tester, I want to remove a mistake, so that my total stays accurate.
- **AC-8.1** Given a tester with at least one entry today, when they send `/undo`, then the most recent entry is removed and the new total is shown.

### FR-9: Enter calories manually (Should)
As a tester, I want to enter calories myself when a food is not found, so that I can still log it.
- **AC-9.1** Given an unknown food, when the tester replies with a number, then the entry is saved with that value and marked as manual.

### Later (Backlog)
Macro tracking, several foods in one message, history beyond today, calorie goals, reminders, photo or barcode input.

## Non-Functional Requirements
| ID | Requirement | How we check it |
|----|-------------|-----------------|
| NFR-1 | The bot replies within 5 seconds for a normal log | Timed during acceptance testing |
| NFR-2 | The bot supports 15 testers without errors | Tested with all testers active in the same week |
| NFR-3 | Bot token, API keys, and `.env` files never appear in the repository | `.gitignore` in place; checked in PR review |
| NFR-4 | Store only what is needed: Telegram user ID, food entries, timestamps | Reviewed against the data model |
| NFR-5 | Stays within free tiers of every service used | Usage checked weekly (Risk 5) |

## Constraints
- Must run on the Telegram Bot API.
- No paid services.
- Six part-time team members with work and other classes (Risk 7).
- Cycle 1 target end: 2026-10-18 (estimate from [Milestones](../planning/milestones.md)).
- Tester data may not be pasted into AI tools ([AI Use Policy](../ai/ai-policy.md), Section 6).

## Assumptions
- Testers use Telegram and log in English.
- All testers are in the Central time zone.
- One food item per message is acceptable to testers for Cycle 1.
- The chosen data source has a free tier large enough for 15 testers.

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-09-29 | Created Cycle 1 requirements package | Adiya |
