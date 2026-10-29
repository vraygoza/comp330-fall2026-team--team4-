# Architecture Package: Team 4 (Calorie Counter Telegram Bot)

Owner: Victoria Raygoza | Backup: Bazid | Last updated: 2026-10-26 | Status: Draft; ADR decisions pending the team vote (#56)

## Purpose
Index to the Cycle 1 architecture and review evidence. The authoritative evidence is in this repository; the Word submission points here.

## Cycle 1 vertical slice
A tester sends one food item to the Telegram bot. The bot looks up its calories, saves the entry under that tester, and returns the day's running total (Chicago time).

## Baselines
Planning baseline: tag `a2-planning-estimate` (commit 4cf90ab). Architecture baseline: tag `a3-architecture-review` (commit 42350c6). Construction baseline: tag `a4-construction-integration` (set at submission).

## Contents
| Document | Owner | Backup | Status |
|---|---|---|---|
| [architecture.md](architecture.md) | Adiya | Mazen | Updated for A4 construction (Section 11) |
| [architecture-diagram.png](architecture-diagram.png) ([source](architecture-diagram.dot)) | Adiya | Khumoyun | Unchanged since A3 |
| Component responsibilities | Khumoyun | Adiya | Kept in [architecture.md, Section 3](architecture.md#3-components); no separate file |
| [api-contracts.md](api-contracts.md) | Adiya | Sohail | Unchanged since A3 except link fixes |
| [data-context.md](data-context.md) | Mazen | Adiya | Unchanged since A3 |
| [INV-01 investigation](investigations/inv-01-lookup-storage.md) | Adiya | Sohail | Unchanged since A3 |
| [ADRs and decision log](../decisions/decision-log.md) | Mazen | Adiya | Proposed; vote in #56 |
| [A1 design check](../reviews/a1-design-check.md) | Adiya | Khumoyun | Construction input to #56 |
| Architecture review action items (`docs/reviews/architecture-review.md`) | Sohail | Bazid | Planned in A4, issue #55 |
| Test strategy (`docs/testing/test-strategy.md`) | Sohail | Mazen | Planned; automated tests live in [/tests](../../tests) |

## Related records
[Requirements](../requirements/requirements.md), [Planning](../planning/README.md), [Decisions](../decisions/decision-log.md), [Source code](../../src/README.md), [AI use log](../ai/ai-use-log.md).

## Open decisions
Pending the team vote (#56): ADR-0001 to ADR-0008 and D3. Pending live checks: nutrition data source (V-1, Adiya with Sohail), hosting and storage (V-2 to V-4, Khumoyun), FDC rate limit and timing (V-5, V-6, Adiya). Privacy notice, deletion and retention: Mazen, Khumoyun.

## AI use
Parts of this package were drafted with AI assistance, then reviewed and edited by team members. See the AI-use log.

## Change Log
| Date | Change | By |
|---|---|---|
| 2026-10-14 | Created | Victoria |
| 2026-10-26 | Moved from `docs/architecture/docs/architecture/` to this location (A3 feedback, Package navigation); fixed links to files that do not exist; added status column | Adiya |
