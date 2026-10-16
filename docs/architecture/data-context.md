# Data and Context Ownership

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |
| Status | Draft for architecture review. Built on proposed decisions [ADR-0001](../decisions/adr-0001-no-ai-in-bot.md) to [ADR-0008](../decisions/adr-0008-performance-and-capacity-checks.md); items marked *(Proposed)* answer OQ-8 and need team agreement |

This file says what data the Cycle 1 bot handles, which copy is authoritative, who is responsible for it, what is sensitive, who can see it, what is logged, how long it is kept, and how we recover when something goes wrong. Components and trust boundaries are in [Architecture](architecture.md); exact fields and tables are in [API Contracts](api-contracts.md), C-1 and C-6.

The bot has no AI behavior ([ADR-0001](../decisions/adr-0001-no-ai-in-bot.md)). [Architecture](architecture.md), Section 6, applies the eight boundary questions to FDC and Telegram; this file owns the data-level answers to **Read, Infer, Log and Recover**.

## Data Inventory

| Data | Comes from | Authoritative copy | Responsible | Sensitivity | Who can see it |
|------|-----------|--------------------|-------------|-------------|----------------|
| Telegram user ID | Telegram (`message.from.id`) | `users` table, SQLite on the host | Adiya (data model, C-6) | Personal identifier | The bot; developers with host access |
| Food entries: food words the tester typed, FDC ID, matched description, quantity, unit, grams, kcal, source, time saved (UTC) | Tester message + FDC lookup | `entries` table | Adiya (data model); deployer keeps the file | Personal: eating habits | The tester, through the bot (FR-7); developers with host access |
| Processed `update_id` values | Telegram | `processed_updates` table | Deployer | Not personal on its own | Developers with host access |
| Food cache (FDC records we looked up) | FDC | `food_cache` table; FDC is the true source | Adiya | Public (CC0), no tester data | Developers with host access |
| Curated Food Map | T-13 hand check | `data/food_map.json` in the repo | Adiya, with the T-13 checker | Public, no tester data | Anyone |
| Operations log: outcome code, handling time, FDC status | The bot | Host server and error logs | Deployer | Not personal: no Telegram IDs and no food text | Developers with host access |
| Secrets: bot token, webhook secret, FDC key, tester invite code (if FR-10 is accepted) | BotFather, api.data.gov, the team | Host environment and each developer's local `.env` | Deployer | Secret | Developers with host access |
| Tester roster: who agreed to test and when they were invited | The team | Kept outside the repo by the G-4 owners | Mazen and Khumoyun | Personal (names) | Mazen and Khumoyun |
| Engineering records: docs, Issues, PRs, reviews | The team | This GitHub repository | Each file's named owner | **Public repository** | Anyone |

**Never read or stored:** first name, last name, username, language, contacts, photos or location from Telegram ([API Contracts](api-contracts.md), C-1). Telegram's own message time is not used; the entry time is the server clock when the entry is saved ([ADR-0007](../decisions/adr-0007-chicago-day.md)). Nothing else is stored (NFR-4, [TR-3](../decisions/tradeoff-records.md)).

*(Proposed)* The tester roster does not record Telegram user IDs, so names and food data are never linked in one place.

## AI Context Sources
- **The bot:** none. It calls no AI model ([ADR-0001](../decisions/adr-0001-no-ai-in-bot.md)).
- **The team's AI tools** (approved in the [AI Use Policy](../ai/ai-policy.md)) may be given repository documents, code and synthetic test data. Never the database, host logs, the tester roster, `.env` files, tokens or keys (AI Use Policy, Section 6).
- AI-assisted work is disclosed in the [AI Use Log](../ai/ai-use-log.md) and reviewed by a person before merging.

## Visibility Rules
1. A tester sees only their own entries. Every Entry Store method takes a Telegram user ID, and there is no method that lists every tester's entries (C-6, FR-7).
2. Host access is limited to named developers with two-factor authentication ([Architecture](architecture.md), TB-4; [ADR-0006](../decisions/adr-0006-hosting-and-storage.md)).
3. The repository is public, so tester data never goes into GitHub: no Telegram IDs, food entries, database files, logs from the host or chat screenshots in commits, Issues, PRs or test evidence. Test evidence uses team members' own accounts and synthetic data.
4. Tester data is never pasted into AI tools or the team group chat.

