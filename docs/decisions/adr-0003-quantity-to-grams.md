# ADR-0003: Converting Amounts to Grams

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |

- **Status:** Proposed (P-4 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). TODO: change to Accepted, with the date, once the team accepts it at the architecture review.
- **Decision owner:** Adiya
- **Closes:** OQ-6, quantity part (the input-form part is [ADR-0004](adr-0004-accepted-input-forms.md))
- **Related:** FR-2 (AC-2.2, AC-2.5, AC-2.6), FR-3 (AC-3.1), FR-6 (AC-6.2); T-10, T-11, T-13; Risks 4 and 19

## Context
FDC lists energy per 100 grams ([ADR-0002](adr-0002-food-data-source-and-matching.md)). Testers send grams ("150g rice cooked"), counts ("2 eggs", "a banana") or no amount ("banana"), as set in [ADR-0004](adr-0004-accepted-input-forms.md). Each has to become grams before calories can be calculated. INV-01 found that many Foundation records have no portion data, and some SR Legacy records list only volume portions such as "1 cup," which cannot turn a count into grams (INV-01 Finding 2).

## Decision
1. **Grams** are used as given.
2. **Counts**, including "a" or "an" (a count of 1), use the food's portion weight: the Curated Food Map portion first, otherwise one FDC portion chosen in a fixed order: medium, then large, then serving.
3. **No amount** uses the same default portion, and the reply says it was assumed (AC-2.2).
4. **No portion weight available:** nothing is saved, and the bot asks for the amount in grams (AC-2.6, outcome `NEEDS_GRAMS`).
5. **Calories** = kcal per 100 g × grams ÷ 100.
6. **Every reply shows the math**, for example "2 x 1 large egg (50 g each) = 100 g" (AC-2.5).
7. **Each saved entry keeps** the quantity, unit (`count`, `g` or `default`), grams, FDC ID and matched description, and the database rejects zero or negative grams or calories ([API Contracts](../architecture/api-contracts.md), C-6).

## Alternatives Considered
| Option | Why not chosen |
|--------|----------------|
| Assume 100 g when no amount is given | Simple, but one egg is not 100 g, and it is not a "standard serving" (AC-2.2) |
| Guess a weight when FDC has no portion | A guessed value, which AC-6.2 and [TR-2](tradeoff-records.md) rule out |
| Require grams in every message | Most accurate, but harder to use, and contradicts TD-3 in [Deferred Scope](deferred-scope.md) |

## Consequences
- **Good:** every saved number traces to an FDC record and a named portion, and the tester sees how it was calculated.
- **Cost:** some foods can only be logged in grams. In the spike, "apple" and "1 rice cooked" asked for grams.
- **Cost:** the Curated Food Map must say which record represents a food as people usually eat it (for example, cooked rice rather than raw).
- **Risk:** real FDC portion data may differ from the synthetic test data (V-1, Risk 4).

## Evidence and Checks
- **Ran (synthetic data, 2026-10-14):** "2 eggs", "egg", "banana", "150g rice cooked", "egg white" and "120g apple" saved with the conversion stated in the reply; "1 rice cooked" and "apple" asked for grams ([spike results](../../spikes/inv-01-lookup-storage/results-2026-10-14.md)).
- **Still needed:** V-1 confirms the real portion fields for the 20 T-13 foods.

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created from P-4 in INV-01 | Mazen |