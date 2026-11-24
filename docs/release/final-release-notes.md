# Final Release Notes: Assignment 6 (`a6-final-release`)

| Field | Value |
|---|---|
| **Release Tag** | `a6-final-release` (to be created at the freeze) |
| **Release Date** | 2026-11-23 (to be created at the freeze) |
| **Owner** | Khumoyun (Operations & Evidence Co-Lead) |
| **Backup** | Mazen (Operations & Evidence Lead) |
| **Reviewer** | Victoria (Team Lead) |
| **Target Runtime** | Python 3.12 (ADR-0009) |
| **Test Suite Status** | 93 passing tests on `main` (`python -m unittest discover -s tests -t .`) |

---

## 1. Executive Summary & Honest Scope Boundary

This document provides the final release notes for the COMP 330 Team 4 Telegram Calorie Tracker bot for Assignment 6.

### The Honest Status: Small Slice, High Rigor
The project follows an explicit engineering constraint: **no unverified features, no placeholders, and honest release status**. 

The release delivers a functional, locally verified **vertical slice** of the calorie tracking workflow:
1. A tester sends `/start` to register their Telegram account in a local SQLite store (`bot.db`).
2. The tester sends a plain text message containing a single food item with a count (e.g., `2 eggs`) or without a count (e.g., `banana`), which defaults to 1 standard serving.
3. The bot parses the message, looks up the nutritional data against a curated local dataset of 8 synthetic foods (`egg`, `banana`, `apple`, `taco`, `rice`, `toast`, `yogurt`, `pizza slice` in `src/core/sample_foods.json`), and calculates calories.
4. The entry is securely persisted under the tester's unique ID in SQLite (`src/adapters/store.py`), strictly isolated from other users (AC-7.1).
5. The bot calculates the cumulative daily calorie total based on the America/Chicago day boundary (midnight to midnight) via `src/core/day.py` and replies with the logged food and total.
6. If an unknown food is submitted, or if an unexpected runtime failure occurs, the bot recovers gracefully and safely logs failures without leaking user identifiers or food names (NFR-3, NFR-4).

### What Is Not Shipped in this Release
- **No live cloud deployment:** Host verification checks (`V-2` to `V-4`) on PythonAnywhere are deferred. The bot runs locally via a polling runner (`python -m src.bot.poll`) rather than a public HTTPS webhook.
- **No live USDA API connection:** Verification check `V-1` is deferred. Food resolution uses an internal curated fixture of 8 foods (`sample_foods.json`), not the external FoodData Central (FDC) API.
- **No external outside testers:** Because the bot runs on a local polling daemon rather than a deployed cloud host, trial testing with outside users is deferred.
- **No deferred features:** Multi-food parsing (`DF-2`), macronutrients (`DF-1`), `/undo` (`FR-8`), and manual calorie entry (`FR-9`) are deferred to future cycles.

---

## 2. What Shipped vs. What Is Deferred

The following matrix records the exact disposition of all functional and non-functional requirements:

| Requirement / Item | Description | Status in `a6-final-release` | Evidence / Notes |
|---|---|---|---|
| **FR-1** | `/start` registration and instructions | **Shipped** | Verified in `tests/test_log_food.py` (`test_start_registers_and_welcomes`) |
| **FR-2** | Log one food per message | **Shipped** | Parser handles count (`2 eggs`) and default serving (`banana`) |
| **FR-3** | Nutrition calorie lookup | **Shipped (Sample Data)** | Local lookup against 8 curated foods; FDC live API deferred (CC-1) |
| **FR-4** | Reply with running daily total | **Shipped** | Replies format logged calories and cumulative daily total |
| **FR-5** | Chicago day total cutoff | **Shipped** | Handled by Day module (`src/core/day.py`); handles DST transitions |
| **FR-5 (Standalone)** | `/today` query command | **Deferred** | TODO: Dedicated query use case deferred (CC-8, Task T-15) |
| **FR-6** | Clear unknown food response | **Shipped** | Unknown foods return friendly notice; nothing saved (AC-6.1) |
| **FR-7** | Multi-tester data isolation | **Shipped** | Enforced by SQLite schema; verified in `test_tester_a_never_sees_tester_b` |
| **FR-8 (O1)** | `/undo` last food entry | **Deferred** | Scope dropped in Cycle 1 to protect the vertical slice (DF-7, T-20) |
| **FR-9 (O2)** | Manual calorie entry | **Deferred** | Optional feature deferred (FR-9, T-21) |
| **FR-10** | Closed tester invite check & `/privacy` | **Deferred** | Task T-29 deferred to live deployment phase |
| **NFR-1** | Response latency (< 5 seconds) | **Shipped (Local)** | Local in-memory lookup runs without external network calls; not formally measured on deployed host |
| **NFR-2** | 15 concurrent tester capacity | **Deferred** | Local single-worker polling runner; cloud scaling deferred |
| **NFR-3** | Zero secrets in repository | **Shipped** | Tokens loaded via `.env`; regex check enforced in `.github/workflows/ci.yml` |
| **NFR-4** | Minimal PII & safe logging | **Shipped** | Lookup failures emit generic logs; no chat IDs or food names logged |
| **NFR-5** | Zero service costs (free tiers) | **Shipped** | Zero paid services used |
| **T-30 / CC-5** | Duplicate `update_id` protection | **Pending Freeze Review** | Implemented in PR #104 by Adiya with atomic SQLite storage. If merged before tag, active; if unmerged at freeze, marked deferred. |

