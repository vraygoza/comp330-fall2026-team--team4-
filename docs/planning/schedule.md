# Project Schedule and Milestones

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-11-09 |

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
| 8 | Assignment 4 submitted, tagged `a4-construction-integration` | 10/29/2026 | Done | Git tag, commit 0a1d54dc; CI success at that SHA |
| 9 | Integrated Cycle 1 path on `main` | 11/09/2026 | In progress | PR #90, approved, not merged |
| 10 | Assignment 5 submitted, tagged `a5-cycle1-release` | 11/10/2026 | In progress | Sakai submission, Git tag |
| 11 | Final project submitted | TODO: confirm with syllabus | Not started | |

## Cycle 1 Working Schedule

Work is tracked as GitHub Issues. Issue prefixes are by owner initial (A Adiya, B Bazid, K Khumoyun, M Mazen, S Sohail, V Victoria).

| Issue | Work | Owner | Status |
|-------|------|-------|--------|
| #47 | A1 design check | Adiya | Merged (#64) |
| #48 | Bot skeleton | Adiya | Merged (#69) |
| #49 | Food lookup | Adiya | Merged (#70) |
| #44 | B2 daily-total function | Bazid | Merged (#83) |
| #61 | K2 input parsing | Khumoyun | Merged (#88) |
| #50 | A4 integration | Adiya | PR #90 approved, not merged — the critical path |
| #51 | A5 architecture index and construction changes | Adiya | Merged (#71); A5 update in PR #92 |
| #56 | ADR acceptance vote (M1) | Team | Not started. A3 High finding and an A4 condition |
| #58 | Dependency review, risk register, CI evidence | Mazen | PR #91, approved |
| M2 | CI workflow and secrets check | Mazen | Merged (#73); successful run at the A4 tag |
| S2 | Contract tests for parser and daily total | Adiya | Merged (#77) |
| S1 | Architecture review, PR template, A4 test matrix | Sohail | Merged (#72); A5 release docs in PR #94 |
| K3 | Repo-wide consistency check, AI log split | Khumoyun | PR #89 |

## Team Change, 2026-10-30 (reversed 2026-11-09)

On 2026-10-30 the team recorded that Sohail had left and reassigned his tasks. The instructor has since confirmed he remains on the team, so that change is reversed. The team is six members and Sohail continues as Quality & Review Lead; T-13, T-22, T-23 and T-26 return to him, as does PR #72.

The entry is kept rather than deleted so the record shows what was decided and why it changed. See [Task Plan](task-plan.md) for current owners.

## Schedule Risks

- **#50 is the critical path and is approved but unmerged.** At the A4 tag a plain food message still returned NOT_READY. Nothing in Cycle 1 is demonstrated until PR #90 is on `main`, and `final-test-evidence.md` and the traceability summary both wait on it.
- ADR-0001 to ADR-0008 are still Proposed and the M1 vote (#56) has not happened. This was a High finding on A3 and a condition on A4; construction is running ahead of accepted decisions.
- Four open pull requests (#89, #90, #91, #94) touch `docs/ai/ai-use-log.md`, and #89 splits it into separate files. Merge order needs agreeing or rows will be lost in conflict resolution.
- Live checks V-1 to V-6 have not run, so hosting, live Telegram and FDC behavior remain assumptions. Food data is synthetic and the bot runs by local polling.
- The Assignment 2 internal review window was shorter than the agreed 48 hours. This is a process note from our own records; it does not establish lateness against Sakai.
- Estimates have no historical velocity behind them. See [Re-estimation Notes](re-estimation.md).

## Change Log

| Date | Change | By |
|------|--------|----|
| 09/29/2026 | Created Cycle 1 schedule | Bazid |
| 10/30/2026 | Updated through A3 and A4; fixed broken links to task-plan.md and meeting-notes.md; replaced the placeholder working schedule with current issues; recorded the team change; reworded the A2 internal-deadline row | Bazid |
| 11/02/2026 | Applied review feedback on #79: S2 owner is Adiya, M2 check passing, B2 status updated | Bazid |
| 11/09/2026 | Reversed the 10/30 team change; added the A4 and A5 milestones; updated working-schedule statuses against the open and closed PR lists; added the ai-use-log merge-order risk | Bazid |
