# Risk Register

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Bazid (Planning & Process Lead) |
| Last updated | 2026-10-15 |

This is a list of things that could go wrong with the project and how we plan to handle each one. We check it at every formal meeting. Anyone can add a risk through a pull request. When a risk is closed, we change its status instead of deleting it.

Risks 1 to 11 are from Assignment 1. Risks 12 to 17 were added for Cycle 1. Risks 18 to 22 come from the Assignment 3 architecture ([Architecture](../architecture/architecture.md), Section 10). "Linked to" shows which requirements (FR/NFR), tasks (T), open questions (OQ) and ADRs each risk affects; ADRs are listed under D4 in the [Decision Log](../decisions/decision-log.md). See [Traceability](traceability.md) for the full mapping. Triggers, and who watches each high-impact risk, are in the second table.

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
| 12 | Tech decisions are still open, so estimates aren't firm | High | High | OQ-2, OQ-3, OQ-4, T-1 to T-3 | Close these at the next meeting and record them in the Decision Log | Adiya | Open: eight ADRs proposed 2026-10-15 (ADR-0001 to ADR-0008) |
| 13 | Understanding food messages is harder than expected | Medium | High | FR-2, OQ-6, T-9 | One food per message ([TD-1](../decisions/deferred-scope.md)); ask the tester to rephrase instead of guessing | Adiya | Open |
| 14 | Testers can't reach the bot | Medium | High | OQ-5, T-6, NFR-2 | PythonAnywhere free + SQLite, adopted only if V-2 to V-4 pass; otherwise Render + Neon (ADR-0006) | Adiya | Open |
| 15 | Not enough testers, or they start too late | Medium | High | OQ-8, OQ-9, T-24, T-25 | Confirm testers early; finish the onboarding notice before testing starts | Mazen | Open |
| 16 | Estimates are wrong because this is our first cycle | High | Medium | [Effort Estimates](estimates.md) | Compare actual hours to estimates after week one; drop Should items first; record changes in re-estimation notes | Sohail | Open |
| 17 | Most tasks have no owner, and the first three tasks all depend on one person | High | High | Task Plan (18 of 26 unassigned; T-1 to T-3 all Adiya) | Assign owners when Issues are created; Adiya's backup helps with T-1 to T-3 | Victoria | Open |
| 18 | The chosen host doesn't fit the bot | Medium | High | ADR-0005, ADR-0006, T-6, NFR-1, AC-1.2 | Run V-2 to V-4 before building on the host; if any fails, switch to Option B and record the NFR-1 exception | Adiya | Open |
| 19 | Food matching is wrong or refuses too many messages | Medium | High | FR-3, FR-6, ADR-0002, ADR-0003, T-11, T-13 | Curated map for common foods; 25% ambiguity rule; count `AMBIGUOUS` outcomes in the test week and revisit P-3 if more than about 1 in 5 messages are refused | Adiya | Open |
| 20 | "Today" is cut at the wrong time | Low | Medium | FR-5 (AC-5.3), T-17, ADR-0007 | One Day Calculator used everywhere; midnight and daylight-saving tests | Adiya | Open: tests passed in INV-01 |
| 21 | Only one person can deploy | Medium | Medium | ADR-0006, checkpoint G-3 | Khumoyun is the backup deployer and does one practice deploy before testing starts | Adiya | Open |
| 22 | Losing the host account loses tester data | Low | High | ADR-0006, [Data and Context](../architecture/data-context.md) | Nightly backup on the host; two-factor login; accepted for Cycle 1 because backups are on the same host | Adiya | Accepted risk for Cycle 1 |

## Risk Triggers and Responsibilities

For each high-impact risk: what we would see if it starts happening, who decides what to do, who watches for it, and who confirms it is fixed.

| # | Warning sign | Decides | Watches | Confirms fixed | Fixed when |
|---|--------------|---------|---------|----------------|------------|
| 1 | Work is late or not pushed 48 hours early | Victoria | Bazid | Victoria | Ongoing |
| 3 | Someone starts a feature that isn't in Cycle 1 scope | Bazid | Victoria | Sohail | Cycle 1 ends with only the planned features |
| 4 | A calorie number doesn't match the USDA website | Adiya | Sohail | Sohail | All 20 checked foods match |
| 6 | A token, key or tester data shows up somewhere public | Mazen | Sohail | Mazen | Ongoing |
| 7 | Someone hasn't confirmed their hours or misses two weekly updates | Bazid | Bazid | Victoria | All six confirm hours that fit the plan |
| 9 | Someone has no GitHub activity for a week | Khumoyun | Khumoyun | Victoria | Ongoing |
| 10 | An AI-assisted PR has no AI log entry | Mazen | Khumoyun | Sohail | Ongoing |
| 12 | An ADR is still Proposed after the architecture review | Adiya | Mazen | Victoria | All eight ADRs are accepted or replaced |
| 13 | Message-reading tests fail, or testers often get "couldn't read that" | Adiya | Sohail | Sohail | Tests pass for every accepted form |
| 14 | The bot doesn't answer at a weekly check | Adiya | Khumoyun | Victoria | 3 outside testers can reach the bot |
| 15 | Fewer than 3 testers lined up a week before testing | Mazen | Khumoyun | Victoria | 3 outside testers have logged meals |
| 17 | A task still has no owner at a weekly check | Victoria | Bazid | Victoria | Every task has an owner |
| 18 | A host check (V-2 to V-4) fails, or entries disappear after a restart | Adiya | Khumoyun | Sohail | Host checks pass and entries survive restarts |
| 19 | More than 1 in 5 test messages get refused, or a food is matched wrong | Adiya | Sohail | Sohail | Refusals stay under 1 in 5 for the test week |
| 22 | We can't log in to the host | Adiya | Khumoyun | Mazen | Accepted for Cycle 1 |



## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-09-18 | Created risk register | Bazid |
| 2026-10-01 | Added Linked to column and Risks 12 to 17; raised Risks 1, 7, and 8; ownership moved to Mazen per the Assignment 2 directions | Mazen |
| 2026-10-15 | A2 review fixes: owner for Risk 14, removed proposed owners, added warning signs and who decides, watches and confirms each high impact risk. A3: linked Risks 12 and 14 to the ADRs; added Risks 18 to 22 from the architecture | Mazen |
