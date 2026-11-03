# Acceptance Test Cases — Cycle 1 Vertical Slice

| Field | Detail |
|---|---|
| Author | Sohail Shaik (Quality & Review Lead) |
| Date | 2026-10-29 |
| Scope | First integrated food-log path, input boundaries, and data isolation |
| Governing Requirements | C-1 through C-8, ADR-0002, ADR-0003, ADR-0006, ADR-0007 |

---

## Planned Test Matrix

| Case ID | Test Category | Preconditions & Inputs | Expected Saved Database State | Expected Telegram Bot Response |
|---|---|---|---|---|
| TC-01 | First-time `/start` | New user (`telegram_user_id: 1001`). User sends `/start`. | User row created in `users` table with ID `1001` and active status. No food rows. | "Welcome to CalorieBot! Log meals by texting what you ate (e.g., '1 cup oatmeal' or 'banana'). Use /today to check totals." |
| TC-02 | Repeat `/start` | Existing user (`1001`) with previous logs. User sends `/start`. | No duplicate user row created; existing food history unchanged. | Standard welcome back message confirming setup is active. No state reset. |
| TC-03 | Standard Food Log | User `1001` sends `"1 banana"`. FDC returns 105 kcal for 1 medium. | 1 row inserted in `food_logs`: `user_id: 1001`, `food_name: "banana"`, `calories: 105`, local date set to today. | "Logged: 1 medium banana (105 kcal). Today's total: 105 kcal." |
| TC-04 | Missing Amount (Default Serving) | User `1001` sends `"apple"`. No numeric quantity specified. | 1 row inserted in `food_logs`: `user_id: 1001`, `food_name: "apple"`, `calories: 95`, `quantity: 1.0` (default portion). | "Logged: 1 medium apple (default serving: 95 kcal). Today's total: 200 kcal." |
| TC-05 | Negative Case (Unknown Food) | User `1001` sends `"flurbo 200g"`. FDC API returns 0 matches. | Zero rows inserted in `food_logs`. Daily total and history unchanged. | "Could not find nutrition info for 'flurbo'. Please check the spelling or try a simpler name." |
| TC-06 | Empty Daily Total | User `1002` (registered, no meals logged today) sends `/today`. | No database changes. Query executes `SELECT SUM(calories) WHERE user_id = 1002 AND date = CURRENT_DATE`. | "You haven't logged any food today. Text a food item to start your log!" |
| TC-07 | Boundary Case: Chicago Midnight Rollover | User `1001` logs food at 11:59 PM CST, then logs another item at 12:01 AM CST. | First log saved under previous calendar date (`YYYY-MM-DD`). Second log saved under new date. | First log adds to previous day's total. Second log confirms entry and shows reset daily total for the new date. |
| TC-08 | Multi-User Data Isolation | User `1001` logs `"2 eggs"` (140 kcal). User `1002` immediately sends `/today`. | Database contains 1 log tied strictly to `user_id: 1001`. `user_id: 1002` has 0 rows. | User `1002` receives empty total message (0 kcal). No cross-user total leakage. |