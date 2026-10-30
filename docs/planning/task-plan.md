# Task Plan

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-10-30 |

Cycle 1 work broken into tasks. Each task traces to a requirement in [Requirements](../requirements/requirements.md). Estimates are in [Effort Estimates](estimates.md) and [Re-estimation Notes](re-estimation.md).

Task IDs are governed by [Task ID Map](task-id-map.md). Do not create a new ID without adding it there first.

Cycle 1 vertical slice: a tester sends one food item, the bot finds the calories, saves the entry, and replies with the daily total.

## Setup Tasks
These come before any requirement work and are blocked by open questions.

| ID | Task | Traces to | Depends on | Owner | Status |
|----|------|-----------|------------|-------|--------|
| T-1 | Choose nutrition data source and confirm free tier | FR-3, NFR-5 | OQ-2 | Adiya | Not started |
| T-2 | Choose language and Telegram bot library | All FRs | OQ-3 | Adiya | Not started |
| T-3 | Choose data storage and design the data model | FR-2, FR-5, FR-7, NFR-4 | OQ-4 | Adiya | Not started |
| T-4 | Set up repo scaffolding, `.gitignore`, and secrets handling | NFR-3 | T-2 | TODO: assign | Not started |
| T-5 | Register the bot and get a working token in a dev environment | FR-1 | T-2 | TODO: assign | Not started |
| T-6 | Decide where the bot runs so testers can reach it anytime | Tester onboarding | OQ-5 | TODO: assign | Not started |

## Must Requirements
| ID | Task | Traces to | Depends on | Owner | Status |
|----|------|-----------|------------|-------|--------|
| T-7 | Handle `/start`: create account, send usage example | FR-1 (AC-1.1) | T-3, T-5 | TODO: assign | Not started |
| T-8 | Make repeat `/start` safe: no duplicate account, keep entries | FR-1 (AC-1.2) | T-7 | TODO: assign | Not started |
| T-9 | Parse a message into food and amount | FR-2 (AC-2.1) | T-2, OQ-6 | TODO: assign | Not started |
| T-10 | Default to one standard serving when no amount is given, and say so | FR-2 (AC-2.2) | T-9 | TODO: assign | Not started |
| T-11 | Query the data source and scale calories to the amount | FR-3 (AC-3.1) | T-1, T-9 | TODO: assign | Not started |
| T-12 | Save the entry with food, amount, calories, and timestamp | FR-2 (AC-2.1) | T-3, T-11 | TODO: assign | Not started |
| T-13 | Build and verify the curated food map (reviewed word to FDC record and portion) | FR-3 (AC-3.2), P-2 | T-11, V-1 | TODO: reassign | Not started |
| T-14 | Calculate and reply with the daily running total | FR-4 (AC-4.1) | T-12 | TODO: assign | Not started |
| T-15 | Build `/today`: list entries plus total | FR-5 (AC-5.1) | T-12 | TODO: assign | Not started |
| T-16 | Handle empty `/today` with a clear message | FR-5 (AC-5.2) | T-15 | TODO: assign | Not started |
| T-17 | Cut the day at midnight Central | FR-5 (AC-5.3) | T-14, OQ-7 | TODO: assign | Not started |
| T-18 | Handle unknown foods: save nothing, ask to rephrase | FR-6 (AC-6.1, AC-6.2) | T-11 | TODO: assign | Not started |
| T-19 | Scope every query to the requesting Telegram user ID | FR-7 (AC-7.1) | T-3, T-12 | TODO: assign | Not started |

## Should Requirements
Only started if every Must task is done.

| ID | Task | Traces to | Depends on | Owner | Status |
|----|------|-----------|------------|-------|--------|
| T-20 | Build `/undo` to remove the last entry and show the new total | FR-8 (AC-8.1) | T-12, T-14 | TODO: assign | Not started |
| T-21 | Accept a manual calorie number after an unknown food | FR-9 (AC-9.1) | T-18 | TODO: assign | Not started |

## Testing and Release
| ID | Task | Traces to | Depends on | Owner | Status |
|----|------|-----------|------------|-------|--------|
| T-22 | Write acceptance tests for every Must acceptance criterion | All Must FRs | T-7 through T-19 | TODO: reassign | Not started |
| T-23 | Time responses to confirm the 5-second target | NFR-1 | T-14 | TODO: reassign | Not started |
| T-24 | Test with 15 testers active in one week | NFR-2 | T-19, OQ-9 | TODO: assign | Not started |
| T-25 | Write tester onboarding and data-handling notice | Tester onboarding | OQ-8 | Mazen | Not started |
| T-26 | Confirm no secrets in the repo before release | NFR-3 | T-4 | TODO: reassign | Not started |

## Governance and Operations Tasks
IDs reconciled 2026-10-30 per [Task ID Map](task-id-map.md). T-27 to T-29 come from [Traceability](traceability.md); T-30 to T-35 were renumbered from the A3 additions.

| ID | Task | Traces to | Depends on | Owner | Status |
|----|------|-----------|------------|-------|--------|
| T-27 | Review the database tables against NFR-4 before the Entry Store merges | NFR-4 | T-3 | Mazen | Not started |
| T-28 | Weekly health check: outcome counts, reply times and FDC calls per hour against free-tier limits | NFR-5, Risk 5 | T-11 | Adiya | Not started |
| T-29 | Build the tester invite check and the `/privacy` reply | FR-10 (AC-10.1 to AC-10.3), OQ-8, G-4 | T-7, OQ-1 | Mazen | Not started |
| T-30 | Record processed `update_id` values in the same transaction as the entry | C-1, INV-01 Finding 7 | T-3, T-12 | TODO: assign | Not started |
| T-31 | Build `food_cache` table, loader, and 30-day refresh rule | C-5, INV-01 Finding 8 | T-1, T-3 | TODO: assign | Not started |
| T-32 | Check `X-Telegram-Bot-Api-Secret-Token`; return 403 and log AUTH_REJECTED | C-1, TB-1 | T-5 | TODO: assign | Unit tests merged in #69; live check remains (V-3) |
| T-33 | Write and test the per-tester deletion script | OQ-8, C-6, G-5 | T-3 | TODO: assign | Not started |
| T-34 | Deploy smoke test: `/start`, `2 eggs`, `/today` on a dev account | G-3 | T-6, T-14 | Adiya | Not started |
| T-35 | Nightly `sqlite3 .backup` of `bot.db` on the host | architecture.md section 8 | T-6 | TODO: assign | Not started |

