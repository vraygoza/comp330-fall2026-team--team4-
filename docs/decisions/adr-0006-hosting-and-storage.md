# ADR-0006: PythonAnywhere Free Web App with SQLite, Decided Together

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |

- **Status:** Proposed and **conditional** (P-7 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). Adopted only if checks V-2, V-3 and V-4 pass. TODO: record the check results and change to Accepted, with the date.
- **Decision owner:** Adiya (proposed owner of OQ-5), with Khumoyun running V-2 to V-4 (proposed)
- **Closes:** OQ-4 and OQ-5
- **Related:** FR-1 (AC-1.2), FR-2, FR-5, FR-7, NFR-1, NFR-2, NFR-4, NFR-5; T-3, T-6; Risks 5, 14, 18, 21 and 22

## Context
Storage and hosting have to be decided together. SQLite is safe only on a host whose disk survives restarts; a host that erases files would delete every tester's entries and break AC-1.2 (INV-01 Finding 5). Testers also need to reach the bot at any time, and every service must be free (NFR-5).

## Decision
1. **Option A:** a PythonAnywhere free web app, with the SQLite database file on its disk.
2. **One storage module:** only the Entry Store contains SQL ([Architecture](../architecture/architecture.md), Section 3), so moving to Postgres changes one module.
3. **Conditional:** adopt Option A only if V-2 (the host can reach `api.telegram.org` and `api.nal.usda.gov`), V-3 (the webhook works with a secret token) and V-4 (an entry survives a web app reload) all pass. If any fails, fall back to **Option B** and record the idle wake-up delay as an NFR-1 exception.
4. **Deploys:** only a tagged commit from `main`, by the deployer (Adiya, backup Khumoyun, proposed), followed by a smoke test of `/start`, `2 eggs` and `/today` (checkpoint G-3). The host login is held by named developers with two-factor authentication.
5. **Backups:** a nightly `sqlite3 .backup` copy kept on the host. Losing the host account itself is an accepted Cycle 1 risk (Risk 22).
6. **Secrets** (bot token, webhook secret, FDC key) live only in the host environment and developers' `.env` (NFR-3).
7. **Renewal:** the free web app expires unless renewed. INV-01 lists renewal every 3 months, but PythonAnywhere's [Free Accounts page](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/) (published 2026-01-15) lists a 1-month expiry. TODO: confirm the interval during V-2 to V-4. Until then, the deployer sets a monthly reminder.

## Options Considered
| Option | Entries survive a restart? | Meets the 5-second reply? | Main problem |
|--------|----------------------------|---------------------------|--------------|
| **A. PythonAnywhere free web app + SQLite** | Yes (V-4 to confirm) | Yes, if FDC is fast from the host (V-6) | `api.telegram.org` access unconfirmed (V-2); shared IP rate limit for FDC (V-5) |
| B. Render free web service + Neon free Postgres | Yes, in Neon | No for the first message after 15 idle minutes (about a 1-minute wake-up) | NFR-1 fails after idle; two accounts to secure |
| C. Render free + SQLite | **No:** files are erased on restart, redeploy and spin-down | Same as B | Loses tester data; rejected |
| D. A team member's always-on computer + SQLite | Yes | Yes, while the computer is on | Bot is down whenever that computer sleeps; tester data on a personal machine |

## Consequences
- **Good:** entries persist with no database server to run, and a move to Postgres touches one module.
- **Cost:** one web worker handles messages one at a time. That is enough for 15 testers (checked in [ADR-0008](adr-0008-performance-and-capacity-checks.md)).
- **Cost:** only the deployer can deploy until the backup is set up (Risk 21).
- **Risk:** if PythonAnywhere free blocks `api.telegram.org`, both this decision and [ADR-0005](adr-0005-python-flask-webhook.md) change (Risks 14 and 18).
- **Risk:** backups live on the same host, so losing the account loses the data (Risk 22).

## Evidence and Checks
- **Ran (synthetic data, 2026-10-14):** an entry written by one Python process was read by a new process from the same file; repeat `/start` kept one user; two testers saw only their own entries; 15 synthetic testers sent 150 messages with 0 errors ([spike results](../../spikes/inv-01-lookup-storage/results-2026-10-14.md)).
- **Still needed:** V-2, V-3 and V-4 on the real host (INV-01, "Verification Still Needed").

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created from P-7 in INV-01 | Mazen |