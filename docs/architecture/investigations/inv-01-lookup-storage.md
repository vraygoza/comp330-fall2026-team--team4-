# INV-01: Lookup and Storage Investigation

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun (Operations & Evidence Co-Lead) |
| Last updated | 2026-10-14 |
| Status | Offline part ran 2026-10-14. Live FDC and hosting checks not yet run (V-1 to V-6) |
| Baseline | Branch `docs/a3-architecture-adiya`, starting from A2 checkpoint `4cf90ab` |

This investigation tests the A2 [Technical Recommendations](../technical-recommendations.md) before the team accepts them. It answers the A2 feedback request for "one small synthetic lookup-and-storage investigation, with alternatives, findings and a proposed decision," and records what actually ran and what is still uncertain.

Nothing here is an accepted decision. Each proposed decision (P-1 to P-10) becomes an ADR in [`/docs/decisions/`](../../decisions/) once the team accepts it at the architecture review. ADRs are owned by Mazen, with Adiya as backup.

## Questions Investigated

| ID | Question | Open question |
|----|----------|---------------|
| Q1 | Can a tester's amount ("2 eggs", "150g rice", "banana") become a gram quantity that FDC can support? | OQ-2, OQ-6 |
| Q2 | When is a lookup reliable enough to save, and what does the bot say when it is not? | OQ-2, FR-6 |
| Q3 | Where do entries live so a restart does not erase them, and which host fits that storage? | OQ-4, OQ-5 |
| Q4 | Does "today" stay correct at midnight and on daylight-saving days? | OQ-7, AC-5.3 |
| Q5 | What exactly is the five-second check, and does lookup time count? | NFR-1 |
| Q6 | How do "3 outside testers" (Definition of Done) and "supports 15 testers" (NFR-2) fit together? | NFR-2 |

## What Ran (2026-10-14)

All results below come from the spike in [`/spikes/inv-01-lookup-storage/`](../../../spikes/inv-01-lookup-storage/). Full output: [results-2026-10-14.md](../../../spikes/inv-01-lookup-storage/results-2026-10-14.md).

**Important limit:** the spike ran against a **synthetic fixture** shaped like FDC records. Calorie values in it are placeholders, not FDC data. The run proves the rules and the storage behavior. It does not prove that FDC returns the records, fields or values we expect. That is V-1.

### Message cases (19 synthetic messages)

| Result | Messages |
|--------|----------|
| Saved, with the conversion stated in the reply | `2 eggs`, `egg`, `banana`, `150g rice cooked`, `egg white`, `120g apple` |
| Not saved: ambiguous match | `150g rice` (raw and cooked rice differ about 2.8 times in kcal per 100 g) |
| Not saved: no portion weight, asked for grams | `1 rice cooked`, `apple` |
| Not saved: record has no energy value | `100g oats` |
| Not saved: no reliable match | `mystery stew`, `xyzfood` |
| Not saved: format not accepted | `a cup of rice`, `eggs 2`, `1/2 banana` |
| Not saved: amount out of range | `25 eggs`, `0 eggs`, `3000g rice cooked` |
| Not saved: lookup timeout (simulated) | `150g rice cooked` with a failing client |

6 entries saved, 13 refused, 0 saved with a guessed or zero value.

### Automated checks (14 of 14 passed)

| Check | What it shows |
|-------|---------------|
| Failure outcomes save nothing | AC-6.1, AC-6.2 hold for every refusal path, including lookup failure |
| Schema rejects zero calories | The database itself refuses `kcal = 0` (second line of defense) |
| Count uses portion; default is stated | "2 x 1 large egg (50 g each) = 100 g" appears in the reply (AC-2.2) |
| Atwater fallback | A record with only nutrient 2047 still yields kcal |
| Repeat `/start` | One user row after two registrations (AC-1.2) |
| Restart persistence | Entry written by one Python process is read by a new process from the same file |
| Two testers | Each sees only their own entries (AC-7.1) |
| 15 synthetic testers | 150 messages through the handler, 0 errors, 10 entries per tester, no leakage |
| Midnight | 11:59:59 PM and 12:00:00 AM Chicago land on different days |
| UTC versus Chicago date | 8:30 PM Chicago on Oct 14 is Oct 15 in UTC and still counts for Oct 14 |
| Fall back (Nov 1, 2026) | The day is 25 hours; both 1:30 AM entries count for Nov 1 |
| Spring forward (Mar 14, 2027) | The day is 23 hours; 11:59 PM and 12:01 AM split correctly |

### Desk research (checked 2026-10-14)

