# Tradeoff Records

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Khumoyun (Operations & Evidence Co-Lead) |
| Last updated | 2026-10-15 |

Tradeoffs the team made while planning Cycle 1: what we chose, what we gave up, and why. Scope tradeoffs (one food per message, Central time, default serving size, free tiers only) are already recorded as TD-1 to TD-4 in [Deferred Scope](deferred-scope.md) and aren't repeated here. General team decisions are in the [Decision Log](decision-log.md).

All records are Proposed until the team confirms them at the next review. The Status column says which decision each one is confirmed with.

## Tradeoff Decisions

| ID | Decision | Alternatives Considered | What We Give Up | Rationale | Status |
|----|----------|-------------------------|-----------------|-----------|--------|
| TR-1 | Commit to Must requirements only; FR-8 and FR-9 are stretch goals | Commit to Must and Should | Testers may not be able to undo a mistake or enter calories by hand | The likely Must-only estimate is 85 hours, about 5 hours per person per week. The high estimate (163 hours) would be about 9, which isn't realistic ([Effort Estimates](../planning/estimates.md)) | Proposed; confirmed with D3 in the [Decision Log](decision-log.md) |
| TR-2 | Reject unknown foods instead of guessing | Save the closest match, or save 0 calories | Until FR-9 is built, a food the data source doesn't know can't be logged at all | A wrong number saved without warning ruins the daily total, and the tester can't tell (Risk 4) | Proposed; applied in [ADR-0002](adr-0002-food-data-source-and-matching.md) and [ADR-0003](adr-0003-quantity-to-grams.md) |
| TR-3 | Store only Telegram user ID, food entries, and timestamps | Also store names and usernames | Features that need to know who a tester is, and easier debugging | Food logs are personal data (Risk 6). Storing less means less can leak (NFR-4) | Proposed; applied in [Data and Context](../architecture/data-context.md) |

## Former Pending Tradeoffs
These were open on 2026-10-01. Each now has an ADR with its alternatives, consequences and risks. The evidence is in [INV-01](../architecture/investigations/inv-01-lookup-storage.md).

| Question | Tradeoff | Now recorded in |
|----------|----------|-----------------|
| OQ-2 Data source | USDA is stronger for generic foods. Taking the first search result was rejected because it saves wrong values, so a curated food map and a 25% ambiguity rule were chosen instead | [ADR-0002](adr-0002-food-data-source-and-matching.md) |
| OQ-3 Language and bot library | `python-telegram-bot` (the A2 recommendation) fits a long-running process; a Flask webhook fits our likely free host better | [ADR-0005](adr-0005-python-flask-webhook.md) |
| OQ-4 and OQ-5 Storage and hosting | SQLite is the simplest, but only safe on a host whose disk survives restarts; Render free erases files | [ADR-0006](adr-0006-hosting-and-storage.md) |
| OQ-6 Input format and amounts | Fewer accepted forms mean fewer parsing errors but more rephrasing by testers | [ADR-0003](adr-0003-quantity-to-grams.md) and [ADR-0004](adr-0004-accepted-input-forms.md) |
| OQ-7 Time zone | One Chicago day for everyone is simple and correct on daylight-saving days; per-tester time zones are deferred | [ADR-0007](adr-0007-chicago-day.md) |

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-01 | Created tradeoff records | Mazen |
| 2026-10-15 | Linked TR-1 to TR-3 to the decisions they apply to; moved pending tradeoffs to ADR-0002 to ADR-0007 | Mazen |
