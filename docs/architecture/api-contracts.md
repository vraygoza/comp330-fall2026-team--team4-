# API and Tool Boundary Contracts

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Sohail (Quality & Review Lead) |
| Last updated | 2026-10-14 |
| Status | Draft for architecture review. External facts checked 2026-10-14; FDC field names pending live check V-1 |

Every boundary the bot crosses, with inputs, outputs, errors, permissions, limits and what each call is allowed to change. Components are defined in [Architecture](architecture.md). Proposed decisions (P-1 to P-10) are explained in [INV-01](investigations/inv-01-lookup-storage.md). Planned tests for each contract are listed at the end for the [Test Strategy](../testing/test-strategy.md).

| ID | Contract | Direction | Kind |
|----|----------|-----------|------|
| C-1 | Telegram webhook (Update in) | Telegram to bot | External, inbound |
| C-2 | Tester conversation (commands and replies) | Tester to bot | User-facing |
| C-3 | Telegram Bot API calls | Bot to Telegram | External, outbound |
| C-4 | FDC food search | Bot to FDC | External, outbound, read-only |
| C-5 | FDC food details | Bot to FDC | External, outbound, read-only |
| C-6 | Entry Store | Core to storage | Internal port |
| C-7 | Food Resolver | Core | Internal port |
| C-8 | Outcome codes | All | Shared vocabulary |

## C-1: Telegram Webhook

**Endpoint:** `POST https://<host>/telegram/webhook` on port 443. Registered with `setWebhook` (C-3).