---

## 3. Automated Test Verification

All software verification runs automatically in GitHub Actions CI on Python 3.12 (ADR-0009):

- **Total Test Count:** 93 automated tests passing on `main`.
- **Test Execution Command:**
  ```bash
  python -m unittest discover -s tests -t .
  ```
- **Test Suite Breakdown:**
  - `tests/test_parser.py` & `tests/test_parser_contract.py`: Message parsing rules, quantities, edge cases, whitespace, units.
  - `tests/test_food_lookup.py`: Exact and alias lookup, casing, unknown food refusals, sanitized error logging.
  - `tests/test_day.py` & `tests/test_day_contract.py`: America/Chicago calendar calculations, midnight cutoff, daylight saving transitions.
  - `tests/test_store.py`: SQLite user registration, entry insertion, user data separation, UTC timestamp sorting.
  - `tests/test_log_food.py`: End-to-end core use case integration, running totals, default serving messages.
  - `tests/test_router.py`: Bot routing, start command, food logging, crash protection, and error recovery.
  - `tests/test_telegram_adapter.py`: Telegram API client configuration and network message sending.
  - `tests/test_web.py`: Webhook endpoint handling and secret token verification.
  - **Secrets Verification:** Automated regex scan in `.github/workflows/ci.yml` ensuring no bot tokens or API keys exist in git history or tracked files.

---

## 4. Known Limitations & Constraints

A detailed matrix of limitations is recorded in [Known Limitations](known-limitations.md). Key operational limits include:
1. **Single Food Per Message:** Multi-food parsing (e.g., `"eggs and toast"`) is not supported (TD-1).
2. **Serving Units Only:** Gram quantities (e.g., `100g chicken`) are parsed but refused with an explanatory notice until real nutrition data is connected (CC-2, CC-7).
3. **Curated Food Fixture:** Only 8 foods are recognized (`egg`, `banana`, `apple`, `taco`, `rice`, `toast`, `yogurt`, `pizza slice` in `src/core/sample_foods.json`).
4. **Local Runner:** Operational execution is managed via `python -m src.bot.poll` on a developer workstation.

---

## 5. Operations & Runbook Reference

For instructions on configuring environment variables, running the local polling daemon, inspecting the database, and executing disaster recovery backups, consult the [Operations Runbook](../operations/runbook.md).

---

## 6. Assignment 6 Release Package & Deliverables Map

The Assignment 6 final release package brings together deliverables across all five team members. The table below maps each deliverable, its assigned owner, and its repository status at the time of authoring:

| Deliverable / Artifact | Path | Owner | Status for Final Release |
|---|---|---|---|
| **Final Release Notes** | `docs/release/final-release-notes.md` | Khumoyun | **This PR** (complete) |
| **Known Limitations & Deferred Scope** | `docs/release/known-limitations.md` | Khumoyun | **This PR** (complete) |
| **Operations Runbook** | `docs/operations/runbook.md` | Khumoyun | **This PR** (complete) |
| **Duplicate Update Protection (T-30)** | `src/adapters/store.py`, `src/bot/router.py` | Adiya | In **PR #104** (pending final merge review; deferred if unmerged at freeze) |
| **Cycle 1 Postmortem** | `docs/operations/postmortem-cycle1.md` | Bazid | In **PR #105** (pending review updates) |
| **Changed Files Since A5** | `docs/release/changed-files-since-a5.md` | Bazid | Assigned for A6 freeze |
| **Demo Script & Verification** | `docs/release/demo-script.md` | Victoria | In **PR #106** (93 tests passing on `main`) |
| **Presentation Index** | `docs/release/presentation-index.md` | Victoria | In **PR #106** (team presentation roadmap) |
| **Release Tag & Package** | Tag `a6-final-release`, release archive | Victoria | Authored at freeze after all PRs merge |
| **Final Test & CI Evidence** | `docs/testing/final-test-evidence.md`, `ci-evidence.md` | Mazen | In **PR #107** (updated with 93 tests passing on `main`) |
| **Cycle 2 Maturity Summary** | `docs/release/cycle2-maturity-summary.md` | Mazen | In **PR #107** (Cycle 2 architectural roadmap) |
| **Security Checklist** | `docs/security/security-checklist.md` | Sohail | Assigned for A6 (Mazen reviewing) |
| **Defect Summary** | `docs/quality/defect-summary.md` | Sohail | Assigned for A6 (Mazen reviewing) |

---

## 7. Project Governance & Direct Links

- **Repository Demo Script:** [Demo Script](demo-script.md)
- **Known Limitations:** [Known Limitations](known-limitations.md)
- **Traceability Summary:** [Traceability Summary](traceability-summary.md)
- **Operations Runbook:** [Operations Runbook](../operations/runbook.md)
- **Architecture Documentation:** [Architecture Documentation](../architecture/architecture.md)
- **Deferred Scope & Decisions:** [Deferred Scope](../decisions/deferred-scope.md)
