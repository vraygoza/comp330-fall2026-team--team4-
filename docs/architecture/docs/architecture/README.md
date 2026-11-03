# Architecture Package – Team 4 (Calorie Counter Telegram Bot)

Owner: Victoria Raygoza | Backup: Bazid | Last updated: 2026-10-14 | Status: Draft for review

## Purpose
Index to the Cycle 1 architecture and review evidence. The authoritative evidence is in this repository; the Word submission points here.

## Cycle 1 vertical slice
A tester sends one food item to the Telegram bot. The bot looks up its calories, saves the entry under that tester, and returns the day's running total (Chicago time).

## Baseline under review
Planning baseline: tag `a2-planning-estimate` (commit 4cf90ab). Architecture baseline: tag `a3-architecture-review`.

## Contents
| Document | Owner | Backup |
|---|---|---|
| [architecture.md](architecture.md) | Adiya | Mazen |
| architecture-diagram.png | Adiya | Khumoyun |
| [component-responsibilities.md](component-responsibilities.md) | Khumoyun | Adiya |
| [api-contracts.md](api-contracts.md) | Adiya | Sohail |
| [data-context.md](data-context.md) | Mazen | Adiya |
| [ADRs](../decisions/) | Mazen | Adiya |
| [architecture-review.md](../reviews/architecture-review.md) | Sophail | Bazid |
| [test-strategy.md](../testing/test-strategy.md) | Sophail | Mazen |

## Related records
[Requirements](../requirements/), [Planning](../planning/), [Decisions](../decisions/), [AI use log](../ai/ai-use-log.md).

## Open decisions
Not yet closed, each with an owner: nutrition data source and quantity conversion (Adiya); storage and hosting (Adiya); accepted input forms and Chicago-day boundary (Adiya); privacy notice, deletion and retention (Mazen, Khumoyun).

## AI use
Parts of this package were drafted with AI assistance, then reviewed and edited by team members. See the AI-use log.
