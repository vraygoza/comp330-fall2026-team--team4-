# Cycle 1 Postmortem

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-11-23 |
| Scope | Project start through the Cycle 1 release, tag `A5Cycle1Release` (commit `8eca1b5`, 2026-11-09) |
| Method | Repository evidence only. Every date below was read from `git log` on `origin/main`, not from recollection |

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
| Duplicate-update protection (T-30) | Not built in Cycle 1. Implementation opened as #104 on 2026-11-23 |
| Gram amounts | Not built (CC-2) |
| Live USDA FoodData Central lookup | Not built |
| Deployed webhook on a host | Not deployed |
| Outside testers | None, because nothing was deployed |

## Timeline

Dates are merge dates on `origin/main`, confirmed with `git log`.

| Date | Event |
|------|-------|
| 2026-10-14 | Architecture package and INV-01 spike land |
| 2026-10-15 | ADR-0001 to ADR-0008 opened as Proposed. Task IDs T-27 to T-29 assigned twice, in two documents, on the same day |
| 2026-10-29 | Bot skeleton (#69) and food lookup (#70) merge |
| 2026-10-30 | `task-id-map.md` merges (#74), resolving the ID collision. T-30 recorded as "TODO: assign" |
| 2026-10-30 | The team records a member as off the team |
| 2026-11-02 | CI with automated tests and a secrets check merges (#73). Contract tests (#77) and the Day Calculator (#83) merge |
| 2026-11-03 | Parser merges (#88). Mazen runs the full path once on his own machine against his own test bot, at commit `14e247b` |
| Before 2026-11-09 | The instructor confirms the member remained on the course roster; the team reverses the 10/30 change |
| 2026-11-09 | #89 merges, restoring AI-use rows lost in earlier merge conflicts and adding one AI log per member |
| 2026-11-09 | Integration merges (#90). 88 tests pass |
| 2026-11-09 | `known-limitations.md` merges (#97) and is reverted the same day (`265a906`) |
| 2026-11-09 | ADR-0001 to ADR-0009 accepted, 6 of 6, on issue #56 — 25 days after they were proposed |
| 2026-11-09 | Tag `A5Cycle1Release` cut at commit `8eca1b5` |
| 2026-11-09 to 2026-11-23 | No pull request merges to `main` |
| 2026-11-23 | `b789a22` is committed directly to `main` with no pull request and no review (see F-7) |
| 2026-11-23 | #104 opens with the T-30 implementation, 39 days after T-30 was first written down |

## What Went Well

These are worth naming because they are the practices that should carry into sustainment, not politeness.

- **CI from #73 onward made review real.** Every pull request runs the test suite and a regex secrets scan.
- **The secrets discipline held.** The risk register (Risk 6, owner Mazen) records that on 2026-11-09 the full history of every branch — a figure of 180 commits, recorded by Mazen, not independently recounted for this postmortem — was scanned with the CI patterns, finding no tokens and no secret files. No bot token has ever been pasted into an AI tool, per the AI policy.
- **The architecture boundary held under integration.** `src/core/` imports no Telegram, Flask, HTTP or SQL. Secrets are read only in `adapters/telegram.py`; SQL runs only in `adapters/store.py`.
- **The hardest correctness problem was solved properly.** The Chicago-day boundary uses `zoneinfo`, not a fixed UTC offset, and is tested on the 23-hour and 25-hour days.
- **The team recorded conflicts instead of hiding them.** The task ID collision produced a published map rather than a quiet renumber. The risk register marks risks "Occurred" rather than editing them down.

## Findings and Root Causes

### F-1 — The release was tagged, but the product was never deployed

**What happened.** Tag `A5Cycle1Release` was cut on 2026-11-09. The bot has run end to end exactly once, on one developer's laptop, against that developer's own test bot.

**Evidence.** Risk 14, "Occurred for Cycle 1." V-2 to V-4 have never run. Architecture Section 11, CC-1.

**Root cause.** ADR-0006 adopted a host *conditional on* verification checks V-2 to V-4 passing. The decision was accepted without those checks being scheduled or assigned, so the condition had no owner. A conditional decision with an unowned condition is an unmade decision that looks made.

**What we would do differently.** A decision that depends on a verification does not get accepted until the verification has an owner and a date in the same pull request that accepts it.

### F-2 — Duplicate-update protection went 39 days without an owner

**What happened.** T-30 was written down on 2026-10-15 and remained an unimplemented `TODO` in `src/bot/web.py` on `main` until #104 opened on 2026-11-23.

**Evidence.** `src/bot/web.py` line 49. `task-id-map.md` lists T-30 as "TODO: assign." Risk 17 and Risk 23 both record it unowned.

**Root cause.** Two documents recorded two different answers to "who owns this." Architecture Section 11 named Khumoyun; the task plan left the owner blank. When one source names an owner and another does not, every reader resolves the contradiction in whichever direction means the work is not theirs.

**Contributing factor.** T-30 gated deployment, and deployment was not scheduled, so nothing downstream ever pulled on it.

**What we would do differently.** The task plan is the only file permitted to name a task owner. Every other document links to it.

### F-3 — Two documents assigned the same task IDs on the same day

**What happened.** On 2026-10-15, `traceability.md` and `task-plan.md` each assigned T-27, T-28 and T-29 to different work.

**Evidence.** `docs/planning/task-id-map.md`, section "What Went Wrong."

**Root cause.** No single source of truth for identifiers. Two leads each took "the next number" from the document in front of them.

**What we changed.** `task-id-map.md` is now the governing list (#74, merged 2026-10-30).

**Still outstanding.** `docs/planning/` contains both `re-estimation.md` and `reestimation.md` — the same defect class, two files for one subject.

### F-4 — Eight architecture decisions sat in Proposed for 25 days

**What happened.** ADR-0001 to ADR-0008 were opened Proposed on 2026-10-15 and accepted 6 of 6 on 2026-11-09, on issue #56. The team built on them throughout.

**Evidence.** Issue #56 vote tally. Risk 12, now Closed. Raised in the Assignment 3 feedback and still open for two weeks after that.

**Root cause.** The vote had no owner and no date. Because the ADRs blocked no code, closing them never competed with anything that had a deadline.

**What we would do differently.** Every proposal gets an owner and a decision date the day it is opened. Any proposal past its date goes to the top of the next meeting agenda.

### F-5 — A shared evidence file lost content in merge conflicts

**What happened.** The AI-use rows for five merged pull requests (#73, #77, #83, #84, #88) disappeared from `docs/ai/ai-use-log.md` when conflicts were resolved by keeping one side. #89 restored them on 2026-11-09 and added one log file per member.

**Evidence.** Risk 2 and Risk 10, both "Occurred." `docs/ai/ai-log-adiya.md`, `ai-log-bazid.md`, `ai-log-khumoyun.md`, `ai-log-mazen.md` and `ai-log-victoria.md` are all present on `main`.

**Root cause.** One append-only file edited by six people on branches that lived for days. A conflict resolved by keeping one side looks clean in the diff and silently discards the other side's rows.

**What we changed.** Per-member files, which is the right fix and is in place.

**Still outstanding.** The central `ai-use-log.md` and the per-member files both exist, and no document states which is authoritative or when consolidation happens. Sohail has no per-member file. Until that is settled, a row can be in one place, both, or neither — which is how the A5 traceability-summary row went unlogged entirely until 2026-11-23.

### F-6 — The release was tagged while its own release documents were unmerged

**What happened.** The Assignment 5 release package listed nine deliverables. At the tagged commit, `docs/release/` contains three files. `release-notes.md`, `defect-summary.md` and `cycle2-handoff.md` are not on `main`. `known-limitations.md` merged (#97) and was reverted the same day (`265a906`). The defect summary, Cycle 2 handoff and presentation index were opened as #94 on 2026-11-09 and are still unmerged.

**Evidence.** `git ls-tree` at tag `A5Cycle1Release`. PR #94, open.

**Root cause.** The tag was cut against a calendar date rather than against a checklist of merged artifacts. The release package table had a status column, but nothing enforced it before tagging.

**What we would do differently.** The tag is not cut until every row of the release package table reads Merged, confirmed by looking at `main` rather than at a pull request.

### F-7 — Cycle 2 produced no reviewed change for two weeks, and the one commit that landed bypassed review

**What happened.** Between the tag on 2026-11-09 and 2026-11-23, no pull request merged to `main`. The instruction on 2026-11-09 was explicitly to run Cycle 2 planning in parallel with finishing Assignment 5, and not to serialize them.

The single commit that did land, `b789a22` on 2026-11-23, was pushed straight to `main` with no pull request and no reviewer. It was mine. It edited `docs/ai/ai-log-bazid.md` — a low-risk change, but the rule it broke (checkpoint G-1, no self-merge, a non-author reviews before `main`) does not have a low-risk exemption, and the person who broke it is the author of this postmortem.

**Evidence.** `git rev-list --parents -n 1 b789a22` shows a single parent, `8eca1b5`. No pull request references it.

**Root cause (the two-week gap).** Cycle 2 scope was discussed but never written into the repository, so it had no issues, no owners and no dates. Work that exists only in a conversation does not get done.

**Root cause (the bypassed review).** The GitHub web editor defaults its commit target to whatever branch the file was opened from. Opening a file from `main` and then choosing "commit directly to this branch" commits to `main`. Nothing in the workflow stops it: `main` has no branch protection, so the rule exists only in `working-agreements.md` and in people remembering it.

**What we would do differently.** Cycle 2 scope goes into the task plan as numbered, owned, dated tasks before Cycle 1 is tagged. And the no-self-merge rule gets enforced by branch protection on `main` rather than by memory, because a written rule with no mechanism behind it is the same category of failure as an unowned task.

### F-8 — The risk register contains duplicated rows with conflicting statuses

**What happened.** Risks 10 through 23 each appear twice in `docs/planning/risk-register.md`, with different statuses, and the header table has two "Last updated" rows.

**Evidence.** `docs/planning/risk-register.md` on `main`.

**Root cause.** A merge conflict resolved by keeping both sides instead of reconciling them — the mirror image of F-5, where keeping one side lost data. Neither resolution was checked against the rendered file.

**What we would do differently.** Any pull request touching a table-heavy evidence file gets its rendered preview checked, not just its diff.

## Cross-Cutting Pattern

Six of the eight findings are the same failure in different clothes: **work with no single owner and no date does not happen, however important it is, and however clearly it is written down.** T-30 was written down 39 days before anyone built it. The ADR vote was written down, flagged by the instructor, and still took 25 days. The deployment condition was written into an accepted decision and never scheduled.

F-7 adds the second half of the pattern: **a rule with no mechanism behind it is not a control.** The no-self-merge rule is written down, agreed, and was broken by the person writing this document, on the day he wrote it, without noticing. Branch protection would have refused the push. Nothing else was going to.

Documentation was not the weak point. This team documented more than it executed. The weak point was that documents recorded intentions without recording who and when, and that nothing in the workflow refused to proceed when those fields were blank.

## Residual Risks Carried Into Cycle 2

| Risk | Status entering Cycle 2 | Owner |
|------|------------------------|-------|
| Not deployed; V-1 to V-6 never run | Open | TODO: assign |
| T-30 duplicate protection | Implemented in #104, approved, not yet merged | Adiya |
| `/today` not built | Open | TODO: assign |
| Food data synthetic; gram amounts unsupported | Open | Adiya |
| Tester invite check and `/privacy` (T-29, FR-10) | Not started | TODO: assign |
| Per-tester deletion script (T-33) | Not started | TODO: assign |
| Central vs per-member AI log, no stated authority; no file for Sohail | Open | Khumoyun |
| `main` has no branch protection | Open | Victoria |
| Duplicate files: `re-estimation.md` / `reestimation.md` | Open | Bazid |
| Risk register duplicate rows | Open | Mazen |

## Action Items

| # | Action | Owner | Due |
|---|--------|-------|-----|
| A-1 | Merge #104 (T-30). Approved by a non-author on 2026-11-23 | Adiya | 2026-11-24 |
| A-2 | State in `ai-policy.md` which AI log is authoritative and when consolidation happens; create Sohail's per-member file | Khumoyun | 2026-11-24 |
| A-3 | De-duplicate the risk register rows and the header table | Mazen | 2026-11-24 |
| A-4 | Delete `reestimation.md`, keep `re-estimation.md` | Bazid | 2026-11-24 |
| A-5 | Merge or close #94, and land the remaining release documents on `main` before tagging | Victoria | Victoria to confirm in the PR thread |
| A-6 | Task plan becomes the only file naming task owners; other docs link to it | Bazid | 2026-11-24 |
| A-7 | Turn on branch protection for `main`: require a pull request and one non-author approval | Victoria | 2026-11-24 |

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-11-23 | Created for Assignment 6 from repository evidence at commit `8eca1b5` | Bazid |
| 2026-11-23 | Corrected merge dates against `git log`; rewrote F-5 after re-checking `main`; reworded the 10/30 entry; added the direct-to-`main` commit to F-7; attributed the 180-commit figure to Risk 6 | Bazid, after review by Victoria |
