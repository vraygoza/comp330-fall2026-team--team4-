# Open Questions

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Last updated | 2026-11-09 |

Questions the team must answer before or during Cycle 1. When a question is closed, record the answer and link the Decision Log entry. Do not delete closed questions.

"Blocks" means implementation of that requirement cannot start until the question is answered.

| ID | Question | Blocks | Proposed owner | Needed by | Status |
|----|----------|--------|----------------|-----------|--------|
| OQ-8 | What do we tell testers about the data we collect, and how do they ask to have it deleted? | Tester onboarding | Mazen, with Adiya and Khumoyun (G6) | Before tester onboarding | Open. Architecture provides `/privacy` (AC-10.3) and deletion checkpoint G-5; the notice text and retention period are still needed |
| OQ-9 | Which testers have agreed to participate, and when do they start? | Cycle 1 Definition of Done | Khumoyun (proposed; tester recruitment in the action plan) | Before tester onboarding | Open |

"Proposed answer" means the question stays open until the team accepts the decision at the architecture review. The accepted decision is then recorded as an ADR in [`/docs/decisions/`](../decisions/), the row moves to Closed Questions, and the [Decision Log](../decisions/decision-log.md) links the ADR.

## Closed Questions
| ID | Question | Answer | Decision | Date |
|----|----------|--------|----------|------|
| OQ-1 | The 2026-09-16 meeting asked the team to expand the project scope. Which added features, if any, go in Cycle 1, and which go to the backlog? | Cycle 1 shipped `/start` and food logging with a daily total on sample data; other added features go to the backlog. What did not ship is in the release notes | [D3](../decisions/decision-log.md) | 2026-11-09 (team vote, #56) |
| OQ-2 | Which nutrition data source will we use? | USDA FoodData Central with a curated food map, conditional on live check V-1. Cycle 1 uses a sample list until then | [ADR-0002](../decisions/adr-0002-food-data-source-and-matching.md) | 2026-11-09 (team vote, #56) |
| OQ-3 | Which programming language and Telegram bot library? | Python 3.12 or later, Flask webhook, thin Telegram adapter | [ADR-0005](../decisions/adr-0005-python-flask-webhook.md), [ADR-0009](../decisions/adr-0009-dependencies.md) | 2026-11-09 (team vote, #56) |
| OQ-4 | Where is tester data stored? | SQLite behind one storage module (built in #90) | [ADR-0006](../decisions/adr-0006-hosting-and-storage.md) | 2026-11-09 (team vote, #56) |
| OQ-5 | Where does the bot run so testers can reach it at any time? | PythonAnywhere free web app, conditional on checks V-2 to V-4 (not run; the bot is not deployed) | [ADR-0006](../decisions/adr-0006-hosting-and-storage.md) | 2026-11-09 (team vote, #56) |
| OQ-6 | What input format do we accept? What happens with units we do not recognize? | The forms in ADR-0004 (built in #88). Unrecognized units are refused with the accepted-forms reply; grams are converted per ADR-0003 once FDC data exists | [ADR-0003](../decisions/adr-0003-quantity-to-grams.md), [ADR-0004](../decisions/adr-0004-accepted-input-forms.md) | 2026-11-09 (team vote, #56) |
| OQ-7 | Is "today" always Central time, or do we need each tester's time zone? | Chicago calendar day for everyone, stored in UTC (built in #83 and #90) | [ADR-0007](../decisions/adr-0007-chicago-day.md) | 2026-11-09 (team vote, #56) |
| OQ-10 | Does lookup time count toward the 5-second target (NFR-1)? | Yes: measured from receipt to reply, lookup included. Not measured yet; needs a deployed bot | [ADR-0008](../decisions/adr-0008-performance-and-capacity-checks.md) | 2026-11-09 (team vote, #56) |
| OQ-11 | How do "3 outside testers" (Definition of Done) and "supports 15 testers" (NFR-2) relate? | 3 real outside testers for the Definition of Done; 15 testers checked synthetically (NFR-2). Not run yet; needs a deployed bot | [ADR-0008](../decisions/adr-0008-performance-and-capacity-checks.md) | 2026-11-09 (team vote, #56) |

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-09-29 | Created open questions | Adiya |
| 2026-10-14 | Added proposed answers from INV-01 for OQ-1 to OQ-7; added OQ-10 and OQ-11; proposed owners for OQ-5 and OQ-9 | Adiya |
| 2026-11-09 | Closed OQ-1 to OQ-7, OQ-10 and OQ-11 after the team vote accepted D3 and ADR-0001 to ADR-0009 (#56); OQ-8 and OQ-9 stay open | Adiya |
