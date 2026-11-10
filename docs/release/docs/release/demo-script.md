# Demo Script: Cycle 1 (Team 4)

**Scope:** controlled test with 8 synthetic foods and made-up calorie values. Not a deployed product.

## Setup
1. Python 3.12. Run tests: `python -m unittest discover -s tests -t .` (expect {88} tests passing, matching CI).
2. Start the bot locally: `python -m src.bot.poll`. Live Telegram and USDA verification are deferred.

## Demo steps
| # | Tester sends | Expected result | Proof (file/test) |
|---|---|---|---|
| 1 | /start | {welcome reply} | {test file} |
| 2 | 2 tacos | {calories and day total, Chicago day} | {test_log_food.py} |
| 3 | banana | {1 standard serving, total increases} | {test_parser.py} |
| 4 | unknownfood | {refused, nothing saved} | {test file} |
| 5 | second tester sends food | {totals are separate per Telegram ID} | {test_store.py} |

## Not demonstrated (deferred to Cycle 2)
/today, duplicate-update protection, gram amounts, live food database, deployed webhook, live Telegram verification.

## Owner / status
Owner: Victoria. Status: {Draft until verified against main after #90}.
