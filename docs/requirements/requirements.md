# Cycle 1 Requirements

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Last updated | 2026-10-14 |

This package covers Cycle 1 only. Scope boundaries are in the [Scope Statement](../planning/scope.md). Unresolved items are in [Open Questions](open-questions.md).

**2026-10-14 update:** criteria marked *(proposed)* come from the [INV-01 investigation](../architecture/investigations/inv-01-lookup-storage.md) and the [API Contracts](../architecture/api-contracts.md). They become committed when the team accepts the matching ADR at the architecture review. Until then the original criteria stand.

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
- **AC-2.3** *(proposed, P-5)* The bot accepts exactly these forms: `<number> <food>` ("2 eggs"), `<number>g <food>` ("150g rice cooked", also `g`, `gram` or `grams` after a space), `a <food>` or `an <food>`, and `<food>` alone. Counts from 1 to 20 (decimals allowed), grams from 1 to 2000, up to 100 characters.
- **AC-2.4** *(proposed, P-5)* Given any other form (cups, ounces, fractions such as "1/2 banana", an amount after the food such as "eggs 2", several foods), then nothing is saved and the bot replies with the accepted forms and two examples.
- **AC-2.5** *(proposed, P-4)* Every saved entry's reply states the grams used and how they were reached (for example, "2 x 1 large egg (50 g each) = 100 g").
- **AC-2.6** *(proposed, P-4)* Given a count or no amount for a food with no known portion weight, then nothing is saved and the bot asks for grams.

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
- **AC-6.3** *(proposed, P-3)* Given a food that matches several records whose calories per 100 g differ by more than 25% (for example "rice": raw or cooked), then nothing is saved and the bot lists up to 3 options and asks the tester to be more specific.
- **AC-6.4** *(proposed)* Given the data source is slow (over 3 seconds), rate-limited or unavailable, then nothing is saved and the bot asks the tester to try again later.

### FR-7: Keep each tester's data separate (Must)
As a tester, I want only my entries in my log, so that my food data stays private.
- **AC-7.1** Given two testers, when each sends `/today`, then each sees only their own entries.

### FR-8: Undo the last entry (Should)
As a tester, I want to remove a mistake, so that my total stays accurate.
- **AC-8.1** Given a tester with at least one entry today, when they send `/undo`, then the most recent entry is removed and the new total is shown.

### FR-9: Enter calories manually (Should)
As a tester, I want to enter calories myself when a food is not found, so that I can still log it.
- **AC-9.1** Given an unknown food, when the tester replies with a number, then the entry is saved with that value and marked as manual.

### FR-10: Tester access (Must, proposed)
As the team, we want only invited testers who have seen the data notice to create accounts, so that we collect food data only from people who agreed to it. (Closes [Traceability](../planning/traceability.md) gap G-1; decision owners for G6: Adiya, Khumoyun and Mazen.)
- **AC-10.1** Given a person who opens the bot through the team's invite link, when they send `/start`, then the account is created and the reply links to `/privacy`.
- **AC-10.2** Given a person without a valid invite, when they send `/start` or any message, then no account or entry is created and the bot replies that it is in a closed test.
- **AC-10.3** Given any registered tester, when they send `/privacy`, then the bot states what is stored, why, how long it is kept and how to ask for deletion.

### Later (Backlog)
Macro tracking, several foods in one message, history beyond today, calorie goals, reminders, photo or barcode input.

## Non-Functional Requirements
| ID | Requirement | How we check it |
|----|-------------|-----------------|
| NFR-1 | The bot replies within 5 seconds for a normal log | *(Proposed, P-9)* Measured from webhook receipt to the reply call returning, **including the food lookup**. Pass: 95% of logged messages in the test week at 5 seconds or less in the operations log, and 10 manual phone trials all at 5 seconds or less |
| NFR-2 | The bot supports 15 testers without errors | *(Proposed, P-10)* Capacity check: 15 synthetic tester IDs, 10 messages each, through the handler with 0 errors and no cross-tester data. Real use by every enrolled tester in the test week. This is separate from the Definition of Done, which needs at least 3 real outside testers |
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
- All testers are in the Central time zone. "Today" is the Chicago calendar day, including 23 and 25 hour days when daylight saving starts or ends (Nov 1, 2026 falls in Cycle 1 testing). *(Proposed, P-8)*
- One food item per message is acceptable to testers for Cycle 1.
- The chosen data source has a free tier large enough for 15 testers.

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-09-29 | Created Cycle 1 requirements package | Adiya |
| 2026-10-14 | Added proposed AC-2.3 to AC-2.6, AC-6.3, AC-6.4, FR-10, and measurable checks for NFR-1 and NFR-2 from INV-01 | Adiya |
