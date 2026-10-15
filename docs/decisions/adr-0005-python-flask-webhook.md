# ADR-0005: Python with a Flask Webhook and a Thin Telegram Adapter

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |

- **Status:** Proposed (P-6 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). TODO: change to Accepted, with the date, once the team accepts it at the architecture review.
- **Decision owner:** Adiya
- **Closes:** OQ-3
- **Related:** T-2, T-4, T-5; NFR-1, NFR-3; Risks 12, 14 and 18

## Context
The A2 [Technical Recommendations](../architecture/technical-recommendations.md) proposed Python with the `python-telegram-bot` library. INV-01 found that our likely free host, PythonAnywhere ([ADR-0006](adr-0006-hosting-and-storage.md)), runs web apps through WSGI, while `python-telegram-bot` is asynchronous and expects to run its own long-lived event loop (INV-01 Finding 6). INV-01 also found that Telegram resends an update if our webhook fails or times out, which could log the same meal twice (Finding 7).

## Decision
1. **Python 3.10 or later.**
2. **A Flask web app receives Telegram webhooks** ([API Contracts](../architecture/api-contracts.md), C-1). A thin Telegram Adapter calls only two Bot API methods directly: `sendMessage` and `setWebhook` (C-3).
3. **Every request is checked** for Telegram's secret token header; a wrong or missing secret gets HTTP 403 and nothing runs.
4. **Duplicates are skipped:** each `update_id` is recorded in the same database transaction as the entry, so a resend cannot save the meal twice. Update IDs are kept 48 hours.
5. **The core stays independent:** the parser, resolver, day calculator and use cases import nothing from Flask, Telegram or database code ([Architecture](../architecture/architecture.md), Section 3). Changing the library or host changes the adapters only.
6. **`python-telegram-bot` stays the alternative** if we move to a host that runs a long-lived process.

## Alternatives Considered
| Option | Why not chosen |
|--------|----------------|
| `python-telegram-bot` (the A2 recommendation) | Fits a long-running process better than a WSGI web app on our likely host; kept as the fallback |
| Node.js with grammY | Only worth it if most of the team is stronger in JavaScript |
| Java with the TelegramBots library | More setup and code for a small bot |

## Consequences
- **Good:** few dependencies (Flask plus the standard library), a fit for the likely free host, and a core that can be tested without Telegram.
- **Cost:** we write and test our own small Telegram adapter and duplicate check instead of using a library's.
- **Risk:** if PythonAnywhere free blocks `api.telegram.org` (V-2), the host changes, and this decision may change with it (Risks 14 and 18).

## Evidence and Checks
- **Ran (2026-10-14):** the spike's core logic runs on the Python standard library (3.10 or later), and its 14 automated checks passed with Python's built-in `unittest` ([spike results](../../spikes/inv-01-lookup-storage/results-2026-10-14.md)).
- **Still needed:** V-3 sets a test bot's webhook with a secret token on PythonAnywhere; it passes when `/start` arrives and a wrong secret gets 403.
- **Planned:** contract checks for C-1: wrong secret, a repeated `update_id`, group chats and non-text messages.

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created from P-6 in INV-01 | Mazen |