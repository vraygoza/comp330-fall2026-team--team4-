# ADR-0004: Accepted Message Forms

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |

- **Status:** Proposed (P-5 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). TODO: change to Accepted, with the date, once the team accepts it at the architecture review.
- **Decision owner:** Adiya
- **Closes:** OQ-6, input-form part (the quantity part is [ADR-0003](adr-0003-quantity-to-grams.md))
- **Related:** FR-2 (AC-2.3, AC-2.4), FR-6; T-9, T-10; Risk 13

## Context
Understanding food messages is a High-impact risk (Risk 13), and T-9 can't start until the accepted forms are fixed. One food per message is already decided (TD-1 in [Deferred Scope](deferred-scope.md)). The A2 recommendation was to accept `<amount> <food>` or `<food>` alone; INV-01 kept that and added a few forms and limits.

## Decision
The bot accepts exactly these forms (AC-2.3):

| Form | Example | Read as |
|------|---------|---------|
| `<number> <food>` | `2 eggs`, `1.5 bananas` | A count |
| `<number>g <food>` (also `g`, `gram` or `grams` after a space) | `150g rice cooked` | Grams |
| `a <food>` or `an <food>` | `an egg` | A count of 1 |
| `<food>` alone | `banana` | The default portion, stated in the reply (AC-2.2) |

Limits: counts from 1 to 20 (decimals allowed), grams from 1 to 2000, messages up to 100 characters. Food words use letters, spaces, apostrophes and hyphens only.

Anything else (cups, ounces, fractions such as `1/2 banana`, an amount after the food such as `eggs 2`, or several foods in one message) saves nothing, and the bot replies with the accepted forms and two examples (AC-2.4, outcome `UNSUPPORTED_FORMAT`). An amount outside the limits saves nothing and shows the allowed ranges (outcome `OUT_OF_RANGE`). How each form becomes grams is in [ADR-0003](adr-0003-quantity-to-grams.md). Full reply wording is in [API Contracts](../architecture/api-contracts.md), C-2.

## Alternatives Considered
| Option | Why not chosen |
|--------|----------------|
| Also accept cups, ounces and spoons | Needs a unit-conversion table and more parsing; deferred to a later cycle |
| Accept the amount before or after the food | More parsing cases and more ways to misread a message (Risk 13) |
| Free-form messages read by an AI model | Ruled out in [ADR-0001](adr-0001-no-ai-in-bot.md) |
| Require grams in every message | Most accurate, but harder to use, and contradicts TD-3 |

## Consequences
- **Good:** a small parser with fixed rules lowers Risk 13, and every rejected message gets a clear, predictable reply.
- **Cost:** some real meals ("a bowl of cereal") have to be rephrased by the tester.
- **Cost:** the limits (20 items, 2000 grams) could reject a real but unusual entry. The test week shows how often `OUT_OF_RANGE` happens.

## Evidence and Checks
- **Ran (synthetic data, 2026-10-14):** `a cup of rice`, `eggs 2` and `1/2 banana` were rejected as unsupported; `25 eggs`, `0 eggs` and `3000g rice cooked` were rejected as out of range; none were saved ([spike results](../../spikes/inv-01-lookup-storage/results-2026-10-14.md)).
- **Planned:** a unit test for every accepted and rejected form in the table (contract check C-2 in [API Contracts](../architecture/api-contracts.md)).

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created from P-5 in INV-01 | Mazen |