Done criteria for T-27, T-28, T-29, T-30, T-32 and T-33 are in the [Task ID Map](task-id-map.md).

## Verification Tasks (INV-01)
These close the blocking decisions.

| ID | Task | Closes | Owner | Status |
|----|------|--------|-------|--------|
| V-1 | Live FDC run of the 20 T-13 foods | P-2, P-3 | Adiya | Not started |
| V-2 | Reach `api.telegram.org` and `api.nal.usda.gov` from PythonAnywhere | P-6, P-7 | Khumoyun (proposed) | Not started |
| V-3 | Register test bot, set webhook with secret, send `/start` | P-7 | Khumoyun (proposed) | Not started |
| V-4 | Write an entry, reload the web app, read it back | P-7 | Khumoyun (proposed) | Not started |
| V-5 | Read `X-RateLimit-Remaining` from the host | Finding 8 | Adiya | Not started |
| V-6 | Time 20 FDC searches from the host | NFR-1, P-9 | Adiya | Not started |

**V-2 is the highest-priority verification item.** If PythonAnywhere blocks `api.telegram.org`, P-6 and P-7 both change and estimates for T-2, T-6 and every hosting-dependent task are revised again.

## Team Change, 2026-10-30
Sohail is no longer on the team. The team is now five members. His tasks are marked `TODO: reassign` above: T-13, T-22, T-23 and T-26.

Quality & Review Lead is vacant. Bazid is the charter backup and is acting in that role for Cycle 1.

Capacity drops from six part-time members to five. [Team Commitments](team-commitments.md) and [Re-estimation Notes](re-estimation.md) need updating before the schedule is used for planning.

PR #72 (architecture review, PR template, A4 test matrix) was opened by Sohail and is still open. The team needs to decide whether to merge, continue it, or close it. The architecture review document in it is a required A3 deliverable the repo still lacks.

## Proposed Owners for Unassigned Tasks
Proposal based on the roles in the [Team Charter](../team-charter.md), for the team to confirm or change. Victoria assigns.

### Adiya (Architecture & Development Lead)
| ID | Task |
|----|------|
| T-4 | Repo scaffolding, `.gitignore`, secrets handling |
| T-9 | Parse message into food and amount |
| T-10 | Default serving when no amount is given |
| T-11 | Query FDC and scale calories |
| T-12 | Save the entry |
| T-14 | Daily running total |
| T-17 | Chicago day cutoff |
| T-31 | `food_cache` table and refresh rule |

### Khumoyun (Operations & Evidence Co-Lead, backup on Architecture)
Already proposed for V-2 to V-4 on the host, so the host-adjacent build work fits.

| ID | Task |
|----|------|
| T-5 | Register bot, dev environment |
| T-6 | Hosting decision |
| T-30 | Duplicate `update_id` protection |
| T-32 | Webhook secret check (live half) |
| T-35 | Nightly backup script |

### Mazen (Operations & Evidence Lead)
| ID | Task |
|----|------|
| T-27 | Data-model review against NFR-4 |
| T-29 | Tester invite check and `/privacy` reply |
| T-33 | Per-tester deletion script |

### Victoria (Team Lead)
| ID | Task |
|----|------|
| T-7 | `/start` account creation |
| T-8 | Repeat `/start` safe |

### Bazid (Planning & Process Lead, acting Quality & Review Lead)
| ID | Task |
|----|------|
| T-15 | `/today` listing |
| T-19 | Per-user data separation |
| T-22 | Acceptance tests for every Must acceptance criterion |
| T-26 | Confirm no secrets in the repo before release |

### Still unowned after the team change
T-13, T-16, T-18, T-23 and T-24 need owners from the remaining four members. T-20 and T-21 are Should scope and stay unassigned until the Must work fits confirmed capacity.

## Dependency Notes
- T-1 through T-3 gate almost everything. Until OQ-2, OQ-3 and OQ-4 close, no implementation task can start and no estimate is firm.
- T-9 is the riskiest parsing task because the accepted input format (OQ-6) isn't decided.
- T-19 is a privacy requirement, not a feature. It has to be built into storage from the start, not added later.
- T-27 blocks the Entry Store merge. It is a review gate, not a build task.
- T-29 has no estimate yet. [Re-estimation Notes](re-estimation.md) needs one before the schedule is trusted.
- T-13 blocks T-11 acceptance and has no owner since the team change. It is on the critical path for FR-3.

## Change Log
| Date | Change | By |
|------|--------|----|
| 09/29/2026 | Created Cycle 1 task plan | Bazid |
| 10/15/2026 | Added architecture and verification tasks; updated T-13 per INV-01; proposed owners | Bazid |
| 10/30/2026 | Reconciled task IDs per task-id-map.md (#74): adopted Mazen's T-27 to T-29, renumbered the A3 additions to T-30 to T-35, merged two duplicate entries into T-29, noted T-32 partly complete in #69. Recorded the team change and marked Sohail's tasks for reassignment | Bazid |
