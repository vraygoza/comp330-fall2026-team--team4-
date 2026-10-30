"""Contract tests for the B2 daily total (issue #44), written before it exists.

They check the interface agreed in docs/reviews/a1-design-check.md, Section 3, and
ADR-0007. Until chicago_day_bounds and daily_total are merged in src/core/day.py,
every test here is skipped, so CI stays green. When B2 merges, they run.

S2 (issue #53). Run: python -m unittest discover -s tests -t .
"""

import importlib.util
import unittest
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

UTC = timezone.utc
CHICAGO = ZoneInfo("America/Chicago")


def _day_ready():
    if importlib.util.find_spec("src.core.day") is None:
        return False
    import src.core.day as day
    return hasattr(day, "chicago_day_bounds") and hasattr(day, "daily_total")


DAY_READY = _day_ready()


@dataclass
class Entry:
    kcal: float
    logged_at: datetime


def chicago(y, m, d, hh, mm):
    return datetime(y, m, d, hh, mm, tzinfo=CHICAGO).astimezone(UTC)


@unittest.skipUnless(DAY_READY, "src/core/day.py not merged yet (B2, #44)")
class ChicagoDayBoundsTests(unittest.TestCase):
    def bounds(self, day):
        from src.core.day import chicago_day_bounds
        return chicago_day_bounds(day)

    def test_normal_day_is_24_hours(self):
        start, end = self.bounds(date(2026, 10, 26))
        self.assertEqual(start, datetime(2026, 10, 26, 5, 0, tzinfo=UTC))
        self.assertEqual(end, datetime(2026, 10, 27, 5, 0, tzinfo=UTC))

    def test_daylight_saving_end_is_25_hours(self):
        start, end = self.bounds(date(2026, 11, 1))
        self.assertEqual(start, datetime(2026, 11, 1, 5, 0, tzinfo=UTC))
        self.assertEqual(end, datetime(2026, 11, 2, 6, 0, tzinfo=UTC))
        self.assertEqual(end - start, timedelta(hours=25))

    def test_daylight_saving_start_is_23_hours(self):
        start, end = self.bounds(date(2027, 3, 14))
        self.assertEqual(end - start, timedelta(hours=23))

    def test_bounds_are_timezone_aware_utc(self):
        start, end = self.bounds(date(2026, 10, 26))
        self.assertEqual(start.utcoffset(), timedelta(0))
        self.assertEqual(end.utcoffset(), timedelta(0))


@unittest.skipUnless(DAY_READY, "src/core/day.py not merged yet (B2, #44)")
class DailyTotalTests(unittest.TestCase):
    def total(self, entries, today):
        from src.core.day import daily_total
        return daily_total(entries, today)

    def test_sums_only_today(self):
        entries = [
            Entry(100, chicago(2026, 10, 26, 9, 0)),
            Entry(250, chicago(2026, 10, 26, 18, 30)),
            Entry(999, chicago(2026, 10, 25, 12, 0)),
            Entry(999, chicago(2026, 10, 27, 8, 0)),
        ]
        self.assertEqual(self.total(entries, date(2026, 10, 26)), 350)

    def test_chicago_midnight_boundary(self):
        # Section 3: 23:30 counts for Oct 26; 00:10 counts for Oct 27 (AC-5.3).
        late = Entry(70, chicago(2026, 10, 26, 23, 30))
        early = Entry(105, chicago(2026, 10, 27, 0, 10))
        self.assertEqual(self.total([late, early], date(2026, 10, 26)), 70)
        self.assertEqual(self.total([late, early], date(2026, 10, 27)), 105)

    def test_utc_midnight_does_not_split_the_day(self):
        # 20:00 Chicago is 01:00 UTC the next day, but it is still Oct 26 in Chicago.
        evening = Entry(200, chicago(2026, 10, 26, 20, 0))
        self.assertEqual(evening.logged_at.date(), date(2026, 10, 27))
        self.assertEqual(self.total([evening], date(2026, 10, 26)), 200)

    def test_daylight_saving_night(self):
        # Section 3: on Nov 1, 23:30 Chicago is 05:30 UTC Nov 2 and counts for Nov 1.
        late = Entry(80, chicago(2026, 11, 1, 23, 30))
        next_day = Entry(95, chicago(2026, 11, 2, 0, 10))
        self.assertEqual(self.total([late, next_day], date(2026, 11, 1)), 80)
        self.assertEqual(self.total([late, next_day], date(2026, 11, 2)), 95)

    def test_start_is_inclusive_end_is_exclusive(self):
        at_start = Entry(10, datetime(2026, 10, 26, 5, 0, tzinfo=UTC))
        at_end = Entry(20, datetime(2026, 10, 27, 5, 0, tzinfo=UTC))
        self.assertEqual(self.total([at_start, at_end], date(2026, 10, 26)), 10)

    def test_no_entries_is_zero(self):
        self.assertEqual(self.total([], date(2026, 10, 26)), 0)


# Tester separation (AC-7.1) is not tested here: daily_total receives one tester's
# entries already filtered by Telegram user ID. That filter lives in the Entry Store,
# so its test (tester A cannot see tester B) belongs with the storage code in A4 (#50).


if __name__ == "__main__":
    unittest.main()
