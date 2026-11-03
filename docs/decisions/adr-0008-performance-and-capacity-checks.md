# ADR-0008: How We Check the 5-Second Reply and 15-Tester Capacity

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |

- **Status:** Proposed (P-9 and P-10 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). TODO: change to Accepted, with the date, once the team accepts it at the architecture review.
- **Decision owner:** Adiya, with Sohail
- **Closes:** OQ-10 and OQ-11
- **Related:** NFR-1, NFR-2, the Cycle 1 Definition of Done in [Scope](../planning/scope.md); T-23, T-24; Risks 14, 15 and 18

## Context
The A2 review asked two questions. First, does the food lookup count toward the 5-second reply target (NFR-1)? Second, how does "at least 3 outside testers" in the Definition of Done relate to "supports 15 testers" in NFR-2? Without one answer for each, nobody could say whether these requirements pass.

## Decision
1. **5-second check (P-9):** time is measured from when the webhook receives the message to when the `sendMessage` call returns, **including the food lookup**. It passes when 95% of logged messages over the test week take 5 seconds or less in the operations log, and 10 manual stopwatch trials from a phone all take 5 seconds or less. The 3-second FDC timeout keeps a failed lookup inside the limit.
2. **15-tester check (P-10):** NFR-2 is a capacity check. It passes when 15 synthetic tester IDs, 10 messages each, go through the handler with 0 errors and no tester seeing another's data, plus normal use by every enrolled tester in the test week.
3. **Definition of Done:** at least 3 real outside testers log meals. Having fewer than 15 real testers does not fail NFR-2.
4. **If hosting falls back to Option B** ([ADR-0006](adr-0006-hosting-and-storage.md)), the slow first reply after the host has been idle is recorded as an NFR-1 exception rather than hidden.

The matching NFR-1 and NFR-2 checks are in [Requirements](../requirements/requirements.md).

## Alternatives Considered
| Option | Why not chosen |
|--------|----------------|
| Time only the bot's own code, not the lookup | Leaves out the slowest part, which the tester actually waits for |
| Require 15 real testers for NFR-2 | Measures how well we recruit, not whether the system holds up |
| A few stopwatch trials only | Too few samples to trust; the log covers every message |

## Consequences
- **Good:** both checks are measurable, repeatable and written down before testing starts.
- **Cost:** the bot has to log its handling time for every message (step 10 in [Architecture](../architecture/architecture.md), Section 4).
- **Risk:** a slow FDC response from the host (V-6) could push replies past 5 seconds.
- **Open:** recruiting at least 3 outside testers is still needed (OQ-9, Risk 15).

## Evidence and Checks
- **Ran (synthetic data, 2026-10-14):** 15 synthetic testers sent 150 messages through the handler with 0 errors, 10 entries each and no data leaking between testers ([spike results](../../spikes/inv-01-lookup-storage/results-2026-10-14.md)).
- **Still needed:** V-6 (time 20 FDC searches from the host) and T-23 (reply timing during the test week), in Sohail's [Test Strategy](../testing/test-strategy.md).

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created from P-9 and P-10 in INV-01 | Mazen |