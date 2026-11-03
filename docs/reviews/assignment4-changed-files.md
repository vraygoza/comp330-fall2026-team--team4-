# Assignment 4: Changed-File Index

| Field | Value |
|---|---|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Reviewer | Victoria |
| Issue | #46 |
| Compared | Tag `a3-architecture-review` (commit `42350c6`) to `main` |
| Last updated | 2026-11-03 |

Every file that changed since the Assignment 3 baseline, what changed in it, and who owns it. This is the source for the Changed-File Index in the Assignment 4 Word document.

Totals: 41 files, 2,088 additions, 154 deletions.

## Changed Files

### Code

| File | What changed | Owner | PR |
|---|---|---|---|
| `src/__init__.py` | New, empty package marker | Adiya | #69 |
| `src/README.md` | New. How to run the bot locally and run the tests | Adiya | #69 |
| `src/bot/__init__.py` | New, empty | Adiya | #69 |
| `src/bot/router.py` | New. Turns one Telegram update into one reply; `/start` and the C-1 filtering rules | Adiya | #69 |
| `src/bot/web.py` | New. Flask webhook endpoint, secret-token check, C-1 responses. Not deployed | Adiya | #69 |
| `src/bot/poll.py` | New. Local development runner using `getUpdates`. Dev-only deviation from ADR-0005, recorded in the design check | Adiya | #69 |
| `src/adapters/__init__.py` | New, empty | Adiya | #69 |
| `src/adapters/telegram.py` | New. The only module holding the bot token and webhook secret; `sendMessage`, `getUpdates`, secret comparison | Adiya | #69 |
| `src/core/__init__.py` | New, empty | Adiya | #70 |
| `src/core/food_lookup.py` | New. Food name to calories per serving, refuses unknown and partial matches (AC-6.2) | Adiya | #70 |
| `src/core/sample_foods.json` | New. Eight foods with synthetic calorie values, labeled as not FDC data | Adiya | #70 |
| `src/core/day.py` | New. Chicago day boundary determination (`chicago_day_bounds`) and running total calculation (`total_for_day`) for B2 (#44) | Bazid | #83 |
| `src/core/parser.py` | New. Message parsing converting food and quantities into `ParseResult` with default serving fallback and unknown food detection for K2 (#61) | Khumoyun | #88 |

### Tests

| File | What changed | Owner | PR |
|---|---|---|---|
| `tests/__init__.py` | New, empty | Adiya | #69 |
| `tests/test_router.py` | New. 7 tests: `/start` variants, group chat, no text, ignored updates | Adiya | #69 |
| `tests/test_web.py` | New. 6 tests for contract C-1: valid update, missing and wrong secret, bad body | Adiya | #69 |
| `tests/test_telegram_adapter.py` | New. 4 tests: missing token, failed send, network error, secret comparison. Asserts the token never reaches the log | Adiya | #69 |
| `tests/test_food_lookup.py` | New. 8 tests: known foods, plurals, unknown, bad input, partial-word refusal, data validation | Adiya | #70 |
| `tests/test_day.py` | New. 13 tests: Chicago day bounds, midnight, both 23h and 25h DST transitions, running total summation | Bazid | #83 |
| `tests/test_day_contract.py` | New. 10 contract tests verifying contract C-6 and Chicago calendar day semantics | Adiya | #77 |
| `tests/test_parser.py` | New. 11 tests: numeric amounts, units, serving fallback, negative amounts, unknown foods | Khumoyun | #88 |
| `tests/test_parser_contract.py` | New. 11 contract tests verifying contract C-2 interface conformance | Adiya | #77 |

### Configuration and CI

| File | What changed | Owner | PR |
|---|---|---|---|
| `requirements.txt` | New. One runtime dependency, `Flask==3.1.3`. Everything else is the standard library (ADR-0005) | Adiya | #69 |
| `.env.example` | New. Names the three environment variables and warns never to commit `.env` | Adiya | #69 |
| `.github/pull_request_template.md` | New. Linked issue, what changed, evidence, risks, tests run, AI assistance, reviewer checklist | Victoria | #65 |
| `.github/workflows/ci.yml` | New. GitHub Actions workflow running tests on Python 3.12 and automated secrets/token regex check (issue #57, M2) | Mazen | #73 |

### Documentation and Reviews

| File | What changed | Owner | PR |
|---|---|---|---|
| `README.md` | Updated project status, local setup and test execution instructions, and evidence map | Victoria, Adiya | #67, #68 |
| `docs/ai/ai-use-log.md` | Updated with Assignment 4 six-column schema; records all AI-assisted changes through K2 parser (#88) | Khumoyun, Team | #82, #88 |
| `docs/architecture/README.md` | Fixed index location (recovered from deleted nested path) and restored evidence links | Adiya | #71 |
| `docs/architecture/api-contracts.md` | Updated contract C-1 duplicate check (T-30), C-2 parser signature, and C-6 day bounds | Adiya | #71, #75 |
| `docs/architecture/architecture.md` | Added Section 11 (Construction Changes CC-1 to CC-5) recording deviations from A3 design | Adiya | #71 |
| `docs/architecture/docs/architecture/README.md` | Deleted erroneous duplicate nested README | Adiya | #71 |
| `docs/meeting-notes.md` | Added formal meeting notes and action items for 2026-10-26 and 2026-10-30; recorded team change | Victoria | #81 |
| `docs/planning/schedule.md` | Updated working schedule with PR links, milestone statuses, and team change notes | Bazid | #79 |
| `docs/planning/task-id-map.md` | New. Governing list of task IDs T-27 to T-35, resolving A3 review ID collision | Bazid | #74 |
| `docs/planning/task-plan.md` | Reconciled task IDs T-27 to T-35 with task ID map; updated owner proposals and statuses | Bazid | #85 |
| `docs/reviews/a1-design-check.md` | New. Detailed interface comparison between A3 design and A4 tasks; records Findings 1–8 | Adiya | #64 |
| `docs/reviews/architecture-review.md` | New. Formal architecture and ADR review record accepting ADR-0001 through ADR-0008 | Sohail, Mazen | #72 |
| `docs/reviews/assignment4-changed-files.md` | New. Index of all 41 changed files, owners, PRs, and workflow traces | Bazid, Khumoyun | #84 |
| `docs/reviews/assignment4-review-package.md` | New. Comprehensive index of deliverables, evidence, workflow story, and known gaps | Victoria | #68 |
| `docs/testing/test-cases.md` | New. Acceptance test case matrix covering Cycle 1 Must criteria | Sohail, Bazid | #72 |

## Areas That Did Not Change

| Area | Why |
|---|---|
| `docs/architecture/data-context.md`, `architecture-diagram.dot`, `.png` | The core data model and high-level component diagram established at A3 remain current. Section 11 of `architecture.md` records construction-level deviations. |
| `docs/decisions/adr-0001` to `adr-0008` | Content stable; accepted at architecture review (`architecture-review.md`). Team vote issue #56 formalizes repository status change. |
| `docs/requirements/requirements.md`, `open-questions.md` | Requirements are locked for Cycle 1. Open questions OQ-2, OQ-4, and OQ-5 await live verification tasks V-1 through V-6. |
| `docs/planning/scope.md` | Cycle 1 scope (S1–S8 committed, O1–O2 optional) remains unchanged. |

## Workflow Examples

Four changes traced from issue to merge.

**1. Bot skeleton**  
Issue #48 → branch `feature/a2-bot-skeleton` → PR #69 → review requested from Sohail and Khumoyun; Victoria submitted a review → 17 tests run locally, all passed; wrong webhook secret returned 403 → merged 2026-11-02.

**2. Food lookup**  
Issue #49 → branch `feature/a3-food-lookup` → PR #70 → review by Sohail → 25 tests run locally (A2 plus A3), all passed → merged 2026-10-29.

**3. Task ID map**  
Issue from A3 feedback → branch `Kbazid330-patch-1` → PR #74 → review by Adiya, who requested five changes; all applied → approved → merged 2026-10-30. Follow-on PR #75 updated the three places in the code and docs that still used the old ID.

**4. Message parser (K2)**  
Issue #61 → branch `feature/k2-parser` → PR #88 → reviewed by Adiya, who requested decoupling parser from `food_lookup`, removing response wording from parser, removing root test script, and resolving contract test file duplicate → all applied → all 11 contract tests and 51 total tests passed locally → approved → merged 2026-11-03.

**Note on CI:** Merges prior to PR #73 had no automated CI check. From PR #73 onward, GitHub Actions automatically executes the secrets scan and full unit test suite on every pull request.

## Board Check

All merged pull requests have been moved to the "Done" column on the Assignment 4 GitHub Projects board.

## Open Pull Requests Not in This Comparison

All core construction pull requests (#64, #65, #67, #68, #69, #70, #71, #72, #73, #74, #75, #77, #79, #81, #82, #83, #84, #85, #88) have merged into `main`.

Remaining construction work:
- Integration work (Issue #50, A4): Wires parser, food lookup, and daily total together inside `src/bot/router.py`. Branch/PR not yet opened; now unblocked by merges of #83 and #88.

## Change Log

| Date | Change | By |
|---|---|---|
| 2026-11-02 | Created from the `a3-architecture-review`-to-`main` comparison | Bazid |
| 2026-11-02 | Updated the open pull requests table, example 1 and the board-check note after review | Victoria |
| 2026-11-03 | Fully updated to 41 changed files, 2,088 additions; added K2 parser workflow example, day/parser modules, contract tests, and review documents | Khumoyun |
