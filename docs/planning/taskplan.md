# Task Plan

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-09-29 |

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
| T-13 | Hand-check 20 common foods against the data source | FR-3 (AC-3.2) | T-11 | Sohail | Not started |
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

## Dependency Notes
- T-1 through T-3 gate almost everything. Until OQ-2, OQ-3, and OQ-4 close, no implementation task can start and no estimate is firm.
- T-9 is the riskiest parsing task because the accepted input format (OQ-6) isn't decided.
- T-19 is a privacy requirement, not a feature. It has to be built into storage from the start, not added later.

## Change Log
| Date | Change | By |
|------|--------|----|
| 09/29/2026 | Created Cycle 1 task plan | Bazid |
