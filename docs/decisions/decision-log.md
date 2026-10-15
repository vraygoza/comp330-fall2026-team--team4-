# Decision Log
 
| Field | Value |
|---|---|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Khumoyun (Operations & Evidence Lead) |
| Last updated | 2026-10-15 |

This log records important team decisions and why we made them.  Architecture decisions are written up in full as ADRs in this folder and listed under D4. If a decision changes, add a new entry instead of deleting the old one.
 
 ## D1: Project Choice
 
- **Status:** Accepted — confirmed at the 2026-09-16 team meeting (all members present). See [Meeting Notes](../meeting-notes.md).
- **Decision:** Build a calorie-counter Telegram bot for a small group of friends and classmates to test and use (about 10 to 15 users).
- **Why:** We have real users available for feedback, the first version has a clear small scope (log a meal, see a daily total), and the Telegram bot API is well documented.
- **Tradeoffs:** We need to choose a nutrition data source, and users' food logs are personal data we must protect.
- **Note:** This decision records the project choice only. Which features go into Cycle 1 is a separate question tracked in OQ-1 ([Open Questions](../requirements/open-questions.md)) and the [Scope Statement](../planning/scope.md). The current S1–S8 committed items are a working assumption until OQ-1 is formally closed.

## D2: Markdown in `/docs/` as the Official Record
 
- **Status:** Accepted (Victoria, Assignment 1 kickoff email)
- **Decision:** All documents are written in Markdown and stored in the matching `/docs/` folder. The Word document submitted to Sakai only links to them.
- **Why:** The course treats the GitHub repository as the record and Markdown changes can be reviewed line by line.


## D3: Cycle 1 Scope

- **Status:** Proposed. TODO: change to Accepted, with the date, once the team closes OQ-1 at the architecture review (Victoria leads).
- **Decision:** Cycle 1 commits to S1–S8 in the [Scope Statement](../planning/scope.md), with O1 (`/undo`) and O2 (manual calories) optional. No new features are added, except FR-10 (tester access), which is privacy work the slice needs before real testers ([Requirements](../requirements/requirements.md)). The expansion ideas from the 2026-09-16 meeting go to the backlog (DF-1 to DF-7 in [Deferred Scope](deferred-scope.md)). This closes OQ-1.
- **Why:** The Must-only forecast (48 / 85 / 163 person-hours in [Estimates](../planning/estimates.md)) is well above the weekly hours confirmed so far in [Team Commitments](../planning/team-commitments.md), so there is no room for more features ([TR-1](tradeoff-records.md), Risk 7).
- **Tradeoffs:** Testers get only the core log-and-total path in Cycle 1; macros, history and the other expansion ideas wait.

## D4: Architecture Decisions (ADRs)

Each ADR records one proposed decision from [INV-01](../architecture/investigations/inv-01-lookup-storage.md) (P-1 to P-10), with its alternatives, consequences and risks. All are Proposed until the team accepts them at the architecture review.

| ADR | Decision | From | Closes | Status |
|-----|----------|------|--------|--------|
| [ADR-0001](adr-0001-no-ai-in-bot.md) | No AI behavior in the running bot | P-1 | A3 AI boundary questions | Proposed |
| [ADR-0002](adr-0002-food-data-source-and-matching.md) | USDA FoodData Central with a curated food map and strict matching | P-2, P-3 | OQ-2 | Proposed |
| [ADR-0003](adr-0003-quantity-to-grams.md) | Converting amounts to grams | P-4 | OQ-6 (quantity) | Proposed |
| [ADR-0004](adr-0004-accepted-input-forms.md) | Accepted message forms | P-5 | OQ-6 (forms) | Proposed |
| [ADR-0005](adr-0005-python-flask-webhook.md) | Python with a Flask webhook | P-6 | OQ-3 | Proposed |
| [ADR-0006](adr-0006-hosting-and-storage.md) | PythonAnywhere free web app with SQLite | P-7 | OQ-4, OQ-5 | Proposed; conditional on V-2 to V-4 |
| [ADR-0007](adr-0007-chicago-day.md) | "Today" is the Chicago calendar day | P-8 | OQ-7 | Proposed |
| [ADR-0008](adr-0008-performance-and-capacity-checks.md) | How we check the 5-second reply and 15-tester capacity | P-9, P-10 | OQ-10, OQ-11 | Proposed |

TODO: once the team accepts or changes these, update the Status column here and in each ADR, and move the closed questions to Closed Questions in [Open Questions](../requirements/open-questions.md) (Adiya).

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-09-18 | Created decision log with D1 and D2 | Mazen |
| 2026-10-14 | D1 marked Accepted; added note separating D1 from Cycle 1 scope | Khumoyun |
| 2026-10-15 | Added D3 (Cycle 1 scope, proposed) and D4 (index of ADR-0001 to ADR-0008); fixed header table | Mazen |