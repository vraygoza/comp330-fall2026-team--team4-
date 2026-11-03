# Assignment 4 Evidence Package: Team 4

Owner: Victoria | Backup: Bazid | Last updated: 2026-11-03
Baseline: tag `a3-architecture-review`. Submission tag: `a4-construction-integration`.

## Purpose
Index of the construction, integration, review, AI-use, CI/CD and test evidence for Assignment 4. The evidence itself lives in the repository; the Word submission points here.

## Deliverables
| Deliverable | Location | Owner | Status |
|---|---|---|---|
| Pull request template | `.github/pull_request_template.md` | Victoria | Merged (#65) |
| CI workflow | `.github/workflows/ci.yml` | Mazen | Merged (#73) |
| CI results evidence | `docs/testing/ci-evidence.md` | Mazen | Not started |
| Source code | `/src/` | Adiya, Bazid, Khumoyun | In progress: skeleton merged (#69), food lookup merged (#70), daily total merged (#83), input parsing merged (#88); integration (Issue #50) PR not yet opened |
| Automated tests | `/tests/` | Adiya, Bazid, Khumoyun | Merged: unit and contract tests (#69, #70, #77, #83, #88) |
| Test cases | `docs/testing/test-cases.md` | Bazid | Merged (#72) |
| Architecture review actions | `docs/reviews/architecture-review.md` | Mazen | Merged (#72) |
| AI code review | `docs/reviews/ai-code-review-01.md` | Khumoyun | Not started |
| Reviewed pull request (integration) | Issue #50 (branch/PR not yet opened) | Adiya (author), Mazen (reviewer) | Not started: unblocked by merges of #83 and #88 |
| Dependency review | `docs/decisions/adr-0009-dependencies.md` | Mazen | Not started |
| Traceability | `docs/planning/traceability.md` | Mazen | Task IDs reconciled and merged (#74); further updates in progress |
| Risk register | `docs/planning/risk-register.md` | Mazen | Not started (#58) |
| Runtime and logging evidence | `docs/testing/runtime-evidence.md` | Khumoyun | Not started |
| Known limitations | `docs/release/known-limitations.md` | Khumoyun | Not started |
| AI-use log | `docs/ai/ai-use-log.md` | Khumoyun | Merged (#82): 22 rows across all contributions in six-column format |
| Changed-file index | `docs/reviews/assignment4-changed-files.md` | Bazid, Khumoyun | Merged (#84): 41 files indexed |
| A1 design check | `docs/reviews/a1-design-check.md` | Adiya | Merged (#64) |
| Architecture update (A5) | `docs/architecture/architecture.md`, Section 11 | Adiya | Merged (#71) |
| Task ID map | `docs/planning/task-id-map.md` | Bazid | Merged (#74) |
| ADR acceptance vote (M1) | `docs/decisions/` (ADR-0001 to ADR-0008) | Mazen | Not started (#56). This was a High finding in the A3 review, so it stays visible here. |
| This evidence package and README section | `docs/reviews/assignment4-review-package.md`, `README.md` | Victoria | Merged (#67, #68) |

Allowed statuses: Not started, In progress, PR open, Merged. Statuses are a snapshot and are re-checked against the Pull requests tab before the Assignment 4 tag. Items shown as PR open are not on `main` yet.

## Workflow story (issue to merge)
To be added after the integration pull request merges: the issue number, branch, pull request, review comments, CI result and merge decision. Until then, see the four traced examples in `docs/reviews/assignment4-changed-files.md` (PR #84).

## Known gaps
`docs/release/known-limitations.md` is not on main yet, so the gaps are listed here. As of 2026-11-03 these are Not started:
- Integration work (Issue #50) wiring router to parser, lookup, and day total; branch/PR not yet opened (now unblocked by #83 and #88 merges)
- Dependency review (adr-0009-dependencies.md)
- Risk register update for construction (#58)
- CI results evidence (docs/testing/ci-evidence.md)
- Runtime and logging evidence (docs/testing/runtime-evidence.md)
- Known-limitations file (docs/release/known-limitations.md)
- AI code review (docs/reviews/ai-code-review-01.md)
- ADR acceptance vote (#56); ADR-0001 to ADR-0008 remain Proposed in repo records
## AI use
Parts of this package were drafted with AI assistance, then reviewed and edited by team members. See `docs/ai/ai-use-log.md`.