## Boundary Questions: Read, Infer, Log, Recover

| Question | Answer |
|----------|--------|
| **Read** | The bot reads only `update_id`, chat ID, chat type, sender ID, message text and message date from each Telegram update (C-1). FDC receives only food words and FDC IDs, never who asked ([Architecture](architecture.md), TB-2). Team AI tools receive no tester data. Hidden on purpose: other testers' entries, names and usernames, secrets. |
| **Infer** | The bot may infer only which FDC record matches the food words ([ADR-0002](../decisions/adr-0002-food-data-source-and-matching.md)), the grams ([ADR-0003](../decisions/adr-0003-quantity-to-grams.md)), the calories, and which Chicago day an entry belongs to ([ADR-0007](../decisions/adr-0007-chicago-day.md)). It never infers diet, health or habits, never guesses calories (AC-6.2), and never compares testers. *(Proposed)* The team does not analyze any single tester's food data; we review only counts of outcome codes. |
| **Log** | See Logging below. |
| **Recover** | See Recovery below. |

Call, Change, Approve and Observe are answered in [Architecture](architecture.md), Sections 6 and 7.

## Logging
- **The database** is the record of what was saved.
- **The operations log** records the outcome code, handling time in milliseconds and FDC status for each message. It never contains Telegram IDs, food text, message text or secrets ([Architecture](architecture.md), components 11 and 12).
- **Processed update IDs** are kept 48 hours for duplicate checks, then deleted (C-1).
- **Weekly health check:** count of each outcome code, 95th-percentile handling time, FDC calls per hour and database file size (Risk 5, NFR-5).
- **Decisions, approvals and reviews** are recorded in GitHub (ADRs, PR reviews, Issues) and in [Meeting Notes](../meeting-notes.md).
- **Data deletions** are recorded in a deletion log: date, number of rows removed, and who ran and who confirmed it. It contains no food data and no Telegram IDs (checkpoint G-5).

## Recovery

| What went wrong | How we notice | What we do |
|-----------------|---------------|------------|
| Bot token leaked | Seen in the repo, a log, a chat or an AI tool | Revoke it in BotFather, install the new token, reset the webhook, then open an Issue without the token (G-6, Risk 6) |
| FDC key leaked | Seen anywhere public, or FDC rejects the key | Get a new key, update the host environment, restart (G-6) |
| Database damaged or a bad migration | Errors on every write | Restore the latest nightly backup copy ([ADR-0006](../decisions/adr-0006-hosting-and-storage.md)); tell affected testers which entries may be missing |
| Host account lost | Cannot log in, or the host deletes the app | Accepted Cycle 1 risk (Risk 22): backups live on the same host, so data is lost; tell testers and restart from a fresh database |
| Wrong value in the Curated Food Map | A tester report or a T-13 recheck | Fix the map by reviewed PR (G-2), then recompute the affected entries by FDC ID |
| Tester asks for their data to be deleted | The request comes from that tester's own Telegram account | One developer runs the deletion for that user ID and a second confirms it (G-5). *(Proposed)* Done within 7 days, and the tester is told when it's done |

## Retention *(Proposed; answers OQ-8 with the tester notice, T-25)*

| Data | Kept until |
|------|-----------|
| Tester accounts and entries | The end of the semester, then the database is deleted. TODO: confirm the exact date |
| Nightly backup copies | The last 7 copies; all are deleted with the database |
| Processed update IDs | 48 hours (already decided in C-1) |
| Operations log | The end of the semester, along with the database |
| Tester roster | The end of the semester |

A tester can ask for deletion at any time (see Recovery).

The `/privacy` reply (AC-10.3) and the tester notice (T-25) use this section. They tell testers what is stored and why, that Telegram carries their messages, that FDC receives only food words, how long data is kept, and how to ask for deletion. No outside tester is onboarded until the notice is approved (checkpoint G-4, OQ-8).

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created for Assignment 3 from ADR-0001 to ADR-0008, Architecture and API Contracts | Mazen |