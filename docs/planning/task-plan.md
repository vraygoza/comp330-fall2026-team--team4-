# Task Plan

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-10-15 |

Cycle 1 work broken into tasks. Each task traces to a requirement in [Requirements](../requirements/requirements.md). Estimates are in [Effort Estimates](estimates.md). Owners marked TODO are assigned by Victoria.

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
| T-13 | Build and verify the curated food map (reviewed word to FDC record and portion) | FR-3 (AC-3.2), P-2 | T-11, V-1 | Sohail | Not started |
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
| T-22 | Write acceptance tests for every Must acceptance criterion | All Must FRs | T-7 through T-19 | Sohail | Not started |
| T-23 | Time responses to confirm the 5-second target | NFR-1 | T-14 | Sohail | Not started |
| T-24 | Test with 15 testers active in one week | NFR-2 | T-19, OQ-9 | TODO: assign | Not started |
| T-25 | Write tester onboarding and data-handling notice | Tester onboarding | OQ-8 | Mazen | Not started |
| T-26 | Confirm no secrets in the repo before release | NFR-3 | T-4 | Sohail | Not started |

## Architecture Tasks (added 10/15/2026)
Added after INV-01 and the architecture package. Sources in [Re-estimation Notes](re-estimation.md).

| ID | Task | Traces to | Depends on | Owner | Status |
|----|------|-----------|------------|-------|--------|
| T-27 | Record processed `update_id` values in the same transaction as the entry | C-1, Finding 7 | T-3, T-12 | TODO: assign | Not started |
| T-28 | Build `food_cache` table, loader, and 30-day refresh rule | C-5, Finding 8 | T-1, T-3 | TODO: assign | Not started |
| T-29 | Check `X-Telegram-Bot-Api-Secret-Token`; return 403 and log AUTH_REJECTED | C-1, TB-1 | T-5 | TODO: assign | Not started |
| T-30 | Write `/privacy` command and the collection notice text | OQ-8, G-4 | Mazen's OQ-8 answer | Mazen | Not started |
| T-31 | Write and test the per-tester deletion script | OQ-8, C-6, G-5 | T-3 | TODO: assign | Not started |
| T-32 | Deploy smoke test: `/start`, `2 eggs`, `/today` on a dev account | G-3 | T-6, T-14 | Adiya | Not started |
| T-33 | Nightly `sqlite3 .backup` of `bot.db` on the host | Section 8 recovery | T-6 | TODO: assign | Not started |
| T-34 | Tester invite code check in the Register use case | FR-10 (proposed) | T-7, OQ-1 | TODO: assign | Not started |

## Verification Tasks (INV-01)
These close the blocking decisions. Owners proposed in INV-01 and confirmed at the architecture review.

| ID | Task | Closes | Owner | Status |
|----|------|--------|-------|--------|
| V-1 | Live FDC run of the 20 T-13 foods | P-2, P-3 | Adiya with Sohail | Not started |
| V-2 | Reach `api.telegram.org` and `api.nal.usda.gov` from PythonAnywhere | P-6, P-7 | Khumoyun (proposed) | Not started |
| V-3 | Register test bot, set webhook with secret, send `/start` | P-7 | Khumoyun (proposed) | Not started |
| V-4 | Write an entry, reload the web app, read it back | P-7 | Khumoyun (proposed) | Not started |
| V-5 | Read `X-RateLimit-Remaining` from the host | Finding 8 | Adiya | Not started |
| V-6 | Time 20 FDC searches from the host | NFR-1, P-9 | Adiya | Not started |

**V-2 is the highest-priority item in Cycle 1.** If PythonAnywhere blocks `api.telegram.org`, P-6 and P-7 both change and estimates for T-2, T-6, and every hosting-dependent task are revised again.

## Proposed Owners for Unassigned Tasks
24 of 34 tasks have no owner. Below is a proposal based on the roles in the [Team Charter](../team-charter.md), for the team to confirm or change at the next meeting. These are not assignments. Victoria assigns.

### Adiya (Architecture & Development Lead)
Maintains repo structure, guides technical decisions, sets development standards. These are the core components she specified in the architecture package.

| ID | Task |
|----|------|
| T-4 | Repo scaffolding, `.gitignore`, secrets handling |
| T-9 | Parse message into food and amount |
| T-10 | Default serving when no amount is given |
| T-11 | Query FDC and scale calories |
| T-12 | Save the entry |
| T-14 | Daily running total |
| T-17 | Chicago day cutoff |
| T-28 | `food_cache` table and refresh rule |

### Khumoyun (Operations & Evidence Co-Lead, backup on Architecture)
Already proposed for V-2 to V-4 on the host, so the host-adjacent build work fits. This also keeps Adiya from being a single point of failure on early decisions, which the A2 review flagged.

| ID | Task |
|----|------|
| T-5 | Register bot, dev environment |
| T-6 | Hosting decision |
| T-27 | Duplicate `update_id` protection |
| T-29 | Webhook secret check |
| T-33 | Nightly backup script |

### Mazen (Operations & Evidence Lead)
Owns OQ-8 and the G-5 deletion checkpoint, so the script that carries it out belongs with him.

| ID | Task |
|----|------|
| T-31 | Per-tester deletion script |

### Sohail (Quality & Review Lead)
Verifies work meets requirements and runs testing. T-16 and T-18 are both refusal paths, which are the error cases a quality lead should own.

| ID | Task |
|----|------|
| T-16 | Empty `/today` message |
| T-18 | Unknown food handling |
| T-24 | 15-tester capacity check |

### Victoria (Team Lead)
Registration is small, self-contained, and blocks no one else. She owns the G-4 tester onboarding checkpoint, and the invite code is the gate for it.

| ID | Task |
|----|------|
| T-7 | `/start` account creation |
| T-8 | Repeat `/start` safe |
| T-34 | Tester invite code check |

### Bazid (Planning & Process Lead)
T-19 is the privacy requirement that has to be built into storage from the start rather than added later, so it needs an owner who will hold that line.

| ID | Task |
|----|------|
| T-15 | `/today` listing |
| T-19 | Per-user data separation |

### Not proposed yet
T-20 and T-21 are Should scope. They stay unassigned until the Must work fits confirmed capacity. [Re-estimation Notes](re-estimation.md) recommends cutting these first if it does not.

### Why this matters
The charter gives the Team Lead and the Planning & Process Lead no implementation tasks. That is why both roles currently show documentation work only. Taking real tasks is how both of us build verifiable contribution for the rest of the cycle.

## Dependency Notes
- T-1 through T-3 gate almost everything. Until OQ-2, OQ-3, and OQ-4 close, no implementation task can start and no estimate is firm.
- T-9 is the riskiest parsing task because the accepted input format (OQ-6) isn't decided.
- T-19 is a privacy requirement, not a feature. It has to be built into storage from the start, not added later.

## Change Log
| Date | Change | By |
|------|--------|----|
| 09/29/2026 | Created Cycle 1 task plan | Bazid |
| 10/15/2026 | Added architecture and verification tasks; updated T-13 per INV-01; proposed owners for unassigned work | Bazid |
