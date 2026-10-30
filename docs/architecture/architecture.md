# Cycle 1 Architecture Overview

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Mazen Malas (Operations & Evidence Lead) |
| Last updated | 2026-10-26 |
| Status | Draft. Built on proposed decisions P-1 to P-10, which the team votes on in #56. Construction changes are recorded in Section 11 |
| Baseline under review | Branch `docs/a3-architecture-adiya` (commit recorded in the review file when the PR opens) |

Related files: [Diagram](architecture-diagram.png) ([source](architecture-diagram.dot)), [API and Tool Contracts](api-contracts.md), [Data and Context](data-context.md), [INV-01 Investigation](investigations/inv-01-lookup-storage.md), [Requirements](../requirements/requirements.md).

## 1. Purpose

The system lets a tester text one food to a Telegram bot, finds the calories in USDA FoodData Central, saves the entry under that tester, and replies with the tester's total for the Chicago day. This document shows which component does each part of that path, which way dependencies point, where trust boundaries and human checkpoints sit, and how we observe and recover from failure.

The architecture serves the Cycle 1 vertical slice only (S1 to S8 in [Scope](../planning/scope.md)). It leaves room for macros (DF-1) by storing the matched FDC record ID with every entry, but it builds nothing for later cycles.

## 2. Architecture Decisions This Depends On

Each line becomes an ADR (owner Mazen, backup Adiya) once the team accepts it. Evidence is in [INV-01](investigations/inv-01-lookup-storage.md).

| ID | Proposed decision | If rejected, what changes here |
|----|-------------------|--------------------------------|
| P-1 | No AI in the running bot; deterministic parsing and matching | An AI boundary and approval design would be needed (Section 8) |
| P-2, P-3 | FDC with a curated food map and a strict, refuse-when-unsure search | Food Resolver and contract C-4 |
| P-4, P-5 | Gram, count and default-portion rules; accepted input forms | Message Parser and contract C-2 |
| P-6 | Flask webhook with a thin Telegram adapter | Webhook Endpoint and Telegram Adapter |
| P-7 | PythonAnywhere free + SQLite, conditional on V-2 to V-4 | Hosting box in the diagram and the Entry Store adapter only |
| P-8 | Chicago calendar day, UTC storage | Day Calculator |
| P-9, P-10 | Five-second and 15-tester checks | Test strategy only |

## 3. Components

The design is layered with the core in the middle. The core (parser, resolver, day calculator, use cases) has no knowledge of Telegram, Flask, HTTP or SQL. Adapters on the outside translate between the core and each external system. That is what lets P-6 and P-7 change without touching business rules.

| # | Component | Layer | Responsibility (one line) | Planned module |
|---|-----------|-------|---------------------------|----------------|
| 1 | Webhook Endpoint | Interface | Accepts Telegram POSTs, checks the secret header, drops repeats, hands the message to the router, always answers fast | `src/bot/web.py` |
| 2 | Command Router | Interface | Maps `/start`, `/today`, `/privacy`, plain text (and `/undo` if built) to a use case | `src/bot/router.py` |
| 3 | Use Cases | Core | Run each request end to end: register, log food, list today | `src/core/use_cases.py` |
| 4 | Message Parser | Core | Turns text into food words, quantity and unit, or a refusal reason | `src/core/parser.py` |
| 5 | Food Resolver | Core | Picks one reliable FDC record and gram amount, or refuses with a reason | `src/core/resolver.py` |
| 6 | Day Calculator | Core | Gives the UTC start and end of a Chicago calendar day | `src/core/day.py` |
| 7 | Telegram Adapter | Adapter | Calls Bot API `sendMessage` and `setWebhook`; holds the bot token | `src/adapters/telegram.py` |
| 8 | FDC Adapter | Adapter | Calls FDC search and food details with a timeout; holds the API key; fills the food cache | `src/adapters/fdc.py` |
| 9 | Entry Store | Adapter | The only code that runs SQL. Every read and write takes a Telegram user ID | `src/adapters/store.py` |
| 10 | Curated Food Map | Data (repo) | Reviewed mapping from tester words to one FDC record and default portion | `data/food_map.json` |
| 11 | SQLite Database | Data (host) | Tables `users`, `entries`, `food_cache`, `processed_updates` | `~/calorie-bot/bot.db` on the host |
| 12 | Operations Log | Data (host) | Outcome codes and timings, no food text, no Telegram IDs | Host server and error logs |

