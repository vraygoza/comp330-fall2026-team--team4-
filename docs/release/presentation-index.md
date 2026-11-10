# Assignment 5 Presentation & Evidence Index

| Field | Detail |
|---|---|
| Compiler | Sohail Shaik (Quality & Review Lead) |
| Date | 2026-11-09 |
| Release Baseline | Tag a5-cycle1-release |
| Governing Requirements | C-1 through C-8, ADR-0001 through ADR-0009 |
| Distribution | Team 4 Repository & Sakai Release Package |

---

## 1. Presentation Artifacts

- Slide Deck Location: Stored in repository at docs/release/slides-cycle1-final.pdf (or linked Google Slides deck).
- Structure and Ownership:
  - Slide 1: Title, Team Roster, and Cycle 1 Release Goal — Victoria Raygoza
  - Slide 2: User Journey and Vertical Slice Architecture — Adiya
  - Slide 3: Construction Highlights and Implementation Details — Bazid and Khumoyun
  - Slide 4: Live Demonstration Walkthrough and Verification — Victoria Raygoza
  - Slide 5: Automated Testing, CI Suite, and Secrets Scanning — Mazen Malas
  - Slide 6: Review Discipline, Quality Gates, and Cycle 2 Handoff — Sohail Shaik

---

## 2. Core Repository Evidence Links

- Demonstration Script: docs/release/demo-script.md
- Traceability Matrix: docs/release/traceability-summary.md
- Continuous Integration Runs: docs/testing/ci-evidence.md
- Defect and Remediation Log: docs/release/defect-summary.md
- Cycle 2 Technical Handoff: docs/release/cycle2-handoff.md
- Known Limitations Log: docs/release/known-limitations.md
- Scope Boundaries and Architecture: docs/architecture/architecture.md

---

## 3. Demonstration Script & Fallback Procedures

- Primary Demonstration: Recorded or live walkthrough of the Telegram bot executing the standard user flow defined in demo-script.md:
  1. User onboarding via /start command.
  2. Single food item logging with default portion resolution (e.g., 2 eggs).
  3. Running total query via /today reflecting Chicago local day aggregation.
  4. Negative path demonstration rejecting unmapped input without crashing.
  5. Multi-user test confirming separate calorie totals between two distinct Telegram accounts.
- Backup Plan: Local command-line execution running tests/test_integration.py against an ephemeral SQLite database, displaying exact JSON payloads and database state transitions if network connectivity fails.