**Authentication:** header `X-Telegram-Bot-Api-Secret-Token` must equal `TELEGRAM_WEBHOOK_SECRET`. Telegram sends this header on every webhook request when the secret is set ([Bot API](https://core.telegram.org/bots/api#setwebhook)).

**Input fields read** (everything else in the Update is ignored and never stored):

| Field | Type | Use |
|-------|------|-----|
| `update_id` | integer | Duplicate check |
| `message.chat.id` | integer | Where to reply |
| `message.chat.type` | string | Must be `private` |
| `message.from.id` | integer | Telegram user ID: the tester's identity |
| `message.text` | string, optional | The command or food |
| `message.date` | Unix time | Not used for the entry time; the server clock is (see C-6) |

Never read: `first_name`, `last_name`, `username`, `language_code`, contacts, photos, location.

**Responses:**

| Condition | HTTP | Side effect |
|-----------|------|-------------|
| Secret missing or wrong | 403 | None; log `AUTH_REJECTED` |
| Body is not JSON or has no `update_id` | 400 | None; log `BAD_UPDATE` |
| `update_id` already processed | 200 | None; log `DUPLICATE` |
| No `message` (edited message, channel post, other) | 200 | None |
| Chat is not private | 200 | One reply: "Please message me directly." |
| Message has no text (photo, sticker, voice) | 200 | Reply with the format hint (C-2) |
| Text handled (logged or refused) | 200 | Per C-2; `update_id` recorded |
| Unexpected exception | 500 | Nothing saved; Telegram retries; log `INTERNAL_ERROR` |

Rules:

- The handler finishes within 5 seconds (NFR-1, P-9). FDC timeout is 3 seconds so a failed lookup still answers in time.
- Saving an entry and recording its `update_id` happen in one transaction, so a retry after a crash cannot create a second entry.
- `update_id` values are kept 48 hours, then deleted. Telegram keeps undelivered updates at most 24 hours.

## C-2: Tester Conversation

This is the contract testers experience. Replies below are the intended wording; exact text can change in review as long as the meaning holds.

| Input | Preconditions | Bot does | Saves | Reply |
|-------|---------------|----------|-------|-------|
| `/start` (new tester) | Valid invite if FR-10 is accepted | Creates user row | `users` row | Welcome, one example, link to `/privacy` (AC-1.1) |
| `/start` (existing tester) | None | Nothing new | Nothing | Same welcome; entries kept (AC-1.2) |
| `/start` without valid invite (FR-10) | FR-10 accepted | Nothing | Nothing | "This bot is in a closed test." |
| `/privacy` | None | Nothing | Nothing | What is stored, why, how long, how to ask for deletion (OQ-8 text) |
| `/today` | Registered | Reads today's entries | Nothing | List and total (AC-5.1) or "Nothing logged yet today." (AC-5.2) |
| `<number> <food>` | Registered | Count rule (P-4) | Entry if `LOGGED` | Item, grams used, kcal, today's total (AC-4.1) |
| `<number>g <food>` (also `g`, `gram`, `grams` with a space) | Registered | Grams as given | Entry if `LOGGED` | Same |
| `a <food>` or `an <food>` | Registered | Count of 1 | Entry if `LOGGED` | Same |
| `<food>` | Registered | Default portion; reply says it was assumed (AC-2.2) | Entry if `LOGGED` | Same, with "assumed because no amount was given" |
| Anything else (units like cup or oz, fractions, amount after the food, several foods, unknown commands) | Any | Nothing | Nothing | Format hint (`UNSUPPORTED_FORMAT`) |
| `/undo` (Should, FR-8) | Registered, entry today | Deletes the latest entry | Deletes one row | Removed item and new total |
| Any text from an unregistered user | Not registered | Nothing | Nothing | "Send /start first." |

Input limits (P-5): text up to 100 characters; count from 1 to 20 (decimals allowed, such as `1.5`); grams from 1 to 2000; food words use letters, spaces, apostrophes and hyphens only. One food per message (TD-1).

## C-3: Telegram Bot API Calls

Base: `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/`. Called only by the Telegram Adapter.

| Method | When | Parameters we send | Success | Errors and handling |
|--------|------|--------------------|---------|---------------------|
| `sendMessage` | Once per handled message | `chat_id`, `text` (plain, no parse mode) | `ok: true` | Network error or `ok: false`: log `REPLY_FAILED` with the error code. The entry stays saved; the tester can check with `/today`. No retry loop |
| `setWebhook` | At deploy only, by the deployer (G-3) | `url`, `secret_token`, `allowed_updates=["message"]`, `drop_pending_updates=false` | `ok: true` | Deploy smoke test fails; deployer fixes before testers are told |

Limits: about 1 message per second per chat and about 30 per second overall ([Bot FAQ](https://core.telegram.org/bots/faq)). We send one reply per tester message, so this is not reached at 15 testers. `/today` caps the list at 50 lines to stay under the message length limit.

Permissions: the token can act as the bot in any chat that messaged it. It is held only in the host environment and developers' `.env`. If it leaks: revoke in BotFather, install the new token, rerun `setWebhook` (G-6, Risk 6).

## C-4: FDC Food Search

`GET https://api.nal.usda.gov/fdc/v1/foods/search` ([FDC API Guide](https://fdc.nal.usda.gov/api-guide)). Called only by the FDC Adapter.

| Parameter | Value |
|-----------|-------|
| `api_key` | `FDC_API_KEY` from the environment |
| `query` | The parsed food words only. Never a Telegram ID or any other tester data |
| `dataType` | `Foundation`, `SR Legacy` (P-2). Branded and Survey data are excluded in Cycle 1 |
| `pageSize` | 5 |

**Fields used from each result** (to confirm in V-1): `fdcId`, `description`, `dataType`, `foodNutrients[].nutrientId`, `foodNutrients[].value`, `foodNutrients[].unitName`, and portion data (`foodMeasures` in search results is expected; the spike assumed `foodPortions`).

**Energy rule:** use nutrient 1008 (Energy, kcal); if absent, 2047; if absent, 2048. Unit must be kcal. If none, outcome `NO_ENERGY_VALUE`.

**Matching rule (P-3):** a result matches only if every query word (singular form) appears in its description and the description's first word is one of the query words. If the top matched results (up to 3) differ by more than 25% in kcal per 100 g, the outcome is `AMBIGUOUS`. If nothing matches, `NOT_FOUND`. Neither saves anything.

| FDC response | Outcome | Logged as |
|--------------|---------|-----------|
| 200 with a reliable match | Continue to grams | `FDC_OK` |
| 200 with no match or ambiguity | `NOT_FOUND` or `AMBIGUOUS` | `FDC_OK` |
| 429 Too Many Requests | `LOOKUP_FAILED` | `FDC_RATE_LIMITED` (key blocked for 1 hour) |
| 403 or 401 | `LOOKUP_FAILED` | `FDC_KEY_REJECTED`: alert the team, key may be deactivated |
| 5xx, timeout over 3 seconds, network error | `LOOKUP_FAILED` | `FDC_UNAVAILABLE` |

Limits: 1,000 requests per hour; going over blocks the key for 1 hour. The guide states the limit per IP address, which may be shared on our host (Finding 8, check V-5). Target: under 200 calls per hour, helped by the cache and the curated map. Never use `DEMO_KEY` (30 per hour) outside local exploration.

Change: none. FDC is read-only. Credit "USDA FoodData Central" in `/privacy` and the README as the data source.

## C-5: FDC Food Details

`GET https://api.nal.usda.gov/fdc/v1/food/{fdcId}?api_key=...`

Used for Curated Food Map entries, which already name the `fdcId`. Same energy rule, errors and limits as C-4. The response's `foodPortions` (amount, modifier, `gramWeight`) is used only to confirm the map's portion during T-13; at run time the map's portion wins.

**Cache:** each fetched record's `fdcId`, description, kcal per 100 g, energy nutrient ID and portions go in `food_cache` with the fetch time. Cache entries are refreshed when the food map changes or after 30 days. The cache holds no tester data.

## C-6: Entry Store (internal port)

The only code that touches the database. Every method that reads or writes tester data takes `telegram_user_id`, and there is no method that lists all users' entries.

| Method | Input | Output | Errors |
|--------|-------|--------|--------|
| `ensure_user(user_id, now_utc)` | Telegram user ID, server time | `True` if created, `False` if it existed | Database error |
| `is_registered(user_id)` | User ID | Boolean | Database error |
| `add_entry(user_id, entry, update_id, now_utc)` | Entry fields below, the Update ID | New entry ID | `DuplicateUpdate` if `update_id` exists (nothing saved); constraint error if kcal or grams are not positive |
| `entries_for_day(user_id, chicago_date)` | User ID, a Chicago date | Ordered list of entries | Database error |
| `total_for_day(user_id, chicago_date)` | User ID, a Chicago date | kcal total, 0 if none | Database error |
| `delete_last_entry_today(user_id, now_utc)` (Should) | User ID | Deleted entry or none | Database error |
| `delete_user(user_id)` (G-5 script only) | User ID | Rows removed | Database error |

**Tables (NFR-4: nothing else is stored):**

| Table | Columns |
|-------|---------|
| `users` | `telegram_user_id` (primary key), `created_at_utc` |
| `entries` | `id`, `telegram_user_id`, `food_text` (the tester's food words), `fdc_id`, `matched_description`, `quantity`, `unit` (`count`, `g`, `default`), `grams` (> 0), `kcal` (> 0), `source` (`fdc`, or `manual` if FR-9 is built), `logged_at_utc` |
| `food_cache` | `fdc_id`, `description`, `kcal_per_100g`, `energy_nutrient_id`, `portions_json`, `retrieved_at_utc` (no tester data) |
| `processed_updates` | `update_id`, `processed_at_utc` (deleted after 48 hours) |

Time rule (P-8): `logged_at_utc` is the server clock in UTC when the entry is saved. A day query uses the Day Calculator window `[Chicago midnight, next Chicago midnight)` converted to UTC, which is 23 or 25 hours on daylight-saving days. Tested in the spike.

## C-7: Food Resolver (internal port)

`resolve(parsed) -> Resolution`

| Input | Output on success | Output on refusal |
|-------|-------------------|-------------------|
| `food` words, `quantity`, `unit` from the parser | `fdc_id`, `description`, `kcal_per_100g`, `energy_nutrient_id`, `grams`, a plain-language explanation of the grams | One outcome code from C-8 and, for `AMBIGUOUS`, up to 3 candidate descriptions |

Order: Curated Food Map (exact match on singular words), then C-4 search with the P-3 rule. Grams: as given for `g`; otherwise map portion, else one FDC portion by preference (medium, large, serving), else `NEEDS_GRAMS`. The resolver never returns a guessed or zero value.

## C-8: Outcome Codes

Used in replies, logs and tests so everyone means the same thing.

| Code | Saved | Tester sees | Cause |
|------|-------|-------------|-------|
| `LOGGED` | Yes | Item, grams, kcal, today's total | Reliable match and grams |
| `UNSUPPORTED_FORMAT` | No | Format hint with two examples | Not one of the accepted forms |
| `OUT_OF_RANGE` | No | Allowed ranges | Count or grams outside limits |
| `NOT_FOUND` | No | Try a simpler name | No reliable match |
| `AMBIGUOUS` | No | Up to 3 options; be more specific | Matches differ by more than 25% |
| `NEEDS_GRAMS` | No | Send it in grams | No portion weight for a count |
| `NO_ENERGY_VALUE` | No | Try a similar food | Record has no kcal |
| `LOOKUP_FAILED` | No | Try again in a minute | FDC error, limit or timeout |
| `NOT_REGISTERED` | No | Send /start first | No user row |

Log-only codes: `AUTH_REJECTED`, `BAD_UPDATE`, `DUPLICATE`, `REPLY_FAILED`, `INTERNAL_ERROR`, `FDC_OK`, `FDC_RATE_LIMITED`, `FDC_KEY_REJECTED`, `FDC_UNAVAILABLE`.

## Contract Checks for the Test Strategy

Proposed for Sohail's [Test Strategy](../testing/test-strategy.md). Items marked "spike" already ran in [INV-01](../../spikes/inv-01-lookup-storage/results-2026-10-14.md) against synthetic data.

| Contract | Check | Kind |
|----------|-------|------|
| C-1 | Wrong secret gets 403 and nothing runs | Unit plus V-3 on the host |
| C-1 | Same `update_id` twice creates one entry | Unit |
| C-1 | Group chat, photo and edited message do not save | Unit |
| C-2 | Each accepted form and each rejected form in the table | Unit (spike) |
| C-2 | Repeat `/start` keeps one user and all entries | Unit (spike) |
| C-3 | `sendMessage` failure leaves the entry saved and logs `REPLY_FAILED` | Unit with a fake adapter |
| C-4 | 429, 403, 5xx and timeout each give `LOOKUP_FAILED` and save nothing | Unit with a fake adapter (spike covers timeout) |
| C-4, C-5 | Live fields and values for the 20 map foods | V-1 manual run |
| C-6 | Two testers see only their own entries; 15 testers with 10 entries each | Unit (spike) |
| C-6 | Midnight, Nov 1 2026 and Mar 14 2027 day windows | Unit (spike) |
| C-6 | Entry survives a process restart and a host reload | Unit (spike) plus V-4 |
| C-7 | Ambiguous, no energy and no portion paths never save | Unit (spike) |

## AI Disclosure

Drafted with Claude from the team's A2 files, INV-01 and the public Telegram and FDC documentation linked above; reviewed and edited by Adiya. See the [AI Use Log](../ai/ai-use-log.md).

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-10-14 | Created draft for architecture review | Adiya |
