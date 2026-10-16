# Re-estimation Notes

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-10-15 |
| Baseline revised | A2 checkpoint 4cf90ab (estimates.md) |
| Trigger | INV-01 lookup and storage investigation; A2 feedback |

Revised estimates after the architecture work. The A2 estimates listed re-estimation triggers; INV-01 hit three of them — a blocking decision closed, the approach changed, and new work appeared. Original A2 numbers are kept beside the revised ones.

## What Changed and Why

| Area | Change | Source |
|------|--------|--------|
| Setup (T-1 to T-3) | Most analysis complete; remaining work is verification V-1 to V-6 | INV-01 |
| T-9, T-10 parsing | Rules fixed and tested in the spike; confidence Low to Medium | INV-01 Findings 1-2 |
| T-11 lookup | Grew: curated map loader, 25% ambiguity rule, Atwater energy fallback | P-2, P-3, Finding 3 |
| T-13 food check | Changed from a hand-check report to building and verifying running configuration | Finding 4 |
| T-17 day boundary | Proven in the spike including both daylight-saving days | P-8 |
| New work | Seven tasks that did not exist at A2 | INV-01, api-contracts.md |

## Revised Estimates (person-hours)

### Setup
| ID | Task | A2 likely | Revised likely | Note |
|----|------|-----------|----------------|------|
| T-1 | Data source | 4 | 3 | Decision proposed (P-2); V-1 and V-5 remain |
| T-2 | Language and library | 2 | 1 | P-6 proposed; conditional on V-2 |
| T-3 | Storage and data model | 5 | 2 | Schema specified in C-6 |
| T-4 | Repo scaffolding and secrets | 3 | 3 | Secrets now named |
| T-5 | Register bot, dev environment | 2 | 2 | Unchanged |
| T-6 | Hosting | 5 | 4 | Narrowed to V-2 to V-4, with Option B fallback |
| | **Subtotal** | **21** | **15** | |

### Must Requirements
| ID | Task | A2 likely | Revised likely | Note |
|----|------|-----------|----------------|------|
| T-7 | `/start` | 3 | 3 | |
| T-8 | Repeat `/start` | 2 | 1 | Spike-proven |
| T-9 | Parse food and amount | 8 | 5 | P-5 forms fixed and tested |
| T-10 | Default serving | 3 | 2 | Folded into P-4 |
| T-11 | Lookup and scale | 6 | 10 | **Grew** — map, ambiguity rule, energy fallback |
| T-12 | Save entry | 3 | 3 | |
| T-13 | Curated food map | 3 | 7 | **Grew** — now produces configuration |
| T-14 | Daily total | 3 | 3 | |
| T-15 | `/today` | 3 | 3 | |
| T-16 | Empty `/today` | 1 | 1 | |
| T-17 | Chicago day cutoff | 4 | 2 | Spike-proven |
| T-18 | Unknown foods | 3 | 3 | Outcome codes defined (C-8) |
| T-19 | Per-user separation | 4 | 3 | Entry Store port enforces it |
| | **Subtotal** | **46** | **46** | Same total, different distribution |

### New Tasks (did not exist at A2)
| ID | Task | Low | Likely | High | Source |
|----|------|-----|--------|------|--------|
| T-27 | Duplicate protection via `processed_updates` | 2 | 3 | 5 | Finding 7, C-1 |
| T-28 | `food_cache` table and refresh rule | 2 | 4 | 7 | C-5, Finding 8 |
| T-29 | Webhook secret check and 403 path | 1 | 2 | 4 | C-1, TB-1 |
| T-30 | `/privacy` command and notice text | 2 | 3 | 5 | OQ-8, G-4 |
| T-31 | Deletion script for G-5 | 2 | 3 | 5 | OQ-8, C-6 |
| T-32 | Deploy smoke test | 1 | 2 | 4 | G-3 |
| T-33 | Nightly backup of `bot.db` | 1 | 2 | 4 | Diagram, SQLite risk |
| | **Subtotal** | **11** | **19** | **34** | |

### Testing and Release
| ID | Task | A2 likely | Revised likely | Note |
|----|------|-----------|----------------|------|
| T-22 | Acceptance tests | 8 | 6 | Contract checks listed; several already run in the spike |
| T-23 | Response time check | 2 | 2 | P-9 defines the conditions |
| T-24 | Capacity check | 4 | 3 | P-10 separates 15 synthetic from 3 real testers |
| T-25 | Tester recruitment | 3 | 2 | Notice text moved to T-30 |
| T-26 | Secrets check | 1 | 1 | |
| | **Subtotal** | **18** | **14** | |

## Totals

| Scope | A2 (L/Li/H) | Revised (L/Li/H) |
|-------|-------------|------------------|
| Implementation tasks, Must only | 48 / 85 / 163 | 55 / 94 / 167 |
| Must + Should | 52 / 92 / 175 | 59 / 101 / 179 |

### Overhead (not counted at A2)
The A2 feedback asked for documentation, meetings and integration to be included, without double-counting the review and testing already inside task estimates.

| Item | Likely hours | Basis |
|------|--------------|-------|
| Documentation (A4, A5 evidence, ADR updates) | 12 | Observed A2 and A3 effort |
| Meetings | 9 | 6 members × 0.5h × 3 weeks |
| Integration allowance | 8 | First end-to-end wiring; not in any task estimate |
| **Overhead subtotal** | **29** | |

### Full Cycle 1 forecast
| Scope | Likely person-hours |
|-------|---------------------|
| Must implementation | 94 |
| Overhead | 29 |
| **Total, Must only** | **123** |
| Should items (T-20, T-21) | +7 |

## Capacity Comparison

| Measure | Hours |
|---------|-------|
| Confirmed weekly capacity (2 of 6 members) | 11 |
| Confirmed over a 3-week window | 33 |
| Forecast, Must only including overhead | 123 |
| **Gap against confirmed capacity** | **90 hours** |

Four members have not confirmed availability, so 33 hours is a partial basis, not the team total. It is not evidence that anyone is inactive. If the four unconfirmed members average 5 hours per week, total capacity would be about 93 hours over three weeks, still short of the 123-hour likely forecast.

The three-week window itself is an estimate. October 18 is a planning estimate, not a confirmed course date.

## Response Options
Presented for the team to decide at the architecture review. No option is adopted here.

1. **Drop Should scope.** Removes 7 hours. Not sufficient on its own.
2. **Extend the window.** If Cycle 1 runs four weeks instead of three, confirmed-plus-estimated capacity gets closer to the likely case.
3. **Reduce Must scope.** FR-5 (`/today`) and FR-6 messaging are the least load-bearing parts of the vertical slice. Removing them would weaken the demonstration and should be a last resort.
4. **Confirm real capacity first.** Four members confirming hours may close part of the gap on paper. This is the cheapest step and should happen before any scope is cut.

**Recommendation:** Option 4 first, then Option 1, then reassess. Do not label Cycle 1 on track until the gap is closed with real numbers.

## Open Dependencies
Estimates for T-2, T-6 and the hosting-dependent tasks hold only if V-2 through V-4 pass. If PythonAnywhere does not allow `api.telegram.org`, P-6 and P-7 both change and these estimates are revised again.

## Change Log
| Date | Change | By |
|------|--------|----|
| 10/15/2026 | Created; revised A2 estimates against INV-01 findings | Bazid |
