# ADR-0002: USDA FoodData Central with a Curated Food Map and Strict Matching

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |

- **Status:** Proposed (P-2 and P-3 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). TODO: change to Accepted, with the date, once the team accepts it at the architecture review.
- **Decision owner:** Adiya
- **Closes:** OQ-2
- **Related:** FR-3, FR-6, NFR-1, NFR-3, NFR-5; T-1, T-11, T-13; Risks 4, 5 and 19

## Context
Every calorie number the bot saves comes from this source, and AC-3.1 says the saved value must match it. INV-01 found that a successful search is not a correct match: generic words hit several records with very different calories ("rice" raw versus cooked, "egg" whole versus white). Taking the first result would save wrong totals without warning, which AC-6.2 and [TR-2](tradeoff-records.md) rule out.

## Decision
1. **Source:** the USDA FoodData Central (FDC) API, **Foundation** and **SR Legacy** data only. Branded and Survey data are excluded in Cycle 1.
2. **Curated Food Map first:** the foods hand-checked in T-13 become a reviewed map from tester words to one FDC record and one default portion. The resolver checks the map before searching.
3. **Strict search fallback (P-3):** every query word must appear in the record description, and the record's first word must be one of the query words. If the top matched records differ by more than 25% in kcal per 100 g, the message is **ambiguous**: nothing is saved, and the bot lists up to 3 options (AC-6.3).
4. **Energy value:** use nutrient 1008, else Atwater 2047, else 2048. If none exists, nothing is saved.
5. **Failures:** a 3-second timeout. A timeout, rate limit (HTTP 429) or error saves nothing and asks the tester to try again (AC-6.4).
6. **Secrets and credit:** the API key lives only in the host environment and developers' `.env`, never in the repo (NFR-3). USDA FoodData Central is credited as the data source (CC0 data).
7. **Changes to the map** need a reviewed PR with T-13 evidence (checkpoint G-2 in [Architecture](../architecture/architecture.md)).

Full call details are in [API Contracts](../architecture/api-contracts.md), C-4, C-5 and C-7.

## Alternatives Considered
| Option | Why not chosen |
|--------|----------------|
| Take the top search result | Simplest, but saves wrong values silently (INV-01 Finding 1) |
| Ask the tester to pick from a numbered list | Needs a two-step conversation with saved state; more scope than Cycle 1 |
| Open Food Facts | Stronger for packaged products, weaker for generic foods like "banana" or "rice" |

## Consequences
- **Good:** common foods are checked by a person; anything uncertain is refused with a clear reason instead of guessed.
- **Cost:** the map needs upkeep through reviewed PRs, and T-11 and T-13 grow (see INV-01, "Effect on Estimates").
- **Risk:** the 25% rule may refuse too many real messages. The test week counts `AMBIGUOUS` outcomes; if more than about 1 in 5 messages are refused, P-3 is revisited (Risk 19).
- **Risk:** FDC's limit is 1,000 requests per hour, stated per IP address. On a shared host, other users could use up our quota. The map and a food cache reduce our calls (Risk 5).

## Evidence and Checks
- **Ran (synthetic data, 2026-10-14):** an ambiguous "150g rice", two unknown foods, a record with no energy value and a simulated lookup timeout all saved nothing, and a record with only Atwater energy (2047) still gave a calorie value ([spike results](../../spikes/inv-01-lookup-storage/results-2026-10-14.md)).
- **Still needed:** V-1 (live FDC run of the 20 T-13 foods), V-5 (rate-limit headers from the host) and V-6 (FDC response time from the host), all listed in INV-01.

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created from P-2 and P-3 in INV-01 | Mazen |