This table is the authoritative list of components and responsibilities (owner Khumoyun, backup Adiya). The separate component-responsibilities file planned in A3 was not created; Section 11 shows which modules exist in the A4 code.

### Dependency direction

```
Telegram --> Webhook Endpoint --> Command Router --> Use Cases --> Parser, Resolver, Day Calculator
                                                        |
                                                        +--> FoodSource port   <-- FDC Adapter --> FDC API
                                                        +--> EntryStore port   <-- Entry Store --> SQLite
                                                        +--> Messenger port    <-- Telegram Adapter --> Bot API
```

Rules the code review checks:

- `src/core/` imports nothing from `src/bot/` or `src/adapters/`, and nothing from Flask, `sqlite3` or `urllib`.
- Only `src/adapters/store.py` contains SQL.
- Only `src/adapters/telegram.py` and `src/adapters/fdc.py` read secrets, and only from environment variables.
- The Entry Store has no method that reads entries without a user ID.

## 4. The Vertical Slice, Step by Step

A tester sends `2 eggs`:

1. Telegram POSTs an Update to the webhook URL with the secret header (contract C-1).
2. Webhook Endpoint rejects a wrong or missing secret with 403. It ignores non-private chats and non-text messages with a short reply. It looks up `update_id` in `processed_updates`; a repeat is answered 200 and skipped.
3. Command Router sends plain text to the Log Food use case.
4. Use Case checks the tester is registered (FR-10 if accepted; otherwise any `/start` registers).
5. Message Parser returns `food="eggs", quantity=2, unit=count` (P-5).
6. Food Resolver finds `egg` in the Curated Food Map, asks the FDC Adapter for that record (cache first), reads kcal per 100 g (nutrient 1008, else 2047, else 2048) and uses the map portion (1 large egg, 50 g) (P-2 to P-4).
7. Use Case computes 100 g and the kcal, then the Entry Store saves the entry with the matched FDC ID and UTC time, and records the `update_id`, in one transaction.
8. Entry Store returns the Chicago-day total using the Day Calculator window (P-8).
9. Telegram Adapter sends: "Logged Egg, whole, raw, fresh: 2 x 1 large egg (50 g each) = 100 g = N kcal. Today's total: M kcal."
10. Webhook Endpoint returns 200 and writes one log line: outcome `LOGGED`, handler milliseconds, FDC status (P-9 measurement).

Any refusal in steps 5 or 6 (`UNSUPPORTED_FORMAT`, `OUT_OF_RANGE`, `NOT_FOUND`, `AMBIGUOUS`, `NEEDS_GRAMS`, `NO_ENERGY_VALUE`, `LOOKUP_FAILED`) skips step 7 entirely and replies with the reason. Nothing is saved. The spike shows each path ([INV-01 results](../../spikes/inv-01-lookup-storage/results-2026-10-14.md)).

## 5. Trust Boundaries and Security

| ID | Boundary | What crosses | Control |
|----|----------|--------------|---------|
| TB-1 | Internet to Webhook Endpoint | Telegram Updates | HTTPS; secret token header checked on every request; only `message` updates subscribed; private chats only |
| TB-2 | Bot to FDC | Food words, FDC IDs, API key | Outbound HTTPS; 3 second timeout; **no Telegram IDs or tester data sent** |
| TB-3 | Bot to Telegram | Reply text, chat ID, bot token | Outbound HTTPS; token only in environment |
| TB-4 | Developers to host | Code deploys, database file, logs | Host account login held by named developers (Section 7); 2FA on the host account |
| TB-5 | Developers to GitHub | Code and docs | No secrets in the repo (NFR-3); reviewed PRs only |

