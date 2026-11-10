# Demo Script: Cycle 1 (Team 4)

**Scope:** controlled test with 8 synthetic foods and made-up calorie values. Not a deployed product.

## Setup
1. Python 3.12. Run tests: `python -m unittest discover -s tests -t .` (TODO: confirm test count matches CI on main).
2. Start the bot locally: `python -m src.bot.poll`. Live Telegram and USDA verification are deferred.

## Demo steps
| # | Tester sends | Expected result | Proof |
|---|---|---|---|
| 1 | /start | TODO: copy welcome reply from commit 14e247b | TODO: test file |
| 2 | 2 eggs | TODO: copy calories and day total | TODO: test file |
| 3 | banana | TODO: confirm 1 serving default | TODO: test file |
| 4 | unknownfood | TODO: confirm refusal text, nothing saved | TODO: test file |
| 5 | second tester sends food | TODO: confirm totals are separate per Telegram ID | TODO: test_store.py |

## Not demonstrated (deferred to Cycle 2)
/today, duplicate-update protection, gram amounts, live food database, deployed webhook, live Telegram verification.

## Owner / status
Owner: Victoria. Status: TODO: verify against main.
