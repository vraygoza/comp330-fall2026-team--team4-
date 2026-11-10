# Assignment 4 Evidence Package: Team 4

Owner: Victoria | Backup: Bazid | Last updated: 2026-11-02
Baseline: tag `a3-architecture-review`. Submission tag: `a4-construction-integration`.

## Purpose
Index of the construction, integration, review, AI-use, CI/CD and test evidence for Assignment 4. The evidence itself lives in the repository; the Word submission points here.

## Deliverables
| Deliverable | Location | Owner | Status |
|---|---|---|---|
| Pull request template | `.github/pull_request_template.md` | Victoria | Merged (#65) |
| CI workflow | `.github/workflows/ci.yml` | Mazen | PR open, approved, check passing (#73) |
| CI results evidence | `docs/testing/ci-evidence.md` | Mazen | Not started |
| Source code | `/src/` | Adiya, Bazid, Khumoyun | In progress: skeleton merged (#69), food lookup merged (#70), daily total approved (#83); input parsing not started (#61) |
| Automated tests | `/tests/` | Adiya | Merged (#69, #70); contract tests in PR #77 (open) |
| Test cases | `docs/testing/test-cases.md` (PR #72, not on main yet) | Bazid | PR open (#72); unowned until reassigned |
| Architecture review actions | `docs/reviews/architecture-review.md` (PR #72, not on main yet) | Mazen | PR open (#72); unowned until reassigned |
| AI code review | `docs/reviews/ai-code-review-01.md` | Khumoyun | Not started |
| Reviewed pull request (integration) | Not yet opened (#50) | Adiya (author), Mazen (reviewer) | Not started |
| Dependency review | `docs/decisions/adr-0009-dependencies.md` | Mazen | Not started |
| Traceability | `docs/planning/traceability.md` | Mazen | Task IDs reconciled and merged (#74); further updates in progress |
| Risk register | `docs/planning/risk-register.md` | Mazen | Not started |
| Runtime and logging evidence | `docs/testing/runtime-evidence.md` | Khumoyun | In progress |
| Known limitations | `docs/release/known-limitations.md` | Khumoyun | Not started |
| AI-use log | `docs/ai/ai-use-log.md` | Khumoyun | In progress: log exists with rows from every member; format update in PR #82 |
| Changed-file index | `docs/reviews/assignment4-changed-files.md` | Bazid | PR open (#84) |
| A1 design check | `docs/reviews/a1-design-check.md` | Adiya | Merged (#64) |
| Architecture update (A5) | `docs/architecture/architecture.md`, Section 11 | Adiya | PR open, approved, waiting on the integration PR (#71) |
| Task ID map | `docs/planning/task-id-map.md` | Bazid | Merged (#74) |
| ADR acceptance vote (M1) | `docs/decisions/` (ADR-0001 to ADR-0008) | Mazen | Not started (#56). This was a High finding in the A3 review, so it stays visible here. |
| This evidence package and README section | `docs/reviews/assignment4-review-package.md`, `README.md` | Victoria | PR open (#67, #68) |

Allowed statuses: Not started, In progress, PR open, Merged. Statuses are a snapshot and are re-checked against the Pull requests tab before the Assignment 4 tag. Items shown as PR open are not on `main` yet.

## Workflow story (issue to merge)
To be added after the integration pull request merges: the issue number, branch, pull request, review comments, CI result and merge decision. Until then, see the three traced examples in `docs/reviews/assignment4-changed-files.md` (PR #84).

## Known gaps
`docs/release/known-limitations.md` is not on main yet, so the gaps are listed here. As of 2026-11-02 these are Not started:
- Integration pull request (#50); input parsing (#61) is not merged
- Dependency review (adr-0009-dependencies.md)
- Risk register update for construction
- CI results evidence
- Runtime and logging evidence
- Known-limitations file
- AI code review (ai-code-review-01.md)
- ADR acceptance vote (#56); ADR-0001 to ADR-0008 remain Proposed
Items shown as PR open are not on main.
## AI use
Parts of this package were drafted with AI assistance, then reviewed and edited by team members. See `docs/ai/ai-use-log.md`.
