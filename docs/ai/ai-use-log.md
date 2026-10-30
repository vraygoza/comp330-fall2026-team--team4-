# AI Use Log

Track all AI tool usage for transparency and academic integrity purposes. Every AI-assisted change gets a row here, with what a human checked or changed before commit.

## Log Format

Date | Tool | Feature/File | Type of Use | Team Member | Notes

## Types of Use

- Code Generation
- Code Review
- Documentation
- Testing/Debugging
- Research/Brainstorming
- Other (specify)

## Log

| Date | Tool | Feature/File | Type of Use | Team Member | Notes |
|---|---|---|---|---|---|
| 2026-09-08 | GitHub Copilot | meeting-notes.md | Documentation | vraygoza | Initial template creation |
| 2026-09-19 | Google Antigravity (Claude) | Multiple docs files | Documentation | Khumoyun | Replaced all instances of misspelled names (Sophail to Sohail, Khumonyun to Khumoyun) across the repo |
| 2026-09-29 | Claude | README.md, docs/planning/README.md, docs/planning/scope.md, docs/requirements/requirements.md, docs/requirements/open-questions.md | Documentation | Adiya | Drafted from existing repo contents; reviewed and edited by Adiya before commit |
| 2026-10-01 | Google Antigravity (Claude) | docs/decisions/deferred-scope.md | Documentation | Khumoyun | Drafted deferred scope and tradeoff decisions from existing scope.md and planning evidence; reviewed and edited by Khumoyun before commit |
| 2026-10-01 | Claude | docs/planning/traceability.md, docs/planning/risk-register.md, docs/decisions/tradeoff-records.md | Documentation | Mazen | Drafted with help from Claude from existing planning docs; reviewed and edited by Mazen before commit |
| 2026-10-14 | Claude | docs/architecture/README.md | Documentation | vraygoza | Drafted from the A3 instructions and A2 feedback; reviewed and edited by Victoria before commit |
| 2026-10-14 | Claude | docs/architecture/architecture.md, api-contracts.md, architecture-diagram.dot and .png, investigations/inv-01-lookup-storage.md, technical-recommendations.md; docs/requirements/requirements.md, open-questions.md; spikes/inv-01-lookup-storage/ (code, synthetic fixtures, results) | Documentation, Code Generation, Research | Adiya | Drafted from the A2 files, A2 feedback and public Telegram, USDA FDC, Render, Neon and PythonAnywhere docs. Fixture calorie values are synthetic and labeled as such. Spike ran offline (19 cases, 14 of 14 checks passed); live FDC check not yet run. Reviewed by Adiya before upload; PR #23 reviewers: Sohail, Khumoyun |
| 2026-10-14 | Google Antigravity (Claude) | docs/meeting-notes.md | Documentation | Khumoyun | Organized Oct 14 meeting notes from a rough draft into the established format; reviewed and edited by Khumoyun before commit |
| 2026-10-15 | Claude | docs/planning/re-estimation.md, docs/planning/task-plan.md | Documentation | Bazid | Drafted re-estimation from INV-01 findings and the A2 estimates; added architecture tasks T-27 to T-34, verification tasks V-1 to V-6, and proposed owners for unassigned work. Reviewed and edited by Bazid before commit; PRs #31 and the stacked follow-on, reviewers Victoria and Khumoyun |
| 2026-10-14 | Claude | docs/architecture/README.md, README.md | Documentation | vraygoza | Drafted from the A3 instructions and A2 feedback; reviewed and edited by Victoria before commit |
| 2026-10-15 | Claude | docs/decisions/adr-0001 to adr-0008, decision-log.md, tradeoff-records.md; docs/architecture/data-context.md; docs/planning/risk-register.md, traceability.md | Documentation | Mazen | Drafted from INV-01, the architecture docs and Victoria's A3 action plan. Reviewed and edited by Mazen before commit |
| 2026-10-26 | Claude (Opus 5.5) | docs/reviews/a1-design-check.md | Documentation, Code Review | Adiya | Claude compared ADR-0001 to 0008, architecture.md and api-contracts.md with the A4 task cards and drafted the language choice, interfaces and Findings 1 to 8. Adiya uploaded it on 10/28. Content review by Mazen in PR #64 (issue #47) |
| 2026-10-26 | Claude (Opus 5.5) | src/bot/, src/adapters/telegram.py, requirements.txt, .env.example, src/README.md, tests/test_router.py, tests/test_web.py, tests/test_telegram_adapter.py | Code Generation, Testing | Adiya | Bot skeleton for #48. Rejected: python-telegram-bot (ADR-0005). Claude ran the 17 tests and a simulated /start webhook check on the uploaded branch (commit 32d7c7e, 10/28): all passed, wrong secret returned 403. Adiya ran the full suite on her Mac (Python 3.15.2) on 10/29 from the A3 branch, which includes A2: 25 tests, OK. Not yet run with a live Telegram bot. Adiya uploaded; review by Sohail in PR #69 (issue #48) |
| 2026-10-26 | Claude (Opus 5.5) | src/core/food_lookup.py, src/core/sample_foods.json, tests/test_food_lookup.py | Code Generation, Testing | Adiya | Food lookup for #49. Calorie values are made up and labeled synthetic. Partial matches such as egg roll are refused, not guessed (AC-6.2). Claude ran 25 tests (A2 plus A3), all passed. Adiya ran the same 25 tests on her Mac (Python 3.15.2) on 10/29: OK. Adiya uploaded; review by Sohail in PR #70 (issue #49) |
| 2026-10-29 | Claude (Opus 5) | docs/planning/task-id-map.md | Documentation | Bazid | Reconciled the conflicting T-27 to T-29 IDs between traceability.md and task-plan.md flagged in the A3 review; added done criteria for the privacy, security and verification tasks. Reviewed and edited by Bazid before commit; PR reviewers Mazen and Adiya |
| 2026-10-29 | Claude (Opus 5.5) | .github/workflows/ci.yml | Documentation/Code Help | Mazen | CI workflow for #57 (M2). Claude helped to finish draft of workflow and its secrets check and also searched the repo for secrets. Mazen read and reviewed all. #73 CI run: secrets check passed, tests failed as expected because main had no tests/ yet. Accepted as drafted; Review by Adiya in PR #73 |
Add a new row for every AI-assisted file in Assignment 3, and name who checked it.

## Summary Statistics

- Total AI-assisted sessions: 8
- Most used tool: Claude (7 of 8, including via Google Antigravity)
- Total AI-assisted sessions: 10
- Most used tool: Claude (9 of 10, including via Google Antigravity)
- Primary use cases: Documentation, Code Generation
