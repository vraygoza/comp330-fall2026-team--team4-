# CI Evidence

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-11-09 |

What the CI workflow checks, how every run has gone, and why the two failed runs failed. The workflow is [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) (issue #57, PR #73). Its packages and Actions are reviewed in [ADR-0009](../decisions/adr-0009-dependencies.md).

## What CI Checks
It runs on every pull request, on every push to `main`, and by hand. Each run:
1. Checks out the code with a read-only token.
2. **Secrets check:** fails if a `.env`, database or key file is committed, or if any file contains text shaped like a Telegram bot token. It prints file names only, never the value (NFR-3, Risk 6).
3. Sets up Python 3.12 and installs `requirements.txt` (Flask 3.1.3).
4. **Tests:** `python -m unittest discover -s tests -t . -v`, the same command as in [`src/README.md`](../../src/README.md).

## Workflow Status
All 58 runs from 2026-10-29 to 2026-11-09 (checked at 9:20 PM): **56 passed, 2 failed, 0 skipped.** All 20 runs on `main` passed. Full list: [CI runs](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/workflows/ci.yml).

| Run | What it checked | Result | Link |
|-----|-----------------|--------|------|
| CI #1 | PR #73 (the CI workflow), first run, 2026-10-29 | Failed, expected (see below) | [Run](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/runs/40933145054/job/123656584599) |
| CI #2 | PR #73 after merging `main`, 2026-10-30 | Passed | [Run](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/runs/41138778597/job/124347669673) |
| CI #29 | `main` at commit `0a1d54d`, the `a4-construction-integration` tag; 66 tests | Passed | [Run](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/runs/41588453315) |
| CI #31 | PR #90 (integration), 2026-11-03; 88 tests | Passed | [Run](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/runs/41721885473) |
| CI #39 | `main` after PR #90 merged (commit `957e410`), 2026-11-09; 88 tests | Passed | [Run](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/runs/42735779685) |
| CI #40 | `main` after PR #92 merged (commit `efce91f`), 2026-11-09 | Passed | [Run](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/runs/42735908534) |
| CI #42 | PR #96 (K3 logging), 2026-11-09, 7:53 PM | Failed (see below) | [CI runs](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/workflows/ci.yml) |
| CI #46 | PR #96 after the fix (commit `52883ed`) | Passed | [CI runs](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/workflows/ci.yml) |
| All other runs, CI #3 to #58 | 17 more runs on `main` and 33 on pull requests | All passed | [CI runs](https://github.com/vraygoza/comp330-fall2026-team--team4-/actions/workflows/ci.yml) |

## Failed or Skipped Checks
- **CI #1 failed, as expected.** The secrets check passed. The test step failed with "Start directory is not importable: 'tests'" because `main` had no `tests/` folder yet. After the bot skeleton (#69) merged, `main` was merged into the branch and CI #2 passed. The workflow steps were not changed to make it pass.
- **CI #42 failed, and CI caught a real problem.** On PR #96, merging `main` into the branch kept an older `src/bot/router.py`, which removed the food logging added in PR #90; 13 tests in `tests/test_log_food.py` failed. The router was fixed in commit `52883ed`, and CI #46 passed. The broken version never reached `main`.
- **No checks were skipped.**
- **Six pull requests merged before CI existed:** #64, #65, #69, #70, #74 and #75. They had no CI check. The tests from #69 and #70 were run by hand before merging (17 and 25 tests, [A4 changed-file index](../reviews/assignment4-changed-files.md)), and every CI run since CI #3 includes them.
- **PRs #79 and #85 have no pull request run;** their last commits were pushed before CI was added. Their merges into `main` passed (CI #20 and #21).
- **Three commits went straight to `main` without a pull request** (CI #43, #44 and #50 on 2026-11-09). CI checked them only after they landed; all three passed.

## Limits
- The secrets check reads the current files, not git history. The full history was scanned once on 2026-11-09 and was clean ([Risk Register](../planning/risk-register.md), Risk 6).
- CI runs unit and contract tests only. Nothing runs against a live Telegram bot or the host, because the bot is not deployed (Risk 14).
- CI runs on Ubuntu only (ADR-0009 notes the extra Windows step).

## Run It Yourself
From the repository root: `python -m unittest discover -s tests -t .` Re-run a CI run from its page with **Re-run jobs**, or start one from the Actions tab with **Run workflow**.

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-11-09 | Created for Assignment 5: workflow status, run links, and the failed and missing checks explained | Mazen |
| 2026-11-09 | Added the runs through CI #58, including the CI #42 failure on PR #96 and the commits pushed straight to `main` | Mazen |