Identities and permissions:

| Identity | Can do | Cannot do |
|----------|--------|-----------|
| Tester (Telegram user ID) | Register, log food, read and (if built) undo **their own** entries | See anyone else's entries; change the food map; reach the database |
| Unknown Telegram user | Receive "closed test" reply (if FR-10 is accepted) | Create an account or store data |
| Telegram platform | Deliver Updates with the right secret | Anything without the secret |
| Developer with host access | Deploy, read logs, run deletion and backup scripts | Merge to `main` without a non-author review |
| GitHub contributor | Propose changes by PR | Commit secrets; change the food map without T-13 evidence |

Secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`, `FDC_API_KEY`, and `TESTER_INVITE_CODE` (if FR-10 is accepted). All live in the host's environment and in each developer's local `.env`. None appear in the repo, logs, AI tools or replies.

## 6. AI and Tool Boundaries

**Decision (P-1, proposed): the running bot has no AI behavior in Cycle 1.** Messages are parsed and matched by fixed rules. Reasons: results must be repeatable and testable, food logs are personal data that should not leave our system, and every service must be free. AI is used only by team members during development, governed by the [AI Use Policy](../ai/ai-policy.md) and the [AI Use Log](../ai/ai-use-log.md).

Following the assignment, we apply the eight boundary questions to the two external tools the bot does call. Data-level detail (Read, Infer, Log, Recover) is owned by [Data and Context](data-context.md); this is the architecture summary.

| Question | FDC (lookup tool) | Telegram Bot API (messaging tool) |
|----------|-------------------|-----------------------------------|
| Read | Receives only food words and FDC IDs. Never sees who asked | Holds the tester's chat. We read only `update_id`, `message.chat.id`, `message.chat.type`, `message.from.id`, `message.text`, `message.date`. Names and usernames are never read or stored |
| Infer | The bot infers only "this record matches these words," and only under P-3. It never infers diet, health or habits | No inference |
| Call | `GET /foods/search` and `GET /food/{fdcId}`. Limit 1,000 per hour per key or IP; we target under 200 per hour with the cache | `sendMessage` (one reply per tester message), `setWebhook` (deploy only) |
| Change | Read-only | Sends replies only. Cannot edit or delete tester messages |
| Approve | Food map changes need a reviewed PR with T-13 evidence (G-2 below) | Webhook URL changes are made only by the deployer (G-3) |
| Observe | FDC HTTP status, latency and `X-RateLimit-Remaining` are logged per call | Outcome code and handler time per update |
| Log | Status and time only; no tester data exists in these calls | `update_id` (kept 48 hours for duplicate checks), outcome, time |
| Recover | On failure, refuse and save nothing (`LOOKUP_FAILED`). On a bad map entry, fix by PR and recompute affected entries by `fdc_id` | Telegram retries failed deliveries; duplicates are skipped by `update_id`. A leaked token is revoked in BotFather |

## 7. Governance and Human Checkpoints

The bot never takes an action that needs approval at run time: it only writes the requesting tester's own entries. Human checkpoints sit around it.

| ID | Checkpoint | Who decides | Criteria | Evidence |
|----|------------|-------------|----------|----------|
| G-1 | Merge to `main` | A reviewer who is not the author | Review checklist; contract tests pass; no secrets | Submitted PR review |
| G-2 | Change to the Curated Food Map | Reviewer plus the person who did the T-13 check | Record and portion confirmed on the FDC website, kcal matches | PR links the T-13 row |
| G-3 | Deploy to the host | Deployer: Adiya (backup Khumoyun, proposed) | Only a tagged commit from `main`; smoke test `/start`, `2 eggs`, `/today` with a developer account | Deploy line in meeting notes |
| G-4 | Tester onboarding | Mazen and Khumoyun (G6 owners) | Tester received the collection notice (OQ-8) and the invite link | Tester list kept outside the repo |
| G-5 | Data deletion request | One developer runs it, a second confirms | Request came from that tester's Telegram account | Deletion log: date, internal row count, who ran and confirmed; no food data |
| G-6 | Secret exposure | Whoever finds it, then the Team Lead | Any token or key in the repo, a log, a chat or an AI tool | Revoke and rotate first, then an Issue |

## 8. Operability and Recovery

| Failure | How we see it | What the system does | Recovery |
|---------|---------------|----------------------|----------|
| FDC slow or down | `LOOKUP_FAILED` count and FDC status in the log | Refuses, saves nothing, tells the tester to retry | Wait; cached and mapped foods still work if cached |
| FDC rate limit (429) | `X-RateLimit-Remaining` trending down; 429 in the log | Same as above | Cache more foods in the map; request a higher limit |
| Telegram resends an update | Repeat `update_id` | Skips it; no double entry | None needed |
| Host restart or reload | Web app reload in the host log | Entries persist in the SQLite file (V-4) | None needed |
| Bad deploy | Smoke test fails, error log | Previous version still tagged | Redeploy the previous tag |
| Database file damaged or a bad migration | Errors on every write | Writes fail; tester told to retry | Restore the nightly `sqlite3 .backup` copy kept on the host. Host loss is an accepted Cycle 1 risk |
| Wrong value in the food map | Tester or T-13 recheck reports it | Keeps using it until fixed | PR to fix (G-2); recompute entries with that `fdc_id` |
| Bot token leak | Found in repo, log or chat | Attacker could send as the bot | Revoke in BotFather, set the new token, reset the webhook (Risk 6) |
| Host free tier expires | Host dashboard warning | Web app stops | Renew every 3 months; calendar reminder for the deployer |

Health signals reviewed weekly (Risk 5 and NFR-5): count of each outcome code, 95th percentile handler time, FDC calls per hour, database file size.

## 9. How the Architecture Meets the Requirements

| Requirement | Where it is met |
|-------------|-----------------|
| FR-1 Start (AC-1.1, AC-1.2) | Router, Register use case, Entry Store `INSERT OR IGNORE` |
| FR-2 Log food (AC-2.1, AC-2.2) | Parser (P-5), Resolver portions (P-4), reply states the grams |
| FR-3 Lookup (AC-3.1, AC-3.2) | Resolver, FDC Adapter, Curated Food Map built from T-13 |
| FR-4 Running total | Entry Store total with Day Calculator window |
| FR-5 Today (AC-5.1 to AC-5.3) | Today use case, Day Calculator (P-8) |
| FR-6 Unknown foods (AC-6.1, AC-6.2) | Refusal outcomes; schema rejects `kcal <= 0` |
| FR-7 Separation (AC-7.1) | Every Entry Store method requires a user ID |
| FR-10 Tester access (proposed) | Register use case checks the invite code |
| NFR-1 Five seconds | Cache, map, 3 second FDC timeout, measurement in Section 4 step 10 |
| NFR-2 15 testers | One worker handles requests in turn; synthetic 15-tester check (P-10) |
| NFR-3 No secrets in repo | Section 5 secrets; G-1, G-6 |
| NFR-4 Minimum data | Data read list in Section 6; schema in [api-contracts.md](api-contracts.md) C-6 |
| NFR-5 Free tiers | Hosting and FDC choices; weekly health signals |

## 10. Known Risks and Open Items

| Item | Effect if it goes wrong | Link |
|------|-------------------------|------|
| V-2: PythonAnywhere free may block `api.telegram.org` | Hosting falls back to Option B; library and storage adapter change | INV-01, Risk 14 |
| V-1: Real FDC fields and portions differ from the fixture | Resolver rules and contract C-4 need changes | INV-01, Risk 4 |
| Ambiguity rule refuses too many messages | Testers get frustrated | P-3, measured in test week |
| Single developer deploys | Delays if the deployer is unavailable | G-3 backup |
| Host loss loses data | Tester history gone | Accepted for Cycle 1; noted in [Risk Register](../planning/risk-register.md) |

These feed the risk register (owner Mazen) and the re-estimation notes (owner Sohail and Bazid).

**Live check status (2026-10-26):** V-1 to V-6 have not been run. The A4 slice is built so it does not depend on them (Section 11). Whether they are completed in A4 or deferred to A5 is the Team Lead's call; the outcome is recorded here and in the [Risk Register](../planning/risk-register.md).

## 11. Construction Changes from Assignment 3

Checked against the code on 2026-10-26 (A5, issue #51). Recommendations behind each change are in the [A1 design check](../reviews/a1-design-check.md). None of these changes the core design: the core still has no knowledge of Telegram, Flask, HTTP or SQL, and secrets are still read only in adapters.

| # | A3 design | A4 code | Why | Reverts when |
|---|-----------|---------|-----|--------------|
| CC-1 | Food Resolver (`src/core/resolver.py`) uses FDC and the curated food map (P-2, P-3, C-4, C-5) | `src/core/food_lookup.py` returns calories from a made-up sample list (`src/core/sample_foods.json`). `lookup()` is the seam the resolver replaces | V-1 has not run; A3 feedback says to build only work that does not depend on unverified FDC behavior | V-1 passes and the FDC Adapter is built |
| CC-2 | Calories computed from grams (P-4, ADR-0003) | `quantity x kcal_per_serving` | Sample data is per serving | CC-1 reverts |
| CC-3 | Webhook only (P-6, C-1, C-3) | Webhook built and unit tested (`src/bot/web.py`). Added `src/bot/poll.py`, a development-only runner using Telegram `getUpdates`, outside contract C-3. Both share `src/bot/router.py` | V-2 to V-4 have not run, so no public webhook URL exists | Never deployed; removed or kept as a dev tool once the host passes V-2 to V-4 |
| CC-4 | Curated Food Map at `data/food_map.json` | Sample file at `src/core/sample_foods.json` | `.gitignore` ignores every `data/` folder | The real food map arrives; the ignore rule is narrowed then |
| CC-5 | Duplicate `update_id` check on every webhook request (C-1, T-30) | Marked TODO in `src/bot/web.py` | Owned by Khumoyun (T-30, formerly T-27; task ID map, #74); not needed for the local slice. **The bot is not deployed until T-30 merges**: without it, a Telegram resend could log a meal twice (Risk Register, #58) | T-30 merges |

Modules in the A4 code, mapped to Section 3: Webhook Endpoint `src/bot/web.py`; Command Router `src/bot/router.py`; Telegram Adapter `src/adapters/telegram.py`; Food lookup (stand-in for the Food Resolver) `src/core/food_lookup.py`. Not yet built: Use Cases, Message Parser (K2, #61), Day Calculator (B2, #44), Entry Store, FDC Adapter.

**Final check after the integration PR (A4, #50):** TODO before this PR merges: compare the merged parser, daily total, storage and wiring with Sections 3 and 4, and add any further row above.

## AI Disclosure

Drafted with Claude from the team's A2 files, the A2 feedback and the INV-01 results; reviewed and edited by Adiya. See the [AI Use Log](../ai/ai-use-log.md).

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-10-14 | Created draft for architecture review | Adiya |
| 2026-10-26 | Added Section 11 (construction changes CC-1 to CC-5), live check status, removed link to the uncreated component-responsibilities file | Adiya |
| 2026-10-29 | CC-5: no deploy until T-27 merges (from Mazen review on #71) | Adiya |
| 2026-10-29 | CC-5: duplicate check renumbered T-27 to T-30 (task ID map, #74) | Adiya |
