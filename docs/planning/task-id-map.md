# Task ID Map

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Last updated | 2026-10-29 |
| Status | Proposed — needs confirmation from Mazen (traceability) and Adiya (architecture) |

One governing list of task IDs T-27 through T-35. This resolves the conflict the A3 review identified: `traceability.md` and `task-plan.md` both used T-27, T-28 and T-29 for different work.

## What Went Wrong

On 2026-10-15, two documents assigned the same IDs to different tasks on the same day, neither checking the other.

| ID | In traceability.md (Mazen) | In task-plan.md (Bazid) |
|----|---------------------------|-------------------------|
| T-27 | Data-model review against NFR-4 | Duplicate `update_id` protection |
| T-28 | Weekly free-tier usage check | `food_cache` table and refresh |
| T-29 | Tester invite check and `/privacy` reply | Webhook secret validation |

The A3 review named the consequence directly: someone could build a cache while another person expects a privacy check.

## Rule Used to Resolve It

`traceability.md` proposed T-27 to T-29 under the heading "For Bazid to add to the Task Plan." Those IDs were assigned first and handed over for adoption, so they keep their numbers. The task-plan entries shift up. Two task-plan entries turned out to duplicate Mazen's T-29 and are merged into it rather than renumbered.

## Governing Task IDs

| ID | Task | Traces to | Owner | Previously called |
|----|------|-----------|-------|-------------------|
| T-27 | Review the database tables against NFR-4 before the Entry Store merges: only the fields listed in Data and Context are stored | NFR-4 | Mazen | — |
| T-28 | Weekly health check: outcome counts, reply times and FDC calls per hour against free-tier limits | NFR-5, Risk 5 | Adiya | — |
| T-29 | Build the tester invite check and the `/privacy` reply | FR-10 (AC-10.1 to AC-10.3), OQ-8, G-4 | TODO: assign | absorbs old T-30 and T-34 |
| T-30 | Record processed `update_id` values in the same transaction as the entry | C-1, INV-01 Finding 7 | TODO: assign | task-plan T-27 |
| T-31 | Build `food_cache` table, loader, and 30-day refresh rule | C-5, INV-01 Finding 8 | TODO: assign | task-plan T-28 |
| T-32 | Check `X-Telegram-Bot-Api-Secret-Token`; return 403 and log AUTH_REJECTED | C-1, TB-1 | TODO: assign | task-plan T-29 |
| T-33 | Write and test the per-tester deletion script | OQ-8, C-6, G-5 | TODO: assign | task-plan T-31 |
| T-34 | Deploy smoke test: `/start`, `2 eggs`, `/today` on a dev account | G-3 | Adiya | task-plan T-32 |
| T-35 | Nightly `sqlite3 .backup` of `bot.db` on the host | architecture.md §8 recovery | TODO: assign | task-plan T-33 |

Verification tasks V-1 through V-6 are unchanged. They appear only in `task-plan.md` and never collided.

## Merged Entries

Two task-plan entries described work Mazen had already captured under T-29.

| Old ID | Old task | Why merged |
|--------|----------|------------|
| T-30 | Write `/privacy` command and collection notice text | T-29 already covers the `/privacy` reply |
| T-34 | Tester invite code check in the Register use case | T-29 already covers the tester invite check |

T-29 now carries both, so the privacy notice and the invite gate stay with one owner.

## Done Criteria for the Consequential Tasks

The A3 review asked for completion criteria on the privacy, security and verification work, not just task names.

| ID | Done when |
|----|-----------|
| T-27 | The `users`, `entries`, `food_cache` and `processed_updates` tables are compared field by field against the list in `data-context.md`; any field not on that list is removed or justified in writing; result recorded in the PR that merges the Entry Store |
| T-29 | An unregistered Telegram ID gets the closed-test reply and no row is created; `/privacy` returns the collection notice; both verified with two synthetic accounts |
| T-30 | The same `update_id` sent twice produces one entry; verified by a unit test with a fake adapter |
| T-32 | A request with a wrong or missing secret header returns 403, logs AUTH_REJECTED, and runs no handler code; verified by unit test and once on the live host (V-3) |
| T-33 | The script removes one tester's rows and leaves every other tester's rows intact; run by one developer and confirmed by a second, per checkpoint G-5 |

## What Has to Change

| File | Change | Owner |
|------|--------|-------|
| `task-plan.md` | Renumber the architecture tasks to T-30 to T-35; add Mazen's T-27 to T-29 with estimates; delete the two merged rows | Bazid |
| `traceability.md` | Mark the "Proposed New Tasks" section adopted; point the NFR-4 and NFR-5 rows at T-27 and T-28 as governing | Mazen |
| `re-estimation.md` | Re-estimate under the new IDs; T-29 is unestimated and needs one | Bazid |
| `risk-register.md` | Update any task references that moved | Mazen |

## How to Keep This From Happening Again

Before proposing a new task ID, check this file for the highest ID in use and take the next one. Any new task is added here first, then referenced from `task-plan.md` and `traceability.md`. This file is the single source for task IDs.

## Confirmation

The A3 review asked that the relevant owners confirm the mapping.

| Owner | Role | Confirmed | Date |
|-------|------|-----------|------|
| Mazen | Operations & Evidence Lead (traceability.md) | | |
| Adiya | Architecture & Development Lead | | |
| Victoria | Team Lead | | |

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-10-29 | Created to resolve the T-27 to T-29 collision found in the A3 review | Bazid |
