# Risk Register

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Bazid (Planning & Process Lead) |
| Last updated | 2026-11-03 |
| Last updated | 2026-11-09 |

This is a list of things that could go wrong with the project and how we plan to handle each one. We check it at every formal meeting. Anyone can add a risk through a pull request. When a risk is closed, we change its status instead of deleting it.

Risks 1 to 11 are from Assignment 1. Risks 12 to 17 were added for Cycle 1. Risks 18 to 22 come from the Assignment 3 architecture ([Architecture](../architecture/architecture.md), Section 10). "Linked to" shows which requirements (FR/NFR), tasks (T), open questions (OQ) and ADRs each risk affects; ADRs are listed under D4 in the [Decision Log](../decisions/decision-log.md). See [Traceability](traceability.md) for the full mapping. Triggers, and who watches each high-impact risk, are in the second table.

Risk 23 was added for the Cycle 1 release (Assignment 5). Statuses were re-checked against `main` (tag `a4-construction-integration`) on 2026-11-09, and the third table gives each risk's next action and who does it.

| # | Risk | Chance | Impact | Linked to | Plan | Owner | Status |
|---|------|--------|--------|-----------|------|-------|--------|
| 1 | Someone misses a deadline | High | High | All tasks | Work is due 48 hours early; every Issue gets a due date; problems get posted as 🚨 BLOCKER | Victoria | Occurred: the Assignment 2 internal deadline (09/27) was missed, and at the Assignment 4 snapshot (11/02) eight deliverables were still Not started ([A4 evidence package](../reviews/assignment4-review-package.md)) |
| 2 | People overwrite each other's work on GitHub | Medium | Medium | All files | Branches and pull requests; stay in your own files | Adiya | Occurred: merge conflicts in `ai-use-log.md` on 11/02 were resolved by keeping one side, which dropped other members' rows (Risk 10) |
| 3 | We try to build too much and finish nothing | High | High | OQ-1, FR-8, FR-9 | Lock scope each cycle; new ideas go to the backlog; Should items are dropped first ([TR-1](../decisions/tradeoff-records.md)) | Bazid | Open: nothing outside Cycle 1 scope has been built; the optional `/undo` and manual calories were not started |
| 4 | No nutrition data source picked yet, or calorie numbers are wrong | High | High | FR-3, OQ-2, T-1, T-13 | Choose a source early (T-1); hand-check 20 common foods (T-13) | Adiya | Open: FDC is not connected yet; the bot uses eight made-up sample foods (CC-1 in [Architecture](../architecture/architecture.md), Section 11). V-1 and T-13 have not run |
| 5 | Telegram or API limits or costs | Medium | Medium | NFR-5, OQ-5 | Stay on free tiers; watch usage | Adiya | Open: not exercised, because the bot is not deployed (Risk 14) |
| 6 | Test users' food logs or bot tokens get exposed | Low | High | FR-7, NFR-3, NFR-4 | Keep secrets out of the repo and AI tools; store as little user data as possible; if a token leaks, revoke it in BotFather right away | Mazen | Open: the CI secrets check runs on every pull request since #73. It checks current files only, so on 2026-11-09 the full history of every branch (180 commits) was scanned with the same patterns: no tokens or secret files found |
| 7 | Busy schedules (work, other classes) | High | High | [Team Commitments](team-commitments.md) | Commit to Must requirements only; clear task owners; weekly WhatsApp updates | Bazid | Open: weekly hours confirmed for only 2 of 6 members |
| 8 | Docs contradict each other or don't follow the format | High | Medium | All docs | Follow the documentation standards; check links and names before tagging | Mazen | Occurred again: the A3 feedback (reviewed 10/26) found contradictory records; `ci.yml` and `requirements.txt` pointed to ADR-0009 before it existed |
| 9 | Some people do more work than others | Medium | High | All tasks | Track who did what through repo evidence | Khumoyun | Open |
| 10 | AI-written work submitted without being checked | Medium | High | All docs and code | Follow the AI policy and log all AI use | Mazen | Open |
| 11 | Bugs or mistakes get through review | Medium | Medium | All code | Use the quality checklist before merging | Bazid (acting) | Open |
| 12 | Tech decisions are still open, so estimates aren't firm | High | High | OQ-2, OQ-3, OQ-4, T-1 to T-3 | Close these at the next meeting and record them in the Decision Log | Adiya | Open: eight ADRs proposed 2026-10-15 (ADR-0001 to ADR-0008) |
| 13 | Understanding food messages is harder than expected | Medium | High | FR-2, OQ-6, T-9 | One food per message ([TD-1](../decisions/deferred-scope.md)); ask the tester to rephrase instead of guessing | Adiya | Open |
| 14 | Testers can't reach the bot | Medium | High | OQ-5, T-6, NFR-2 | PythonAnywhere free + SQLite, adopted only if V-2 to V-4 pass; otherwise Render + Neon (ADR-0006) | Adiya | Open |
| 15 | Not enough testers, or they start too late | Medium | High | OQ-8, OQ-9, T-24, T-25 | Confirm testers early; finish the onboarding notice before testing starts | Mazen | Open |
| 16 | Estimates are wrong because this is our first cycle | High | Medium | [Effort Estimates](estimates.md) | Compare actual hours to estimates after week one; drop Should items first; record changes in re-estimation notes | Bazid | Open |
| 17 | Most tasks have no owner, and the first three tasks all depend on one person | High | High | Task Plan (18 of 26 unassigned; T-1 to T-3 all Adiya) | Assign owners when Issues are created; Adiya's backup helps with T-1 to T-3 | Victoria | Open |
| 18 | The chosen host doesn't fit the bot | Medium | High | ADR-0005, ADR-0006, T-6, NFR-1, AC-1.2 | Run V-2 to V-4 before building on the host; if any fails, switch to Option B and record the NFR-1 exception | Adiya | Open |
| 19 | Food matching is wrong or refuses too many messages | Medium | High | FR-3, FR-6, ADR-0002, ADR-0003, T-11, T-13 | Curated map for common foods; 25% ambiguity rule; count `AMBIGUOUS` outcomes in the test week and revisit P-3 if more than about 1 in 5 messages are refused | Adiya | Open |
| 20 | "Today" is cut at the wrong time | Low | Medium | FR-5 (AC-5.3), T-17, ADR-0007 | One Day Calculator used everywhere; midnight and daylight-saving tests | Adiya | Open: tests passed in INV-01 |
| 21 | Only one person can deploy | Medium | Medium | ADR-0006, checkpoint G-3 | Khumoyun is the backup deployer and does one practice deploy before testing starts | Adiya | Open |
| 22 | Losing the host account loses tester data | Low | High | ADR-0006, [Data and Context](../architecture/data-context.md) | Nightly backup on the host; two-factor login; accepted for Cycle 1 because backups are on the same host | Adiya | Accepted risk for Cycle 1 |
| 23 | Team member departure mid-cycle | High | High | T-13, T-22, T-23, T-26 | Sohail departed 10/30; Bazid acting Quality Lead; reassign tasks to remaining 5 members | Victoria | Occurred (10/30): tasks marked for reassignment |
| 10 | AI-written work submitted without being checked | Medium | High | All docs and code | Follow the AI policy and log all AI use | Mazen | Occurred: the AI-use rows for five merged Assignment 4 PRs (#73, #77, #83, #84, #88) are missing from the log on `main`, lost in merge conflicts (Risk 2). Open PR #89 restores them |
| 11 | Bugs or mistakes get through review | Medium | Medium | All code | Use the quality checklist before merging | Sohail | Open: CI runs the tests on every pull request since #73 (66 tests on `main`). PRs merged before #73 had no CI check |
| 12 | Tech decisions are still open, so estimates aren't firm | High | High | OQ-2, OQ-3, OQ-4, T-1 to T-3 | Close these at the next meeting and record them in the Decision Log | Adiya | Closed: ADR-0001 to ADR-0009 accepted by team vote on 2026-11-09 (#56); ADR-0002 and ADR-0006 stay conditional on V-1 and V-2 to V-4 |
| 13 | Understanding food messages is harder than expected | Medium | High | FR-2, OQ-6, T-9 | One food per message ([TD-1](../decisions/deferred-scope.md)); ask the tester to rephrase instead of guessing | Adiya | Open: parser merged (#88); its 22 unit and contract tests pass in CI |
| 14 | Testers can't reach the bot | Medium | High | OQ-5, T-6, NFR-2 | PythonAnywhere free + SQLite, adopted only if V-2 to V-4 pass; otherwise Render + Neon (ADR-0006) | Adiya | Occurred for Cycle 1: the bot is not deployed. V-2 to V-4 have not run, and deployment waits for T-30 (Risk 23) |
| 15 | Not enough testers, or they start too late | Medium | High | OQ-8, OQ-9, T-24, T-25 | Confirm testers early; finish the onboarding notice before testing starts | Mazen | Occurred for Cycle 1: no outside testers, because the bot is not deployed (Risk 14). T-25 (onboarding notice) and T-29 (invite check, `/privacy`) are not started |
| 16 | Estimates are wrong because this is our first cycle | High | Medium | [Effort Estimates](estimates.md) | Compare actual hours to estimates after week one; drop Should items first; record changes in re-estimation notes | Sohail | Occurred: the integration pull request planned for Assignment 4 (#50) moved to Assignment 5 (PR #90) |
| 17 | Most tasks have no owner, and the first three tasks all depend on one person | High | High | Task Plan (18 of 26 unassigned; T-1 to T-3 all Adiya) | Assign owners when Issues are created; Adiya's backup helps with T-1 to T-3 | Victoria | Open: T-30, T-31, T-32 (live check), T-33 and T-35 have no owner in [Task Plan](task-plan.md). Architecture Section 11 names Khumoyun for T-30; the task plan does not |
| 18 | The chosen host doesn't fit the bot | Medium | High | ADR-0005, ADR-0006, T-6, NFR-1, AC-1.2 | Run V-2 to V-4 before building on the host; if any fails, switch to Option B and record the NFR-1 exception | Adiya | Open: V-2 to V-4 have not run |
| 19 | Food matching is wrong or refuses too many messages | Medium | High | FR-3, FR-6, ADR-0002, ADR-0003, T-11, T-13 | Curated map for common foods; 25% ambiguity rule; count `AMBIGUOUS` outcomes in the test week and revisit P-3 if more than about 1 in 5 messages are refused | Adiya | Open: the lookup refuses unknown foods and partial matches (8 tests in CI); the real refusal rate is unknown until testers use the bot |
| 20 | "Today" is cut at the wrong time | Low | Medium | FR-5 (AC-5.3), T-17, ADR-0007 | One Day Calculator used everywhere; midnight and daylight-saving tests | Adiya | Mitigated: Day Calculator merged (#83); midnight and daylight-saving tests pass in CI |
| 21 | Only one person can deploy | Medium | Medium | ADR-0006, checkpoint G-3 | Khumoyun is the backup deployer and does one practice deploy before testing starts | Adiya | Open: no practice deploy yet, because nothing is deployed |
| 22 | Losing the host account loses tester data | Low | High | ADR-0006, [Data and Context](../architecture/data-context.md) | Nightly backup on the host; two-factor login; accepted for Cycle 1 because backups are on the same host | Adiya | Accepted risk for Cycle 1. No tester data exists yet, because the bot is not deployed |
| 23 | A Telegram resend logs the same meal twice | Medium | Medium | C-1, T-30, ADR-0005, CC-5 in [Architecture](../architecture/architecture.md), Section 11 | Do not deploy until T-30 (duplicate `update_id` check) merges | Adiya |Open: T-30 is not built and has no owner yet (Architecture Section 11 names Khumoyun; the Task Plan does not, Risk 17). The bot runs only on a developer's computer |

## Risk Triggers and Responsibilities

For each high-impact risk: what we would see if it starts happening, who decides what to do, who watches for it, and who confirms it is fixed.

| # | Warning sign | Decides | Watches | Confirms fixed | Fixed when |
|---|--------------|---------|---------|----------------|------------|
| 1 | Work is late or not pushed 48 hours early | Victoria | Bazid | Victoria | Ongoing |
| 3 | Someone starts a feature that isn't in Cycle 1 scope | Bazid | Victoria | Bazid (acting) | Cycle 1 ends with only the planned features |
| 4 | A calorie number doesn't match the USDA website | Adiya | Bazid | Adiya | All 20 checked foods match |
| 6 | A token, key or tester data shows up somewhere public | Mazen | Mazen | Mazen | Ongoing |
| 7 | Someone hasn't confirmed their hours or misses two weekly updates | Bazid | Bazid | Victoria | All five confirm hours that fit the plan |
| 9 | Someone has no GitHub activity for a week | Khumoyun | Khumoyun | Victoria | Ongoing |
| 10 | An AI-assisted PR has no AI log entry | Mazen | Khumoyun | Bazid (acting) | Ongoing |
| 12 | An ADR is still Proposed after the architecture review | Adiya | Mazen | Victoria | All eight ADRs are accepted or replaced |
| 13 | Message-reading tests fail, or testers often get "couldn't read that" | Adiya | Adiya | Bazid (acting) | Tests pass for every accepted form |
| 14 | The bot doesn't answer at a weekly check | Adiya | Khumoyun | Victoria | 3 outside testers can reach the bot |
| 15 | Fewer than 3 testers lined up a week before testing | Mazen | Khumoyun | Victoria | 3 outside testers have logged meals |
| 17 | A task still has no owner at a weekly check | Victoria | Bazid | Victoria | Every task has an owner |
| 18 | A host check (V-2 to V-4) fails, or entries disappear after a restart | Adiya | Khumoyun | Bazid (acting) | Host checks pass and entries survive restarts |
| 19 | More than 1 in 5 test messages get refused, or a food is matched wrong | Adiya | Adiya | Bazid (acting) | Refusals stay under 1 in 5 for the test week |
| 22 | We can't log in to the host | Adiya | Khumoyun | Mazen | Accepted for Cycle 1 |
| 23 | Team member departure leaves tasks or role vacant | Victoria | Victoria | Victoria | All unassigned tasks reassigned to the 5 members |



## Next Actions (Cycle 1 Release)

Checked 2026-11-09. "Before the A5 tag" means before the `a5-cycle1-release` tag on 2026-11-10. Cycle 2 items also go into the Assignment 5 Cycle 2 handoff.

| # | Next action | Who | When |
|---|-------------|-----|------|
| 1 | Drafts open as pull requests by Monday 9 PM, everything merged by Tuesday noon (A5 task list) | Victoria | Before the A5 tag |
| 2 | When resolving a merge conflict in a shared file, keep both sides; ask the file owner if unsure | Everyone | Ongoing |
| 3 | Pick Cycle 2 work from the Cycle 1 handoff, not from new ideas | Bazid | Cycle 2 planning |
| 4 | Run V-1, build the FDC adapter, and hand-check 20 foods (T-13) | Adiya | Cycle 2 |
| 5 | Start the weekly health check (T-28) once the bot is deployed | Adiya | After deployment |
| 6 | Re-run the history scan and `pip-audit` before deployment; if a token ever appears, revoke it in BotFather | Mazen | Before deployment |
| 7 | Confirm weekly hours for Cycle 2 | Bazid | Cycle 2 planning |
| 8 | Check the release documents against `main` for contradictions (dates, statuses, owners, links) | Mazen | Before the A5 tag |
| 9 | Peer reviews submitted privately in Sakai; contribution stays visible through PR authors and reviewers | Everyone | 2026-11-10, noon |
| 10 | Restore the five missing AI-use rows on `main`; every Assignment 5 PR adds its own row, and reviewers check for it | Khumoyun (log owner), Mazen | Before the A5 tag |
| 11 | Every PR approved by someone other than the author, with the CI check green | Each reviewer | Ongoing |
| 12 | Update ADR-0001 to ADR-0008 to the #56 vote result | Adiya | Before the A5 tag |
| 13 | Count "couldn't read that" replies once testers start | Adiya | Test week |
| 14 | T-30, then V-2 to V-4 on PythonAnywhere, then the T-34 smoke test | Adiya, with the T-30 owner | Cycle 2 |
| 15 | Finish T-25 (onboarding notice) and T-29 (invite check, `/privacy`), then line up 3 outside testers | Mazen | Before deployment |
| 16 | Compare actual hours with the estimates in [Re-estimation](re-estimation.md) | Bazid | Cycle 2 planning |
| 17 | Assign owners to the tasks listed in Risk 17, and make the Task Plan and Architecture Section 11 agree on T-30 | Victoria | Cycle 2 planning |
| 18 | Same as Risk 14 | Adiya | Cycle 2 |
| 19 | Count refusals during the test week; revisit P-3 if more than about 1 in 5 messages are refused | Adiya | Test week |
| 20 | None beyond keeping the day tests in CI | Adiya | Ongoing |
| 21 | Khumoyun does one practice deploy before testers start | Khumoyun | Before testers |
| 22 | Revisit when the bot is deployed and holds tester data | Adiya | After deployment |
| 23 | Build T-30 with a unit test that sends the same `update_id` twice | T-30 owner (Risk 17) | Before deployment |

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-09-18 | Created risk register | Bazid |
| 2026-10-01 | Added Linked to column and Risks 12 to 17; raised Risks 1, 7, and 8; ownership moved to Mazen per the Assignment 2 directions | Mazen |
| 2026-10-15 | A2 review fixes: owner for Risk 14, removed proposed owners, added warning signs and who decides, watches and confirms each high impact risk. A3: linked Risks 12 and 14 to the ADRs; added Risks 18 to 22 from the architecture | Mazen |
| 2026-11-03 | Added Risk 23 for team member departure (Sohail); reassigned former Quality Lead risk responsibilities to Bazid (acting); updated Risk 7 to 5 members | Mazen, Khumoyun |
| 2026-11-09 | Cycle 1 release review: re-checked statuses against `main`, added Risk 23 and the Next Actions table, added the full-history secrets scan result (Risk 6) | Mazen |
