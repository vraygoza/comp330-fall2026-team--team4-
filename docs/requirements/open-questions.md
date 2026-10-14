# Open Questions

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Last updated | 2026-10-14 |

Questions the team must answer before or during Cycle 1. When a question is closed, record the answer and link the Decision Log entry. Do not delete closed questions.

"Blocks" means implementation of that requirement cannot start until the question is answered.

| ID | Question | Blocks | Proposed owner | Needed by | Status |
|----|----------|--------|----------------|-----------|--------|
| OQ-1 | The 2026-09-16 meeting asked the team to expand the project scope. Which added features, if any, go in Cycle 1, and which go to the backlog? | Scope lock | Whole team (Victoria leads) | Architecture review meeting | Open. **Proposed answer (Adiya):** add no new features to Cycle 1. The architecture and the capacity numbers (11 confirmed weekly hours against a 48/85/163 hour Must-only forecast) leave no room. The only addition is FR-10 (tester access), which is privacy work the slice needs before real users. Expansion ideas go to [Deferred Scope](../decisions/deferred-scope.md) |
| OQ-2 | Which nutrition data source will we use? | FR-3 | Adiya | Architecture review | **Proposed answer:** USDA FoodData Central, Foundation and SR Legacy only, with a curated food map from T-13 and a strict search fallback (P-2, P-3 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). Live check V-1 still needed |
| OQ-3 | Which programming language and Telegram bot library? | All FRs | Adiya | Architecture review | **Proposed answer:** Python 3.10 or later; Flask webhook with a thin Telegram adapter (P-6). Changed from the A2 recommendation because of the hosting finding |
| OQ-4 | Where is tester data stored? | FR-2, FR-5, FR-7 | Adiya | Architecture review | **Proposed answer:** SQLite on the host's persistent disk, behind one storage module (P-7). Decided together with OQ-5 |
| OQ-5 | Where does the bot run so testers can reach it at any time? | Tester onboarding | Adiya (proposed; was unassigned) with Khumoyun for V-2 to V-4 | Before tester onboarding | **Proposed answer:** PythonAnywhere free web app, conditional on V-2 to V-4. Fallback: Render free plus Neon free Postgres (P-7) |
| OQ-6 | What input format do we accept? What happens with units we do not recognize? | FR-2 | Adiya | Before FR-2 work starts | **Proposed answer:** AC-2.3 to AC-2.6 in [Requirements](requirements.md) (P-4, P-5). Tested in the spike |
| OQ-7 | Is "today" always Central time, or do we need each tester's time zone? | FR-5 | Adiya with Sohail | Before FR-5 work starts | **Proposed answer:** Chicago calendar day for everyone; UTC storage; 23 and 25 hour days handled (P-8). Midnight and daylight-saving checks pass in the spike |
| OQ-8 | What do we tell testers about the data we collect, and how do they ask to have it deleted? | Tester onboarding | Mazen, with Adiya and Khumoyun (G6) | Before tester onboarding | Open. Architecture provides `/privacy` (AC-10.3) and deletion checkpoint G-5; the notice text and retention period are still needed |
| OQ-9 | Which testers have agreed to participate, and when do they start? | Cycle 1 Definition of Done | Khumoyun (proposed; tester recruitment in the action plan) | Before tester onboarding | Open |
| OQ-10 | Does lookup time count toward the 5-second target (NFR-1)? | NFR-1, T-23 | Adiya with Sohail | Architecture review | **Proposed answer:** yes. Measured from webhook receipt to reply, lookup included (P-9) |
| OQ-11 | How do "3 outside testers" (Definition of Done) and "supports 15 testers" (NFR-2) relate? | NFR-2, T-24 | Adiya with Sohail | Architecture review | **Proposed answer:** 3 real outside testers is the Definition of Done; 15 is a capacity check with synthetic tester IDs (P-10) |

"Proposed answer" means the question stays open until the team accepts the decision at the architecture review. The accepted decision is then recorded as an ADR in [`/docs/decisions/`](../decisions/), the row moves to Closed Questions, and the [Decision Log](../decisions/decision-log.md) links the ADR.

## Closed Questions
| ID | Question | Answer | Decision | Date |
|----|----------|--------|----------|------|
| | | | | |

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-09-29 | Created open questions | Adiya |
| 2026-10-14 | Added proposed answers from INV-01 for OQ-1 to OQ-7; added OQ-10 and OQ-11; proposed owners for OQ-5 and OQ-9 | Adiya |
