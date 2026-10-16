# Requirement-to-Task Traceability

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Khumoyun (Operations & Evidence Co-Lead) |
| Last updated | 2026-10-15 |

This maps each Cycle 1 requirement to the tasks that deliver it, the estimated hours, the owner, related risks, and how it will be tested. Requirements come from [Requirements](../requirements/requirements.md), tasks and owners from the [Task Plan](taskplan.md), hours from [Effort Estimates](estimates.md), and risk numbers from the [Risk Register](risk-register.md).

Issue numbers will be added once the GitHub Issues are created. Each Issue title should start with its task ID (for example, `T-9: Parse food and amount`).

## Traceability Matrix

| Requirement | Priority | Tasks | Likely hours | Owner | Risks | Verified by | Issue |
|-------------|----------|-------|--------------|-------|-------|-------------|-------|
| FR-1 Start the bot | Must | T-5, T-7, T-8 | 7 | TODO | 12, 18 | T-22 | TODO |
| FR-2 Log a food item | Must | T-9, T-10, T-12 | 14 | TODO | 12, 13 | T-22 | TODO |
| FR-3 Look up calories | Must | T-1, T-11, T-13 | 13 | Adiya, Sohail, TODO | 4, 5, 19 | T-13, T-22 | TODO |
| FR-4 Running total | Must | T-14 | 3 | TODO | 4 | T-22 | TODO |
| FR-5 View today's log | Must | T-15, T-16, T-17 | 8 | TODO | 20 | T-22 | TODO |
| FR-6 Unknown foods | Must | T-18 | 3 | TODO | 4, 13, 19 | T-22 | TODO |
| FR-7 Separate data per tester | Must | T-19 | 4 | TODO | 6 | T-22 | TODO |
| FR-8 Undo last entry | Should | T-20 | 3 | TODO | 3 | Gap G-3 | TODO |
| FR-9 Manual calories | Should | T-21 | 4 | TODO | 3 | Gap G-3 | TODO |
| FR-10 Tester access | Must (proposed) | T-6, T-25, T-29 | 8 + T-29 | Adiya (T-6), Mazen (T-25), TODO (T-29) | 6, 14, 15 | AC-10.1 to AC-10.3; 3 outside testers log meals | TODO |
| NFR-1 Reply within 5 seconds | Not stated | T-23 | 2 | Sohail | 14, 18 | T-23 | TODO |
| NFR-2 Supports 15 testers | Not stated | T-24 | 4 | TODO | 14, 15 | T-24 | TODO |
| NFR-3 No secrets in repo | Must | T-4, T-26 | 4 | TODO, Sohail | 6 | T-26 | TODO |
| NFR-4 Store only what is needed | Not stated | T-3 | — | Adiya | 6 | T-27 data-model review (proposed) | TODO |
| NFR-5 Free tiers only | Not stated | T-1 | — | Adiya | 5 | T-28 weekly usage check (proposed) | TODO |

Tasks shared by several requirements are counted once: T-2 (2 hours) and T-3 (5 hours), owned by Adiya, and T-22 acceptance tests (8 hours), owned by Sohail. T-6 hosting (5 hours) and T-25 tester onboarding notice (3 hours, Mazen) now trace to FR-10. The total is still 92 likely hours, which matches [Effort Estimates](estimates.md); the proposed tasks T-27 to T-29 are not estimated yet.

Every acceptance criterion (AC-1.1 through AC-9.1) is covered by at least one task. The proposed criteria added on 2026-10-14 are covered too: AC-2.3 and AC-2.4 by T-9, AC-2.5 and AC-2.6 by T-10 and T-11, AC-6.3 and AC-6.4 by T-11 and T-18, and AC-10.1 to AC-10.3 by T-25 and T-29.

## Proposed New Tasks
For Bazid to add to the [Task Plan](taskplan.md) with estimates.

| ID | Task | Traces to | Proposed owner |
|----|------|-----------|----------------|
| T-27 | Review the database tables against NFR-4 before the Entry Store merges: only the fields listed in [Data and Context](../architecture/data-context.md) are stored | NFR-4 | Mazen |
| T-28 | Weekly health check: outcome counts, reply times and FDC calls per hour against free-tier limits | NFR-5, Risk 5 | Adiya |
| T-29 | Build the tester invite check and the `/privacy` reply | FR-10 (AC-10.1 to AC-10.3) | TODO |

## Design Decisions Behind Each Requirement
ADRs are listed under D4 in the [Decision Log](../decisions/decision-log.md). All are proposed until the architecture review.

| Requirement | Decided in |
|-------------|------------|
| FR-1 Start the bot | ADR-0005, ADR-0006 |
| FR-2 Log a food item | ADR-0003, ADR-0004 |
| FR-3 Look up calories | ADR-0002, ADR-0003 |
| FR-4 Running total | ADR-0007 |
| FR-5 View today's log | ADR-0007 |
| FR-6 Unknown foods | ADR-0002, ADR-0003, ADR-0004 |
| FR-7 Separate data per tester | ADR-0006; [Data and Context](../architecture/data-context.md) |
| FR-8, FR-9 (Should) | Not designed yet |
| FR-10 Tester access | ADR-0006; Data and Context |
| NFR-1 Reply within 5 seconds | ADR-0002, ADR-0005, ADR-0006, ADR-0008 |
| NFR-2 Supports 15 testers | ADR-0006, ADR-0008 |
| NFR-3 No secrets in repo | ADR-0002, ADR-0005, ADR-0006; Data and Context |
| NFR-4 Store only what is needed | ADR-0006; Data and Context |
| NFR-5 Free tiers only | ADR-0002, ADR-0006 |
| AI boundary questions (A3 Section 6) | ADR-0001 |

## Gaps Found

| # | Gap | Fix | Status |
|---|-----|-----|--------|
| G-1 | T-6 and T-25 (hosting and the tester notice) didn't trace to any requirement, even though the Definition of Done needs 3 outside testers | FR-10 (tester access, proposed by Adiya) now covers them | Closed once FR-10 is accepted |
| G-2 | NFR-4 and NFR-5 do map to tasks (T-3 and T-1), but nothing checked them. The A2 version wrongly said they had no task or owner | Proposed T-27 (data-model review) and T-28 (weekly usage check) | Open until T-27 and T-28 are in the Task Plan |
| G-3 | FR-8 and FR-9 have no test task, because T-22 only covers Must requirements | Extend T-22 if either one gets built | Open |
| G-4 | 18 of 26 tasks have no owner | Assign owners when the Issues are created | Open |

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-01 | Created Cycle 1 traceability matrix | Mazen |
| 2026-10-15 | A2 review fixes: corrected G-2, added FR-10 row (closes G-1), proposed T-27 to T-29. A3: added a table linking each requirement to ADR-0001 to ADR-0008 | Mazen |
