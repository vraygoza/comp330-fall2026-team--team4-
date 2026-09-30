# Effort Estimates

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-09-29 |

Estimates for the tasks in [Task Plan](task-plan.md). Numbers are hours of focused work by one person.

## How These Were Made
- This is the team's first implementation cycle, so there is no past velocity to base estimates on. Everything here is judgment, not measurement.
- Each task has a low, likely, and high estimate. The spread shows how confident we are, and wide spreads mark the tasks most likely to need re-estimation.
- Estimates cover writing the code, testing it, and getting it reviewed. They do not include writing documentation or time spent in meetings.
- Confidence is Low, Medium, or High. Low means the task depends on a decision we haven't made yet.

## Setup
| ID | Task | Low | Likely | High | Confidence |
|----|------|-----|--------|------|------------|
| T-1 | Choose data source | 2 | 4 | 8 | Medium |
| T-2 | Choose language and library | 1 | 2 | 4 | High |
| T-3 | Storage and data model | 3 | 5 | 10 | Low |
| T-4 | Repo scaffolding and secrets | 2 | 3 | 5 | Medium |
| T-5 | Register bot, dev environment | 1 | 2 | 4 | High |
| T-6 | Hosting for the bot | 2 | 5 | 12 | Low |
| | **Subtotal** | **11** | **21** | **43** | |

## Must Requirements
| ID | Task | Low | Likely | High | Confidence |
|----|------|-----|--------|------|------------|
| T-7 | `/start` and account creation | 2 | 3 | 5 | Medium |
| T-8 | Repeat `/start` safe | 1 | 2 | 3 | Medium |
| T-9 | Parse food and amount | 4 | 8 | 16 | Low |
| T-10 | Default serving size | 2 | 3 | 6 | Low |
| T-11 | Query data source, scale calories | 3 | 6 | 12 | Low |
| T-12 | Save the entry | 2 | 3 | 6 | Medium |
| T-13 | Hand-check 20 foods | 2 | 3 | 5 | High |
| T-14 | Daily running total | 2 | 3 | 5 | Medium |
| T-15 | `/today` listing | 2 | 3 | 5 | Medium |
| T-16 | Empty `/today` message | 1 | 1 | 2 | High |
| T-17 | Midnight Central cutoff | 2 | 4 | 8 | Low |
| T-18 | Unknown food handling | 2 | 3 | 6 | Medium |
| T-19 | Per-user data separation | 2 | 4 | 8 | Medium |
| | **Subtotal** | **27** | **46** | **87** | |

## Should Requirements
| ID | Task | Low | Likely | High | Confidence |
|----|------|-----|--------|------|------------|
| T-20 | `/undo` | 2 | 3 | 5 | Medium |
| T-21 | Manual calorie entry | 2 | 4 | 7 | Medium |
| | **Subtotal** | **4** | **7** | **12** | |

## Testing and Release
| ID | Task | Low | Likely | High | Confidence |
|----|------|-----|--------|------|------------|
| T-22 | Acceptance tests | 4 | 8 | 14 | Medium |
| T-23 | Response time check | 1 | 2 | 4 | Medium |
| T-24 | 15-tester load test | 2 | 4 | 8 | Low |
| T-25 | Tester onboarding notice | 2 | 3 | 5 | Medium |
| T-26 | Secrets check before release | 1 | 1 | 2 | High |
| | **Subtotal** | **10** | **18** | **33** | |

## Totals
| Scope | Low | Likely | High |
|-------|-----|--------|------|
| Must only (setup + Must + testing) | 48 | 85 | 163 |
| Must + Should | 52 | 92 | 175 |

## Capacity Check
Cycle 1 runs from now to an estimated 10/18/2026, about three weeks. With six members, the likely Must-only estimate of 85 hours works out to roughly **5 hours per person per week**.

That is close to the limit of what this team can sustain, and [Team Commitments](team-commitments.md) still has unconfirmed capacity for five of six members. If the high estimate of 163 hours turns out to be right, it is about 9 hours per person per week, which is not realistic alongside other courses and jobs.

**Recommendation:** commit only to the Must requirements for Cycle 1. Treat FR-8 and FR-9 as stretch goals and drop them without discussion if the schedule slips.

## Assumptions
- Cycle 1 is three weeks, ending 10/18/2026. This is an estimate, not a confirmed course date.
- All six members contribute implementation or testing hours, not just documentation.
- The chosen data source has a usable free API. If it needs scraping or a paid tier, T-1 and T-11 grow a lot.
- Nobody on the team has built a Telegram bot before, so the first tasks include learning time.

## What Would Trigger Re-estimation
- OQ-2, OQ-3, or OQ-4 closing with an answer that changes the approach.
- Any task taking more than its high estimate.
- The real Cycle 1 end date differing from 10/18/2026.
- A member's confirmed capacity coming in below what is assumed here.

Re-estimation is tracked by Sophail in [reestimation.md](reestimation.md).

## Change Log
| Date | Change | By |
|------|--------|----|
| 09/29/2026 | Created Cycle 1 estimates | Bazid |
