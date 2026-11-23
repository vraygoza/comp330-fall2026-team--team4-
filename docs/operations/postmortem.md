# Cycle 1 Postmortem

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-11-23 |
| Scope | Project start through the Cycle 1 release, tag `A5Cycle1Release` (commit `8eca1b5`, 2026-11-09) |
| Method | Repository evidence only: merged pull requests, commit history, tags, issue records and the risk register |

TODO: reconcile section headings with the Postmortem Template in Sakai Start Here before the Assignment 6 tag.

## Summary

Cycle 1 delivered a working, tested calorie-logging path and never deployed it. A tester's message is parsed, matched against a sample food list, saved under their Telegram ID, and answered with a Chicago-day total. Every step of that has unit and contract tests running in CI on each pull request. None of it has run anywhere except a developer's laptop.

The gap between "the code works" and "the release is usable" is the subject of this postmortem. In every case below, the technical work was not the hard part. The failures were in ownership, scheduling and record-keeping: tasks that appeared in two documents with two different owners, decisions that nothing blocked and so nobody closed, and evidence files that six people edited at once.

## What We Set Out to Build vs What Shipped

| Committed for Cycle 1 | Shipped at tag `A5Cycle1Release` |
|---|---|
| `/start` registration | Merged, tested (#69) |
| Log a food from a plain message | Merged, tested (#88, #90) |
| Calorie lookup | Merged, tested (#70), against eight synthetic foods |
| Daily total on the Chicago day | Merged, tested (#83), including both daylight-saving days |
| Two testers kept separate | Merged, tested (#90), AC-7.1 |
| `/today` command | Not built |
| Duplicate-update protection (T-30) | Not built. Still a `TODO` comment in `src/bot/web.py` on `main` |
| Gram amounts | Not built (CC-2) |
| Live USDA FoodData Central lookup | Not built |
| Deployed webhook on a host | Not deployed |
| Outside testers | None, because nothing was deployed |

## Timeline

| Date | Event |
|------|-------|
| 2026-10-14 | Architecture package and INV-01 spike land |
| 2026-10-15 | ADR-0001 to ADR-0008 opened as Proposed. Task IDs T-27 to T-29 assigned twice, in two documents, on the same day |
| 2026-10-29 | `task-id-map.md` merged (#74), resolving the ID collision. T-30 recorded as "TODO: assign" |
| 2026-10-29 | CI with automated tests and a secrets check merged (#73) |
| 2026-10-30 | A team member is removed from the team for capacity reasons |
| 2026-11-02 | AI-use rows for five merged pull requests found missing, lost in merge conflicts |
| 2026-11-03 | Integration merged (#90). 88 tests pass. Mazen runs the full path once on his own machine against his own test bot (commit `14e247b`) |
| ~2026-11-07 | The removed member is reinstated by the instructor |
| 2026-11-09 | ADR-0001 to ADR-0009 accepted, 6 of 6, on issue #56 — 25 days after they were proposed |
| 2026-11-09 | Tag `A5Cycle1Release` cut at commit `8eca1b5` |
| 2026-11-09 to 2026-11-23 | No commit reaches `main` |
| 2026-11-23 | PR #104 opens with the T-30 implementation, 39 days after T-30 was first written down |

## What Went Well

These are worth naming because they are the practices that should carry into sustainment, not politeness.

- **CI from #73 onward made review real.** Every pull request runs the test suite and a regex secrets scan. It caught a broken merge before it reached `main`.
- **The secrets discipline held.** On 2026-11-09 the full history of every branch — 180 commits — was scanned with the same patterns used in CI. No tokens and no secret files were found. No bot token has ever been pasted into an AI tool, per the AI policy.
- **The architecture boundary held under integration.** `src/core/` still imports no Telegram, Flask, HTTP or SQL. The one place that reads secrets is `adapters/telegram.py`; the one place that runs SQL is `adapters/store.py`. This was checked with `git grep` against the integration branch, not asserted.
- **The hardest correctness problem was solved properly.** The Chicago-day boundary is handled with `zoneinfo`, not a fixed UTC offset, and is tested on the 23-hour and 25-hour days. A fixed offset was explicitly rejected.
- **The team recorded conflicts instead of hiding them.** The task ID collision produced a published map rather than a quiet renumber. The risk register marks risks "Occurred" rather than editing them down.

## Findings and Root Causes

### F-1 — The release was tagged, but the product was never deployed

**What happened.** Tag `A5Cycle1Release` was cut on 2026-11-09. The bot has run end to end exactly once, on one developer's laptop, against that developer's own test bot.

**Evidence.** Risk 14, status "Occurred for Cycle 1." Verification tasks V-2 to V-4 have never run. Architecture Section 11, CC-1.

**Root cause.** ADR-0006 adopted a host *conditional on* verification checks V-2 to V-4 passing. The decision was accepted without those checks being scheduled or assigned, so the condition had no owner. A conditional decision with an unowned condition is an unmade decision that looks made.

**What we would do differently.** A decision that depends on a verification does not get accepted until the verification has an owner and a date in the same pull request that accepts it.

### F-2 — Duplicate-update protection went 39 days without an owner

**What happened.** T-30 was written down on 2026-10-15. It is still an unimplemented `TODO` comment in `src/bot/web.py` on `main` today. The implementation only opened as PR #104 on 2026-11-23.

**Evidence.** `src/bot/web.py` line 49. `task-id-map.md` lists T-30 as "TODO: assign." Risk 17 and Risk 23 both record it unowned.

**Root cause.** Two documents recorded two different answers to "who owns this." Architecture Section 11 named Khumoyun; the task plan left the owner blank. When one source names an owner and another does not, every reader resolves the contradiction in whichever direction means the work is not theirs.

**Contributing factor.** T-30 was the gate on deployment, and deployment was not scheduled, so nothing downstream ever pulled on it. Work that blocks nothing scheduled gets done last regardless of how important it is.

**What we would do differently.** The task plan is the only file permitted to name a task owner. Every other document links to it rather than restating it.

### F-3 — Two documents assigned the same task IDs on the same day

**What happened.** On 2026-10-15, `traceability.md` and `task-plan.md` each assigned T-27, T-28 and T-29 to different pieces of work.

**Evidence.** `docs/planning/task-id-map.md`, section "What Went Wrong."

**Root cause.** No single source of truth for identifiers. Two leads each took "the next number" from the document in front of them.

**What we changed.** `task-id-map.md` is now the governing list and the place a new ID is taken from.

**Still outstanding.** `docs/planning/` contains both `re-estimation.md` and `reestimation.md`. The same class of defect — two files, one subject — has not been cleaned up.

### F-4 — Eight architecture decisions sat in Proposed for 25 days

**What happened.** ADR-0001 to ADR-0008 were opened Proposed on 2026-10-15 and accepted 6 of 6 on 2026-11-09, on issue #56. The team built on them throughout that window.

**Evidence.** Issue #56 vote tally. Risk 12, now Closed. The delay was raised in the Assignment 3 feedback and remained open for another two weeks after that.

**Root cause.** The vote had no owner and no date. Because the ADRs did not block any code — the code was written against them regardless — closing them never competed with anything that had a deadline.

**What we would do differently.** Every proposal gets an owner and a decision date the day it is opened. Any proposal past its date goes to the top of the next meeting agenda before any other item.

### F-5 — Shared evidence files lost content in merge conflicts

**What happened.** The AI-use rows for five merged pull requests (#73, #77, #83, #84, #88) disappeared from `docs/ai/ai-use-log.md`. They were restored by #89. The fix — splitting the log into one file per member — was built and then removed again by the #97 revert chain, so `main` today has both the shared log and the per-member files in an inconsistent state.

**Evidence.** Risk 2 and Risk 10, both "Occurred." PR #101 deletes `docs/ai/ai-log-*.md`.

**Root cause.** One append-only file edited by six people on branches that lived for days. Conflicts were resolved by keeping one side, which silently discards the other side's rows — a resolution that looks clean in the diff and loses data.

**What we would do differently.** Per-member files, which was the right fix. It needs to be re-landed and not reverted again.

### F-6 — The release was tagged while its own release documents were unmerged

**What happened.** The Assignment 5 release package listed nine deliverables. At the tagged commit, `docs/release/` contains three files. `release-notes.md`, `known-limitations.md`, `defect-summary.md` and `cycle2-handoff.md` are not on `main`. `known-limitations.md` was merged and then reverted.

**Evidence.** `git ls-tree` at tag `A5Cycle1Release`.

**Root cause.** The tag was cut against a calendar date rather than against a checklist of merged artifacts. The release package had a status column, but nothing enforced it before tagging.

**What we would do differently.** The tag is not cut until every row of the release package table reads Merged, confirmed by looking at `main` rather than at a pull request.

### F-7 — Two weeks of Cycle 2 produced no merged change

**What happened.** `main` has not moved since 2026-11-09. The instruction on that date was explicitly to run Cycle 2 planning in parallel with finishing Assignment 5, and not to serialize them.

**Evidence.** `git rev-parse HEAD` equals the `A5Cycle1Release` tag.

**Root cause.** Cycle 2 scope was discussed but never written into the repository, so it had no issues, no owners and no dates. Work that exists only in a conversation does not get done.

**What we would do differently.** Cycle 2 scope goes into the task plan as numbered, owned, dated tasks before Cycle 1 is tagged, not after.

### F-8 — The risk register contains duplicated rows with conflicting statuses

**What happened.** Risks 10 through 23 each appear twice in `docs/planning/risk-register.md`, with different statuses, and the header table has two "Last updated" rows.

**Evidence.** `docs/planning/risk-register.md` on `main`.

**Root cause.** A merge conflict resolved by keeping both sides instead of reconciling them — the mirror image of F-5, where keeping one side lost data. Neither resolution was reviewed against the rendered file.

**What we would do differently.** Any pull request touching a table-heavy evidence file gets its rendered preview checked, not just its diff.

## Cross-Cutting Pattern

Six of the eight findings are the same failure in different clothes: **work with no single owner and no date does not happen, however important it is, and however clearly it is written down.** T-30 was written down five weeks before anyone built it. The ADR vote was written down and flagged by the instructor and still took 25 days. The deployment condition was written into an accepted decision and never scheduled.

Documentation was not the weak point. This team documented more than it executed. The weak point was that documents recorded intentions without recording who and when, and nothing in the workflow refused to proceed when those fields were blank.

## Residual Risks Carried Into Cycle 2

| Risk | Status entering Cycle 2 | Owner |
|------|------------------------|-------|
| Not deployed; V-1 to V-6 never run | Open | TODO: assign |
| T-30 duplicate protection | Implementation open in PR #104, unmerged, unreviewed | Adiya (author); reviewer TODO |
| `/today` not built | Open | TODO: assign |
| Food data synthetic; gram amounts unsupported | Open | Adiya |
| Tester invite check and `/privacy` (T-29, FR-10) | Not started | TODO: assign |
| Per-tester deletion script (T-33) | Not started | TODO: assign |
| AI-use log split reverted | Inconsistent on `main` | Khumoyun |
| Duplicate files: `re-estimation.md` / `reestimation.md` | Open | Bazid |
| Risk register duplicate rows | Open | Mazen |

## Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| A-1 | Review and merge PR #104 (T-30) with a non-author reviewer | Bazid (review) | 2026-11-24 |
| A-2 | Re-land the per-member AI log split and do not revert it | Khumoyun | 2026-11-24 |
| A-3 | De-duplicate the risk register rows and the header table | Mazen | 2026-11-24 |
| A-4 | Delete `reestimation.md`, keep `re-estimation.md` | Bazid | 2026-11-24 |
| A-5 | Write the missing release documents onto `main` before tagging | Victoria | 2026-11-24 |
| A-6 | Task plan becomes the only file naming task owners; other docs link to it | Bazid | 2026-11-24 |

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-11-23 | Created for Assignment 6 from repository evidence at commit `8eca1b5` | Bazid |#
