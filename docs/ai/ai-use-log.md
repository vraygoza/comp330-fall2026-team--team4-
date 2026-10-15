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
| 2026-10-15 | Claude | docs/decisions/adr-0001 to adr-0008, decision-log.md, tradeoff-records.md; docs/architecture/data-context.md; docs/planning/risk-register.md, traceability.md | Documentation | Mazen | Drafted from INV-01, the architecture docs and Victoria's A3 action plan. Reviewed and edited by Mazen before commit |

Add a new row for every AI-assisted file in Assignment 3, and name who checked it.

## Summary Statistics

- Total AI-assisted sessions: 9
- Most used tool: Claude (8 of 9, including via Google Antigravity)
- Primary use cases: Documentation, Code Generation
