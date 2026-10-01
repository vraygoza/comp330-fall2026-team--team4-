# Tradeoff Records

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Khumoyun (Operations & Evidence Co-Lead) |
| Last updated | 2026-10-01 |

Tradeoffs the team made while planning Cycle 1: what we chose, what we gave up, and why. Scope tradeoffs (one food per message, Central time, default serving size, free tiers only) are already recorded as TD-1 to TD-4 in [Deferred Scope](deferred-scope.md) and aren't repeated here. General team decisions are in the [Decision Log](decision-log.md).

All records are Proposed until the team confirms them at the next meeting.

## Tradeoff Decisions

| ID | Decision | Alternatives Considered | What We Give Up | Rationale | Status |
|----|----------|-------------------------|-----------------|-----------|--------|
| TR-1 | Commit to Must requirements only; FR-8 and FR-9 are stretch goals | Commit to Must and Should | Testers may not be able to undo a mistake or enter calories by hand | The likely Must-only estimate is 85 hours, about 5 hours per person per week. The high estimate (163 hours) would be about 9, which isn't realistic ([Effort Estimates](../planning/estimates.md)) | Proposed |
| TR-2 | Reject unknown foods instead of guessing | Save the closest match, or save 0 calories | Until FR-9 is built, a food the data source doesn't know can't be logged at all | A wrong number saved without warning ruins the daily total, and the tester can't tell (Risk 4) | Proposed |
| TR-3 | Store only Telegram user ID, food entries, and timestamps | Also store names and usernames | Features that need to know who a tester is, and easier debugging | Food logs are personal data (Risk 6). Storing less means less can leak (NFR-4) | Proposed |

## Pending Tradeoffs
These aren't decided yet. When one is decided, it gets a TR entry and the open question is closed.

| Question | Options | Main Tradeoff | Owner |
|----------|---------|---------------|-------|
| OQ-2 Data source | USDA FoodData Central, Open Food Facts | USDA is stronger for generic foods like "banana"; Open Food Facts is stronger for packaged products. Picking one that also has protein, carbs, and fat avoids switching when macros are added later | Adiya |
| OQ-3 Language and bot library | Not listed yet | A language most of the team already knows lets more people help build (Risk 17) | Adiya |
| OQ-4 and OQ-5 Storage and hosting | SQLite or a hosted database; host not chosen | SQLite is the simplest, but some free hosts erase local files when they restart, so these two need to be decided together | Adiya, TODO |

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-01 | Created tradeoff records | Mazen |
