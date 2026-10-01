# Risk Register

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Bazid (Planning & Process Lead) |
| Last updated | 2026-10-01 |

This is a list of things that could go wrong with the project and how we plan to handle each one. We check it at every formal meeting. Anyone can add a risk through a pull request. When a risk is closed, we change its status instead of deleting it.

Risks 1 to 11 are from Assignment 1. Risks 12 to 17 were added for Cycle 1. "Linked to" shows which requirements (FR/NFR), tasks (T), and open questions (OQ) each risk affects. See [Traceability](traceability.md) for the full mapping. Owners marked "(proposed)" will be confirmed at the next meeting.

| # | Risk | Chance | Impact | Linked to | Plan | Owner | Status |
|---|------|--------|--------|-----------|------|-------|--------|
| 1 | Someone misses a deadline | High | High | All tasks | Work is due 48 hours early; every Issue gets a due date; problems get posted as 🚨 BLOCKER | Victoria | Occurred: the Assignment 2 internal deadline (09/27) was missed |
| 2 | People overwrite each other's work on GitHub | Medium | Medium | All files | Branches and pull requests; stay in your own files | Adiya | Open |
| 3 | We try to build too much and finish nothing | High | High | OQ-1, FR-8, FR-9 | Lock scope each cycle; new ideas go to the backlog; Should items are dropped first ([TR-1](../decisions/tradeoff-records.md)) | Bazid | Open |
| 4 | No nutrition data source picked yet, or calorie numbers are wrong | High | High | FR-3, OQ-2, T-1, T-13 | Choose a source early (T-1); hand-check 20 common foods (T-13) | Adiya | Open |
| 5 | Telegram or API limits or costs | Medium | Medium | NFR-5, OQ-5 | Stay on free tiers; watch usage | Adiya | Open |
| 6 | Test users' food logs or bot tokens get exposed | Low | High | FR-7, NFR-3, NFR-4 | Keep secrets out of the repo and AI tools; store as little user data as possible; if a token leaks, revoke it in BotFather right away | Mazen | Open |
| 7 | Busy schedules (work, other classes) | High | High | [Team Commitments](team-commitments.md) | Commit to Must requirements only; clear task owners; weekly WhatsApp updates | Bazid | Open: weekly hours confirmed for only 2 of 6 members |
| 8 | Docs contradict each other or don't follow the format | High | Medium | All docs | Follow the documentation standards; check links and names before tagging | Mazen | Occurred: misspelled names (fixed by Khumoyun) and links to `task-plan.md` instead of `taskplan.md` |
| 9 | Some people do more work than others | Medium | High | All tasks | Track who did what through repo evidence | Khumoyun | Open |
| 10 | AI-written work submitted without being checked | Medium | High | All docs and code | Follow the AI policy and log all AI use | Mazen | Open |
| 11 | Bugs or mistakes get through review | Medium | Medium | All code | Use the quality checklist before merging | Sohail | Open |
| 12 | Tech decisions are still open, so estimates aren't firm | High | High | OQ-2, OQ-3, OQ-4, T-1 to T-3 | Close these at the next meeting and record them in the Decision Log | Adiya (proposed) | Open |
| 13 | Understanding food messages is harder than expected | Medium | High | FR-2, OQ-6, T-9 | One food per message ([TD-1](../decisions/deferred-scope.md)); ask the tester to rephrase instead of guessing | Adiya (proposed) | Open |
| 14 | Testers can't reach the bot | Medium | High | OQ-5, T-6, NFR-2 | Decide hosting early, and decide storage at the same time | TODO: assign | Open |
| 15 | Not enough testers, or they start too late | Medium | High | OQ-8, OQ-9, T-24, T-25 | Confirm testers early; finish the onboarding notice before testing starts | Mazen (proposed) | Open |
| 16 | Estimates are wrong because this is our first cycle | High | Medium | [Effort Estimates](estimates.md) | Compare actual hours to estimates after week one; drop Should items first; record changes in re-estimation notes | Sohail (proposed) | Open |
| 17 | Most tasks have no owner, and the first three tasks all depend on one person | High | High | Task Plan (18 of 26 unassigned; T-1 to T-3 all Adiya) | Assign owners when Issues are created; Adiya's backup helps with T-1 to T-3 | Victoria (proposed) | Open |

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-09-18 | Created risk register | Bazid |
| 2026-10-01 | Added Linked to column and Risks 12 to 17; raised Risks 1, 7, and 8; ownership moved to Mazen per the Assignment 2 directions | Mazen |
