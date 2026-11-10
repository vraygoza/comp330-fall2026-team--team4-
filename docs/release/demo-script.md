# Demo Script: Cycle 1 (Team 4)

**Scope:** controlled test with 8 synthetic foods and made-up calorie values. Not a deployed product.

## Setup
1. Python 3.12. Run tests: `python -m unittest discover -s tests -t .` (88 tests pass on main, same as CI).
2. Start the bot locally with a test bot token in `.env`: `python -m src.bot.poll`. Live Telegram verification, the deployed webhook and the USDA lookup are deferred.

## Demo steps
| # | Tester sends | Expected reply | Proof |
|---|---|---|---|
| 1 | /start | Welcome to the Team 4 calorie tracker test. Send one food per message, for example: 2 eggs | tests/test_log_food.py: test_start_registers_and_welcomes |
| 2 | 2 eggs | Logged 2 x Egg (1 large egg each) = 140 kcal. Today's total: 140 kcal. | tests/test_log_food.py: test_logs_food_and_replies_with_total |
| 3 | banana | Logged 1 x Banana (1 medium banana, assumed because no amount was given) = 105 kcal. Today's total: 245 kcal. | tests/test_log_food.py: test_no_amount_assumes_one_serving_and_says_so |
| 4 | unknownfood | I don't know "unknownfood" yet, so nothing was saved. Try another food, like: banana | tests/test_log_food.py: test_unknown_food_saves_nothing |
| 5 | Second tester sends /start, then "an egg" | Logged 1 x Egg (1 large egg each) = 70 kcal. Today's total: 70 kcal. (only their own food) | tests/test_log_food.py: test_two_testers_have_separate_totals; tests/test_store.py: test_tester_a_never_sees_tester_b |

## Not demonstrated (deferred to Cycle 2)
/today, duplicate-update protection, gram amounts, live food database (USDA), deployed webhook, live Telegram verification.

## Owner / status
Owner: Victoria. Status: replies copied from a run on main by Mazen on 2026-11-09 and matched to the test names above.