| Topic | Finding | Source |
|-------|---------|--------|
| FDC limits | 1,000 requests per hour by default; exceeding it blocks the key for 1 hour (HTTP 429). `DEMO_KEY` allows 30 per hour and 50 per day. The guide states the limit per IP address | [FDC API Guide](https://fdc.nal.usda.gov/api-guide) |
| FDC terms | Data is public domain (CC0 1.0); USDA asks for credit to FoodData Central. Keys found in public repositories are deactivated | [FDC API Guide](https://fdc.nal.usda.gov/api-guide) |
| Render free | Ephemeral filesystem (lost on restart, redeploy and spin-down); spins down after 15 idle minutes, about 1 minute to wake; no persistent disk on free; free Postgres is deleted after 30 days plus a 14-day grace period | [Render free docs](https://render.com/docs/free) |
| Neon free | Permanent free plan, no card; 1 GB per project; compute suspends after 5 idle minutes | [Neon pricing](https://neon.com/pricing) |
| PythonAnywhere free | Outbound internet only to an allowlist through a proxy. `api.nal.usda.gov` is on the allowlist. `api.telegram.org` was not found in the part of the list I could read, so it is unconfirmed. Webhook bots were reported working on free accounts in 2024; free web apps must be renewed every 3 months | [Allowlist](https://www.pythonanywhere.com/whitelist/), [PythonAnywhere blog](https://blog.pythonanywhere.com/148/) |
| Telegram webhooks | Secret token arrives in header `X-Telegram-Bot-Api-Secret-Token`; failed deliveries are retried; updates are kept at most 24 hours; webhook and `getUpdates` are mutually exclusive; ports 443, 80, 88, 8443 | [Bot API](https://core.telegram.org/bots/api) |
| Telegram send limits | About 1 message per second per chat; about 30 per second overall | [Bot FAQ](https://core.telegram.org/bots/faq) |
| Bot library | `python-telegram-bot` 22.8 is the current release on PyPI. It is built on `asyncio` | PyPI index, checked with `pip index versions` |

## Findings

1. **A successful HTTP response is not a correct match.** Generic words hit several records with very different calories ("rice" raw versus cooked; "egg" whole, white or yolk). Taking the first search result would save wrong totals without warning.
2. **Counts need a portion weight, and not every record has a usable one.** Foundation records often have no portion data, and some SR Legacy records only list "1 cup," which is not a count. A count without a weight must be refused, not guessed.
3. **Energy is not always nutrient 1008.** Some Foundation records report only Atwater energy (2047 or 2048). The lookup must check all three and refuse when none exist. (Shown with fixture data; the live run must confirm how often this happens.)
4. **A curated map for common foods removes most ambiguity.** The 20 foods hand-checked in T-13 can become a reviewed map from tester words to one FDC record and one default portion. T-13 then produces running configuration, not only a report.
5. **Storage and hosting are one decision.** SQLite is safe only on a host whose disk survives restarts. Render free does not qualify; PythonAnywhere free does (not yet tested, V-4).
6. **Hosting changes the library choice.** PythonAnywhere free runs web apps through WSGI. `python-telegram-bot` is asynchronous and expects to own an event loop, which fits a long-running process better than a WSGI view. A webhook in Flask that calls two Bot API methods directly is simpler on this host.
7. **Telegram retries can double-log.** If our webhook fails or times out after saving, Telegram resends the same update. We must record processed `update_id` values and skip repeats.
8. **The rate limit may be shared on PythonAnywhere.** The FDC guide states the limit per IP address, and PythonAnywhere free traffic leaves through a shared proxy. If that is how it is enforced, other users could spend our quota. A small food cache and the curated map reduce our calls; V-5 checks the headers.
9. **Daylight saving is real for this project.** Clocks fall back on Sunday, November 1, 2026, inside the likely tester window. Storing UTC and computing the Chicago day window per date handles it.

## Alternatives

### Hosting and storage (Q3)

| Option | Persistence on restart | Fits 5-second reply | Cost and limits | Main risk |
|--------|------------------------|---------------------|-----------------|-----------|
| **A. PythonAnywhere free web app (webhook) + SQLite file** | Yes, disk persists (V-4 to confirm) | Yes, if FDC latency from the host is low (V-6) | Free; one web worker; renew every 3 months; outbound allowlist | `api.telegram.org` access unconfirmed (V-2); shared IP rate limit (V-5) |
| B. Render free web service + Neon free Postgres | Yes, in Neon | No for the first message after 15 idle minutes (about 1 minute wake) | Free; two vendors; 750 instance hours per month | NFR-1 fails after idle; two accounts to secure |
| C. Render free + SQLite | **No.** File is erased on restart, redeploy and spin-down | Same as B | Free | Loses tester data: rejected |
| D. Team member's always-on computer, polling + SQLite | Yes | Yes while the computer is on | Free | Bot is down whenever that computer sleeps; data on a personal machine |

### Food matching (Q2)

| Option | Strength | Weakness |
|--------|----------|----------|
| Take the top search result | Simplest | Saves wrong values silently (Finding 1). Rejected |
| **Curated map for T-13 foods, then strict search with an ambiguity check** | Common foods are reviewed by a person; anything uncertain is refused with a reason | Map needs maintenance through PRs |
| Ask the tester to choose from a numbered list | Tester resolves ambiguity | Two-step conversation needs saved state; more scope than Cycle 1 |
| Open Food Facts instead of FDC | Stronger for packaged products | Weaker for generic foods ("banana", "rice") |

## Proposed Decisions (for ADRs)

| ID | Decision | Closes | Status |
|----|----------|--------|--------|
| P-1 | No AI behavior in the running bot for Cycle 1. Parsing and matching are deterministic rules | AI boundary (A3 Section 6) | Proposed |
| P-2 | USDA FoodData Central, Foundation and SR Legacy datasets only, with a curated food map built from T-13 and a strict search fallback | OQ-2 | Proposed |
| P-3 | Matching rule: every query word must appear in the record description, the record's first word must be one of the query words, and if the top matched records differ by more than 25% in kcal per 100 g the message is ambiguous and nothing is saved | OQ-2, FR-6 | Proposed |
| P-4 | Quantity rule: grams are used as given; a count or no amount uses the curated map portion, else one FDC portion chosen by a fixed preference (medium, large, serving); if none exists, ask for grams. Every reply states the grams used | OQ-6, AC-2.2 | Proposed |
| P-5 | Accepted input forms: `<number> <food>`, `<number>g <food>`, `a <food>`, `<food>`. Limits: 1 to 20 items, 1 to 2000 grams, 100 characters. Everything else gets a format hint and nothing is saved | OQ-6 | Proposed |
| P-6 | Python 3.10 or later; Flask webhook with a thin Telegram adapter calling `sendMessage` and `setWebhook` directly. `python-telegram-bot` stays the alternative if we move to a host with a long-running process | OQ-3 | Proposed (changes the A2 recommendation, see Finding 6) |
| P-7 | Option A: PythonAnywhere free web app with SQLite on its disk, behind a storage module so a move to Postgres (Option B) touches one module. Adopt only if V-2, V-3 and V-4 pass; otherwise fall back to Option B and accept the idle wake-up delay as a recorded NFR-1 exception | OQ-4, OQ-5 | Proposed, conditional |
| P-8 | "Today" is the Chicago calendar day for every tester. Timestamps are stored in UTC; the day window is computed per date with `America/Chicago`, so 23 and 25 hour days are correct | OQ-7 | Proposed |
| P-9 | NFR-1 check: time from webhook receipt to the `sendMessage` call returning, including lookup. Pass when 95% of logged messages over the test week are 5 seconds or less, and 10 manual stopwatch trials from a phone are all 5 seconds or less | NFR-1 | Proposed |
| P-10 | NFR-2 is a capacity criterion checked with 15 synthetic tester IDs through the handler plus whatever real testers are enrolled. The Definition of Done needs at least 3 real outside testers. Fewer than 15 real testers does not fail NFR-2 | NFR-2, DoD | Proposed |

## Verification Still Needed

| ID | Check | Proposed owner | Pass when |
|----|-------|----------------|-----------|
| V-1 | Live FDC run of the 20 T-13 foods (`run_investigation.py --live`): records found, energy nutrient, portion fields, kcal compared with the FDC website | Adiya with Sohail (T-13) | Every map food has one confirmed record and portion; field names match the contract |
| V-2 | From a PythonAnywhere free console, reach `api.telegram.org` and `api.nal.usda.gov` | Khumoyun (proposed backup investigation) | Both return HTTP 200 |
| V-3 | Register a test bot, set the webhook with a secret token to the PythonAnywhere URL, send `/start` | Khumoyun (proposed) | Webhook receives the update; wrong secret gets 403 |
| V-4 | Write an entry, reload the web app, read it back | Khumoyun (proposed) | Entry is still there |
| V-5 | Read `X-RateLimit-Remaining` on FDC calls made from PythonAnywhere | Adiya | Remaining count reflects only our calls |
| V-6 | Time 20 FDC searches from the host | Adiya | Slowest call under 3 seconds |

V-2 to V-4 are the specific investigation for my backup, so T-1 to T-3 do not all wait on one person. Khumoyun needs to agree to this on the team call.

## What Remains Uncertain

- Real FDC values, field names (`foodPortions` in food details, `foodMeasures` in search results) and how often Foundation records lack portions. Only V-1 answers this.
- Whether PythonAnywhere free allows `api.telegram.org`. If not, Option A fails and P-6 and P-7 change together.
- Whether the 25% ambiguity ratio refuses too many real messages. The test week should count `AMBIGUOUS` outcomes; if more than about 1 in 5 messages are refused, revisit P-3.
- Cooking state. The curated map must say which record represents a food as people usually eat it (for example cooked rice).

## Effect on Estimates (for Bazid)

- T-1, T-2, T-3: most of the analysis is done; remaining work is V-1 to V-6.
- T-9 and T-10: parsing rules are fixed and tested in the spike, so confidence can move from Low to Medium.
- T-11: grows. It now includes the curated map loader, the ambiguity rule and the energy fallback.
- T-13: becomes "build and verify the curated food map," not only a hand check.
- New work to estimate: processed `update_id` tracking (duplicate protection), food cache table, webhook secret check, tester invite check (if FR-10 is accepted).

## AI Disclosure

The spike code, fixture and this report were drafted with Claude from the team's A2 files, the A2 feedback and the public sources listed above. Adiya reviews every line before commit. The fixture values are invented on purpose and labeled as synthetic. An entry goes in the [AI Use Log](../../ai/ai-use-log.md).

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-10-14 | Created; offline spike run recorded | Adiya |
