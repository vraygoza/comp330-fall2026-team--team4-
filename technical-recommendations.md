# Cycle 1 Technical Recommendations

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Last updated | 2026-09-29 |
| Status | Proposed, for team decision |

These are recommendations for the open questions assigned to the Architecture & Development Lead in [Open Questions](../requirements/open-questions.md). Nothing here is final until the team agrees. Accepted choices are then recorded in the [Decision Log](decision-log.md) by its owner.

## OQ-3: Language and Bot Library
**Recommendation:** Python with the `python-telegram-bot` library.

- **Why:** Python is readable for a team with mixed coding experience, and the library is widely used with thorough documentation and examples.
- **Tradeoff:** Python is slower than some alternatives, which does not matter at 15 testers.
- **Alternative:** Node.js with a Telegram library such as grammY. Choose this only if most of the team is stronger in JavaScript.

## OQ-2: Nutrition Data Source
**Recommendation:** USDA FoodData Central API.

- **Why:** Free, government maintained, public domain data. A free personal API key allows about 1,000 requests per hour, far more than 15 testers need.
- **Tradeoff:** Nutrients are listed per 100 grams, so "2 eggs" must be converted to grams using the portion data in the food record. A search also returns many matches, so we limit results to the general food datasets (Foundation and SR Legacy) instead of branded products.
- **Security note:** USDA deactivates keys found in public code, so the key lives only in `.env` (see `.gitignore`).
- **Alternative:** Open Food Facts, which is stronger for packaged products than for basic foods like "banana" or "rice."
- **Validation:** Before committing, test 20 common foods against the USDA website by hand (AC-3.2 in [Requirements](../requirements/requirements.md)). If matches are poor, this recommendation is revisited.

## OQ-4: Data Storage
**Recommendation:** SQLite.

- **Why:** One file, no database server, built into Python. Enough for 15 testers.
- **Tradeoff:** Depends on OQ-5 (hosting). If the chosen host erases files on restart, switch to a free hosted database.
- **Data kept:** Telegram user ID, food name, amount, calories, and timestamp only (NFR-4).

## OQ-6: Input Format
**Recommendation:** Accept `<amount> <food>` or `<food>` alone.

| Tester sends | Bot does |
|--------------|----------|
| `2 eggs` | Two of the standard unit |
| `150g rice` | 150 grams |
| `banana` | One standard serving, stated in the reply |
| `a cup of rice` | Asks the tester to rephrase as a number or grams |

- **Why:** Counts and grams cover most meals and keep parsing simple (Risk 3).
- **Tradeoff:** Cups, ounces, and spoons are deferred to a later cycle.

## OQ-7: Time Zone
**Recommendation:** Keep Central time for everyone in Cycle 1, as currently assumed. Per-tester time zones go to the backlog.

## Decisions Needed From the Team
1. Confirm or change each recommendation at the next team meeting.
2. Record accepted choices in the Decision Log.
3. Assign OQ-5 (hosting), since storage depends on it.

## AI Disclosure
Drafted with Claude from the team's requirements and public USDA API documentation; reviewed by Adiya.
