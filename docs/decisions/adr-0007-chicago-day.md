# ADR-0007: "Today" Is the Chicago Calendar Day

| Field | Value |
|-------|-------|
| Owner | Mazen Malas (Operations & Evidence Lead) |
| Backup | Adiya (Architecture & Development Lead) |
| Last updated | 2026-10-15 |

- **Status:** Proposed (P-8 in [INV-01](../architecture/investigations/inv-01-lookup-storage.md)). TODO: change to Accepted, with the date, once the team accepts it at the architecture review.
- **Decision owner:** Adiya, with test cases from Sohail
- **Closes:** OQ-7 (confirms TD-2 in [Deferred Scope](deferred-scope.md))
- **Related:** FR-4, FR-5 (AC-5.3); T-14, T-17; Risk 20

## Context
TD-2 says "today" runs midnight to midnight Central time, and AC-5.3 says entries from before midnight are not in today's total. Two cases make this easy to get wrong. First, Chicago midnight is not UTC midnight, so an 8:30 PM meal in Chicago is already the next day in UTC. Second, daylight saving: on Sunday, November 1, 2026, clocks fall back and the day is 25 hours long, likely during our tester window (INV-01 Finding 9). On March 14, 2027, clocks spring forward and the day is 23 hours.

## Decision
1. "Today" is the Chicago calendar day for every tester.
2. Each entry's time is saved in UTC, taken from the server clock when the entry is saved ([API Contracts](../architecture/api-contracts.md), C-6).
3. The Day Calculator gives the UTC start and end of a Chicago day, from that day's midnight up to (not including) the next midnight, computed per date with the `America/Chicago` time zone. This handles 23- and 25-hour days.
4. Every "today" query (the running total and `/today`) uses the Day Calculator, never its own date math.
5. Central time stays an assumption: if a tester outside Central time joins, OQ-7 reopens (TD-2, ATD-3).

## Alternatives Considered
| Option | Why not chosen |
|--------|----------------|
| Store local Chicago time | During the fall-back hour, two different moments have the same local time |
| Use the UTC day | Meals after 7 PM in summer (6 PM in winter) would count toward the next day |
| Each tester's own time zone | Deferred (TD-2, ATD-3); testers are assumed to be in Central time |

## Consequences
- **Good:** one rule, handled by Python's standard library, correct on both daylight-saving days.
- **Cost:** code review has to confirm that every caller uses the Day Calculator (Risk 20).

## Evidence and Checks
- **Ran (synthetic data, 2026-10-14), all passed:** 11:59:59 PM and 12:00:00 AM Chicago landed on different days; an 8:30 PM Chicago entry on October 14 (October 15 in UTC) still counted for October 14; November 1, 2026 was 25 hours, with both 1:30 AM entries counting for that day; March 14, 2027 was 23 hours ([spike results](../../spikes/inv-01-lookup-storage/results-2026-10-14.md)).
- **Planned:** keep these four checks as unit tests in the [Test Strategy](../testing/test-strategy.md) (Sohail).

## Change Log
| Date | Change | By |
|------|--------|----|
| 2026-10-15 | Created from P-8 in INV-01 | Mazen |