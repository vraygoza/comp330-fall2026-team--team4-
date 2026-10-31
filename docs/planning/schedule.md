# Project Schedule and Milestones

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-10-30 |

Schedule for Cycle 1 of the Telegram calorie-counter bot. The Cycle 1 vertical slice is: a tester sends the bot one food item, the bot finds the calories, saves the entry, and replies with the daily total. See [Scope Statement](scope.md).

Task IDs referenced here are governed by [Task ID Map](task-id-map.md).

## Team Cadence

| What | When |
|------|------|
| Formal team meeting | Wednesdays, 7:00 PM (before each assignment or checkpoint) |
| Internal deadline | 48 hours before every Sakai due date |
| Async check-in | WhatsApp, blockers posted as 🚨 BLOCKER |
| PR review | Reviewer chosen by the author based on the area changed (agreed 10/14) |

## Milestones

| # | Milestone | Date | Status | Evidence |
|---|-----------|------|--------|----------|
| 1 | Kickoff call, lead roles assigned | 09/08/2026 | Done | [Meeting Notes](../meeting-notes.md) |
| 2 | Team charter written | 09/16/2026 | Done | [Team Charter](../team-charter.md) |
| 3 | Assignment 1 submitted, tagged `a1-project-launch` | 09/20/2026 | Done | Sakai submission, Git tag |
| 4 | Project concept chosen (calorie bot) | 09/16/2026 | Done | [Decision Log](../decisions/decision-log.md) (D1, still Proposed) |
| 5 | Assignment 2 submitted, tagged `a2-planning-estimate` | 09/29/2026 | Done | Git tag, commit 4cf90ab |
| 6 | Assignment 3 submitted, tagged `a3-architecture-review` | 10/15/2026 | Done | Git tag, commit 42350c6 |
| 7 | Task IDs reconciled across planning records | 10/30/2026 | Done | [Task ID Map](task-id-map.md), PRs #74, #75, #76 |
| 8 | Assignment 4 construction package | 10/29/2026 | In progress | `/src/`, `/tests/`, PRs #65 to #77 |
| 9 | Cycle 1 implementation complete | TODO: confirm with syllabus | Not started | |
| 10 | Final project submitted | TODO: confirm with syllabus | Not started | |

## Cycle 1 Working Schedule

Work is tracked as GitHub Issues. Issue prefixes are by owner initial (A Adiya, B Bazid, K Khumoyun, M Mazen, V Victoria).

| Issue | Work | Owner | Status |
|-------|------|-------|--------|
| #47 | A1 design check | Adiya | Merged (#64) |
| #48 | Bot skeleton | Adiya | Merged (#69) |
| #49 | Food lookup | Adiya | Merged (#70) |
| #51 | A5 architecture index and construction changes | Adiya | PR #71 open, blocked on #50 |
| #44 | B2 daily-total function | Bazid | Not started — blocks #50 |
| #61 | K2 input parsing | Khumoyun | Not started — blocks #50 |
| #50 | A4 integration | Adiya | Blocked on #44 and #61 |
| #56 | ADR acceptance vote | Team | Open |
| #58 | Risk register update | Mazen | Open |
| M2 | CI workflow and secrets check | Mazen | PR #73 open, check failing |
| S2 | Contract tests for parser and daily total | Unowned | PR #77 open |

## Team Change, 2026-10-30

Sohail is no longer on the team; the instructor was notified the same day. The team is now five part-time members.

Consequences for this schedule:
- Quality & Review Lead is vacant. Bazid is the charter backup and is acting in the role for Cycle 1.
- T-13, T-22, T-23 and T-26 need new owners. See [Task Plan](task-plan.md).
- PR #72 (architecture review, PR template, A4 test matrix) and PR #77 (contract tests) were his. Both are open and need a decision to adopt, continue or close.
- Capacity assumptions in [Team Commitments](team-commitments.md) and [Re-estimation Notes](re-estimation.md) are now out of date and must be recalculated for five people.

## Schedule Risks

- **#50 is blocked on two unstarted issues.** The integration PR cannot proceed until B2 (#44) and K2 (#61) land. These are the critical path for the vertical slice.
- **Capacity dropped from six members to five** mid-cycle, while the forecast already exceeded confirmed hours.
- ADR-0001 to ADR-0008 are still Proposed. Construction is running ahead of accepted decisions (#56).
- Live checks V-1 to V-6 have not run, so hosting and FDC behavior remain assumptions.
- The Assignment 2 internal review window was shorter than the agreed 48 hours. This is a process note from our own records; it does not establish lateness against Sakai.
- Estimates have no historical velocity behind them. See [Re-estimation Notes](re-estimation.md).

## Change Log

| Date | Change | By |
|------|--------|----|
| 09/29/2026 | Created Cycle 1 schedule | Bazid |
| 10/30/2026 | Updated through A3 and A4; fixed broken links to task-plan.md and meeting-notes.md; replaced the placeholder working schedule with current issues; recorded the team change; reworded the A2 internal-deadline row | Bazid |
