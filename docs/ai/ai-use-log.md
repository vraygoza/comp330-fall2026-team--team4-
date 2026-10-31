# AI Use Log

Track all AI tool usage for transparency and academic integrity purposes. Every AI-assisted change gets a row here, with what a human checked or changed before commit.

## Log Format

Date | Tool | Feature/File | Type of Use | Team Member | Notes
Tool/Model | Task | Accepted output | Rejected output | Human edits | Verification

## Types of Use

- Code Generation
- Code Review
- Documentation
- Testing/Debugging
- Research/Brainstorming
- Other (specify)

## Log

| Date | Tool | Feature/File | Type of Use | Team Member | Notes |
| Tool/Model | Task | Accepted output | Rejected output | Human edits | Verification |
|---|---|---|---|---|---|
| 2026-09-08 | GitHub Copilot | meeting-notes.md | Documentation | vraygoza | Initial template creation |
| 2026-09-19 | Google Antigravity (Claude) | Multiple docs files | Documentation | Khumoyun | Replaced all instances of misspelled names (Sophail to Sohail, Khumonyun to Khumoyun) across the repo |
| 2026-09-29 | Claude | README.md, docs/planning/README.md, docs/planning/scope.md, docs/requirements/requirements.md, docs/requirements/open-questions.md | Documentation | Adiya | Drafted from existing repo contents; reviewed and edited by Adiya before commit |
| 2026-10-01 | Google Antigravity (Claude) | docs/decisions/deferred-scope.md | Documentation | Khumoyun | Drafted deferred scope and tradeoff decisions from existing scope.md and planning evidence; reviewed and edited by Khumoyun before commit |
| 2026-10-01 | Claude | docs/planning/traceability.md, docs/planning/risk-register.md, docs/decisions/tradeoff-records.md | Documentation | Mazen | Drafted with help from Claude from existing planning docs; reviewed and edited by Mazen before commit |
| 2026-10-14 | Claude | docs/architecture/README.md | Documentation | vraygoza | Drafted from the A3 instructions and A2 feedback; reviewed and edited by Victoria before commit |
| 2026-10-14 | Google Antigravity (Claude) | docs/meeting-notes.md | Documentation | Khumoyun | Organized Oct 14 meeting notes from a rough draft into the established format; reviewed and edited by Khumoyun before commit |
| GitHub Copilot | meeting-notes.md template creation (2026-09-08, Documentation) | Initial meeting notes template structure | n/a | vraygoza: created and committed initial template | n/a |
| Google Antigravity (Claude) | Fix misspelled names across repo documentation (2026-09-19, Documentation) | Replaced all instances of misspelled names (Sophail to Sohail, Khumonyun to Khumoyun) across multiple docs files | n/a | Khumoyun: reviewed diffs across repo and committed changes | Khumoyun: verified replacements across docs files |
| Claude | Draft planning and requirements documentation (README.md, docs/planning/README.md, docs/planning/scope.md, docs/requirements/requirements.md, docs/requirements/open-questions.md) (2026-09-29, Documentation) | Draft documentation based on existing repo contents | n/a | Adiya: reviewed and edited draft before commit | Adiya: reviewed against existing repo contents |
| Google Antigravity (Claude) | Draft deferred scope and tradeoff decisions (docs/decisions/deferred-scope.md) (2026-10-01, Documentation) | Drafted deferred scope and tradeoff decisions from existing scope.md and planning evidence | n/a | Khumoyun: reviewed and edited before commit | Khumoyun: verified against scope.md and planning evidence |
| Claude | Draft traceability matrix, risk register, and tradeoff records (docs/planning/traceability.md, docs/planning/risk-register.md, docs/decisions/tradeoff-records.md) (2026-10-01, Documentation) | Drafted traceability.md, risk-register.md, and tradeoff-records.md from existing planning docs | n/a | Mazen: reviewed and edited draft before commit | Mazen: verified against existing planning docs |
| Claude | Draft architecture README (docs/architecture/README.md) (2026-10-14, Documentation) | Drafted architecture overview based on A3 instructions and A2 feedback | n/a | vraygoza: reviewed and edited before commit | Victoria: verified against A3 instructions and A2 feedback |
| Claude | Architecture package and INV-01 spike (docs/architecture/architecture.md, api-contracts.md, architecture-diagram.dot and .png, investigations/inv-01-lookup-storage.md, technical-recommendations.md; docs/requirements/requirements.md, open-questions.md; spikes/inv-01-lookup-storage/*) (2026-10-14, Documentation, Code Generation, Research) | Drafted architecture docs, API contracts, diagrams, recommendations, and offline spike code/synthetic fixtures | Live USDA FDC API calls (deferred; used synthetic fixtures instead) | Adiya: labeled fixture calorie values as synthetic; reviewed before upload | Adiya: ran offline spike (19 cases, 14 of 14 checks passed); PR #23 reviewed by Sohail and Khumoyun |
| Google Antigravity (Claude) | Format Oct 14 meeting notes (docs/meeting-notes.md) (2026-10-14, Documentation) | Organized rough draft of Oct 14 meeting notes into established format | n/a | Khumoyun: reviewed and edited before commit | Khumoyun: verified against meeting notes draft |
| Claude | Re-estimation and task planning (docs/planning/re-estimation.md, docs/planning/task-plan.md) (2026-10-15, Documentation) | Drafted re-estimation from INV-01 findings and A2 estimates; added architecture tasks T-27 to T-34, verification tasks V-1 to V-6, and proposed owners | n/a | Bazid: reviewed and edited before commit | Reviewed by Victoria and Khumoyun in PR #31 and stacked follow-on PR |
| Claude | Draft updates to architecture README and root README (docs/architecture/README.md, README.md) (2026-10-14, Documentation) | Drafted updates from A3 instructions and A2 feedback | n/a | vraygoza: reviewed and edited before commit | Victoria: checked against A3 instructions and A2 feedback |
| Claude | Draft ADRs 0001-0008, data-context, and update planning docs (docs/decisions/adr-0001 to adr-0008, decision-log.md, tradeoff-records.md; docs/architecture/data-context.md; docs/planning/risk-register.md, traceability.md) (2026-10-15, Documentation) | Drafted ADR-0001 through ADR-0008, data-context.md, and updates to decision log, tradeoff records, risk register, and traceability | n/a | Mazen: reviewed and edited before commit | Mazen: verified against INV-01, architecture docs, and A3 action plan |
| Claude (Opus 5.5) | A1 design check review (docs/reviews/a1-design-check.md) (2026-10-26, Documentation, Code Review) | Comparison of ADR-0001 to 0008, architecture.md, and api-contracts.md with A4 task cards; drafted language choice, interfaces, and Findings 1 to 8 | n/a | Adiya: reviewed and uploaded on 10/28 | Content review by Mazen in PR #64 (issue #47) |
| Claude (Opus 5.5) | Bot skeleton and tests for #48 (src/bot/, src/adapters/telegram.py, requirements.txt, .env.example, src/README.md, tests/test_router.py, tests/test_web.py, tests/test_telegram_adapter.py) (2026-10-26, Code Generation, Testing) | Bot skeleton, webhook router, Telegram adapter, and test cases | python-telegram-bot library (rejected per ADR-0005) | Adiya: reviewed code, prepared branch for upload; confirmed live Telegram bot not yet needed | Claude ran 17 tests and simulated /start webhook check (all passed, wrong secret returned 403); Adiya ran full suite on Mac (Python 3.15.2, 25 tests passed); review by Sohail in PR #69 |
| Claude (Opus 5.5) | Food lookup implementation and tests for #49 (src/core/food_lookup.py, src/core/sample_foods.json, tests/test_food_lookup.py) (2026-10-26, Code Generation, Testing) | Food lookup implementation, synthetic food sample data, and unit tests | Guessing partial matches like egg roll (refused per AC-6.2) | Adiya: labeled calorie values as synthetic; uploaded branch | Claude ran 25 tests (all passed); Adiya ran 25 tests on Mac (Python 3.15.2, OK); review by Sohail in PR #70 |
| Claude (Opus 5) | Reconcile task IDs and criteria (docs/planning/task-id-map.md) (2026-10-29, Documentation) | Reconciliation of conflicting T-27 to T-29 IDs between traceability.md and task-plan.md; added done criteria for privacy, security, and verification tasks | n/a | Bazid: reviewed and edited before commit | PR reviewed by Mazen and Adiya |
| Claude (Opus 5.5) | Restructure AI use log table format and update statistics (docs/ai/ai-use-log.md) (2026-10-31, Documentation) | Reformatted log with six columns: Tool/Model, Task, Accepted output, Rejected output, Human edits, Verification; migrated all historical rows; updated summary statistics | n/a | Khumoyun: reviewed and verified all rows, columns, and statistics before commit | Khumoyun: verified column structure, preserved all historical entries, verified summary counts | PR Reviewed by <placeholder>

## Summary Statistics

- Total AI-assisted sessions: 7
- Most used tool: Claude (6 of 7, including via Google Antigravity)
- Primary use cases: Documentation
- Total AI-assisted sessions: 15
- Most used tool: Claude (13 of 15, including via Google Antigravity and Opus models)
- Primary use cases: Documentation, Code Generation, Testing, Code Review
