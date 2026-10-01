# Requirement-to-Task Traceability

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Khumoyun (Operations & Evidence Co-Lead) |
| Last updated | 2026-10-01 |

This maps each Cycle 1 requirement to the tasks that deliver it, the estimated hours, the owner, related risks, and how it will be tested. Requirements come from [Requirements](../requirements/requirements.md), tasks and owners from the [Task Plan](taskplan.md), hours from [Effort Estimates](estimates.md), and risk numbers from the [Risk Register](risk-register.md).

Issue numbers will be added once the GitHub Issues are created. Each Issue title should start with its task ID (for example, `T-9: Parse food and amount`).

## Traceability Matrix

| Requirement | Priority | Tasks | Likely hours | Owner | Risks | Verified by | Issue |
|-------------|----------|-------|--------------|-------|-------|-------------|-------|
| FR-1 Start the bot | Must | T-5, T-7, T-8 | 7 | TODO | 12 | T-22 | TODO |
| FR-2 Log a food item | Must | T-9, T-10, T-12 | 14 | TODO | 12, 13 | T-22 | TODO |
| FR-3 Look up calories | Must | T-1, T-11, T-13 | 13 | Adiya, Sohail, TODO | 4, 5 | T-13, T-22 | TODO |
| FR-4 Running total | Must | T-14 | 3 | TODO | 4 | T-22 | TODO |
| FR-5 View today's log | Must | T-15, T-16, T-17 | 8 | TODO | — | T-22 | TODO |
| FR-6 Unknown foods | Must | T-18 | 3 | TODO | 4, 13 | T-22 | TODO |
| FR-7 Separate data per tester | Must | T-19 | 4 | TODO | 6 | T-22 | TODO |
| FR-8 Undo last entry | Should | T-20 | 3 | TODO | 3 | Gap G-3 | TODO |
| FR-9 Manual calories | Should | T-21 | 4 | TODO | 3 | Gap G-3 | TODO |
| NFR-1 Reply within 5 seconds | Not stated | T-23 | 2 | Sohail | 14 | T-23 | TODO |
| NFR-2 Supports 15 testers | Not stated | T-24 | 4 | TODO | 14, 15 | T-24 | TODO |
| NFR-3 No secrets in repo | Must | T-4, T-26 | 4 | TODO, Sohail | 6 | T-26 | TODO |
| NFR-4 Store only what is needed | Not stated | T-3 | — | Adiya | 6 | Gap G-2 | TODO |
| NFR-5 Free tiers only | Not stated | T-1 | — | Adiya | 5 | Gap G-2 | TODO |

Tasks shared by several requirements are counted once: T-2 (2 hours) and T-3 (5 hours), owned by Adiya, and T-22 acceptance tests (8 hours), owned by Sohail. T-6 hosting (5 hours) and T-25 tester onboarding notice (3 hours, Mazen) don't trace to any requirement (see G-1). With these included, the total is 92 likely hours, which matches [Effort Estimates](estimates.md).

Every acceptance criterion (AC-1.1 through AC-9.1) is covered by at least one task.

## Gaps Found

| # | Gap | Proposed fix |
|---|-----|--------------|
| G-1 | T-6 and T-25 (tester onboarding) don't trace to a requirement, even though the Definition of Done needs 3 outside testers | Add a requirement for tester access to [Requirements](../requirements/requirements.md) |
| G-2 | NFR-4 and NFR-5 have no task or owner | Add a data-model review for NFR-4 and a weekly usage check for NFR-5 to the Task Plan |
| G-3 | FR-8 and FR-9 have no test task, because T-22 only covers Must requirements | Extend T-22 if either one gets built |
| G-4 | 18 of 26 tasks have no owner | Assign owners when the Issues are created |

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-01 | Created Cycle 1 traceability matrix | Mazen |
