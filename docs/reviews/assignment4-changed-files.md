# Assignment 4: Changed-File Index

| Field | Value |
|-------|-------|
| Owner | Bazid (Planning & Process Lead) |
| Backup | Victoria (Team Lead) |
| Reviewer | Victoria |
| Issue | #46 |
| Compared | Tag `a3-architecture-review` (commit `42350c6`) to `main` |
| Last updated | 2026-11-02 |

Every file that changed since the Assignment 3 baseline, what changed in it, and who owns it. This is the source for the Changed-File Index in the Assignment 4 Word document.

Totals: 22 files, 908 additions, 1 deletion.

## Changed Files

### Code

| File | What changed | Owner | PR |
|------|--------------|-------|----|
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

### Tests

| File | What changed | Owner | PR |
|------|--------------|-------|----|
| `tests/__init__.py` | New, empty | Adiya | #69 |
| `tests/test_router.py` | New. 7 tests: `/start` variants, group chat, no text, ignored updates | Adiya | #69 |
| `tests/test_web.py` | New. 6 tests for contract C-1: valid update, missing and wrong secret, bad body | Adiya | #69 |
| `tests/test_telegram_adapter.py` | New. 4 tests: missing token, failed send, network error, secret comparison. Asserts the token never reaches the log | Adiya | #69 |
| `tests/test_food_lookup.py` | New. 8 tests: known foods, plurals, unknown, bad input, partial-word refusal, data validation | Adiya | #70 |

### Configuration and dependencies

| File | What changed | Owner | PR |
|------|--------------|-------|----|
| `requirements.txt` | New. One runtime dependency, `Flask==3.1.3`. Everything else is the standard library (ADR-0005) | Adiya | #69 |
| `.env.example` | New. Names the three environment variables and warns never to commit `.env` | Adiya | #69 |
| `.github/pull_request_template.md` | New. Linked issue, what changed, evidence, risks, tests run, AI assistance, reviewer checklist | Victoria | #65 |

### Documentation

| File | What changed | Owner | PR |
|------|--------------|-------|----|
| `docs/reviews/a1-design-check.md` | New. Compares the A3 design with the A4 task cards; fixes the interfaces for K2, A3 and B2; records 8 findings | Adiya | #64 |
| `docs/planning/task-id-map.md` | New. Governing list of task IDs T-27 to T-35, resolving the collision the A3 review found | Bazid | #74 |
| `docs/ai/ai-use-log.md` | Rows added for every AI-assisted change in this window | Adiya, Bazid | #64, #69, #70, #74 |

## Areas That Did Not Change

| Area | Why |
|------|-----|
| `docs/architecture/architecture.md`, `api-contracts.md`, `data-context.md`, the diagram | The A3 baseline is still the design under construction. Changes recording how the code differs are in PR #71, not yet merged |
| `docs/decisions/adr-0001` to `adr-0008` | All still Proposed. Acceptance is the team vote, issue #56. The A1 design check is the input to that vote, not a substitute for it |
| `docs/requirements/requirements.md`, `open-questions.md` | Requirements did not change during construction. Open questions OQ-2, OQ-4 and OQ-5 stay open until V-1 to V-6 run |
| `docs/planning/scope.md` | Cycle 1 scope is unchanged |

## Workflow Examples

Three changes traced from issue to merge.

**1. Bot skeleton**
Issue #48 → branch `feature/a2-bot-skeleton` → PR #69 → review requested from Sohail and Khumoyun; Victoria submitted a review → 17 tests run locally, all passed; wrong webhook secret returned 403 → merged 2026-11-2.

**2. Food lookup**
Issue #49 → branch `feature/a3-food-lookup` → PR #70 → review by Sohail → 25 tests run locally (A2 plus A3), all passed → merged 2026-10-29.

**3. Task ID map**
Issue from the A3 feedback → branch `Kbazid330-patch-1` → PR #74 → review by Adiya, who requested five changes; all applied → approved → merged 2026-10-30. Follow-on PR #75 updated the three places in the code and docs that still used the old ID.

**Note on CI:** none of these merges had a CI check. The workflow is in PR #73 and had not merged at the time. From #73 onward, pull requests run the check automatically.

## Board Check

Board check: not completed at the time of this snapshot; see the Assignment 4 board for current status.

## Open Pull Requests Not in This Comparison

These were open when the comparison was taken, so their files are not listed above.

| PR | Contents | Owner |
|----|----------|-------|
| #71 | Architecture index fix and the construction-change record (Section 11) | Adiya |
| #72 | Architecture review, A4 test matrix. Unowned since the team change | — |
| #73 | CI workflow and secrets check | Mazen |
| #77 | Contract tests for the parser and daily total | Adiya |
| #85 | Task plan renumbered to the governing IDs | Bazid |
| #79 | Schedule updated through A4 | Bazid |
| #80 | README change in a stacked pull request, to be closed because #67 merged | Victoria |
| #81 | Meeting notes for 10/26 and 10/30 | Victoria |
| #82 | AI-use log, six-column format | Khumoyun |
| #83 | `src/core/day.py` and its tests, issue #44 | Bazid |

#67 and #68 were also open when the comparison was taken and have since merged.

This index is regenerated against `main` before the Assignment 4 tag.

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-11-02 | Created from the `a3-architecture-review`-to-`main` comparison | Bazid |
| 2026-11-02 | Updated the open pull requests table, example 1 and the board-check note after review | Victoria |
