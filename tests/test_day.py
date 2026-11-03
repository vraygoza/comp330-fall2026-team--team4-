import unittest
from datetime import date, datetime
from zoneinfo import ZoneInfo

from src.core.day import chicago_day_bounds, total_for_day

UTC = ZoneInfo("UTC")


def entry(logged_at_utc, kcal):
    return {"logged_at_utc": logged_at_utc, "kcal": kcal}


class TestChicagoDayBounds(unittest.TestCase):

    def test_normal_day_is_24_hours(self):
        start, end = chicago_day_bounds(date(2026, 10, 14))
        self.assertEqual((end - start).total_seconds(), 24 * 3600)

    def test_fall_back_day_is_25_hours(self):
        start, end = chicago_day_bounds(date(2026, 11, 1))
        self.assertEqual((end - start).total_seconds(), 25 * 3600)

    def test_spring_forward_day_is_23_hours(self):
        start, end = chicago_day_bounds(date(2027, 3, 14))
        self.assertEqual((end - start).total_seconds(), 23 * 3600)


class TestTotalForDay(unittest.TestCase):

    def test_no_entries_returns_zero(self):
        self.assertEqual(total_for_day([], date(2026, 10, 14)), 0)

    def test_adds_up_entries_in_the_day(self):
        entries = [
            entry(datetime(2026, 10, 14, 13, 0, tzinfo=UTC), 140),
            entry(datetime(2026, 10, 14, 18, 30, tzinfo=UTC), 260),
        ]
        self.assertEqual(total_for_day(entries, date(2026, 10, 14)), 400)

    def test_entry_just_before_midnight_counts(self):
        # 11:59:59 PM Chicago on Oct 14 is 04:59:59 UTC on Oct 15
        entries = [entry(datetime(2026, 10, 15, 4, 59, 59, tzinfo=UTC), 100)]
        self.assertEqual(total_for_day(entries, date(2026, 10, 14)), 100)

    def test_entry_at_midnight_belongs_to_the_next_day(self):
        # 12:00:00 AM Chicago on Oct 15 is 05:00:00 UTC on Oct 15
        entries = [entry(datetime(2026, 10, 15, 5, 0, 0, tzinfo=UTC), 100)]
        self.assertEqual(total_for_day(entries, date(2026, 10, 14)), 0)
        self.assertEqual(total_for_day(entries, date(2026, 10, 15)), 100)

    def test_both_1_30_am_entries_count_on_fall_back_day(self):
        # Nov 1 2026 has 1:30 AM twice: once CDT (06:30 UTC), once CST (07:30 UTC)
        entries = [
            entry(datetime(2026, 11, 1, 6, 30, tzinfo=UTC), 50),
            entry(datetime(2026, 11, 1, 7, 30, tzinfo=UTC), 70),
        ]
        self.assertEqual(total_for_day(entries, date(2026, 11, 1)), 120)

    def test_other_days_are_excluded(self):
        entries = [
            entry(datetime(2026, 10, 13, 18, 0, tzinfo=UTC), 500),
            entry(datetime(2026, 10, 14, 18, 0, tzinfo=UTC), 200),
            entry(datetime(2026, 10, 16, 18, 0, tzinfo=UTC), 900),
        ]
        self.assertEqual(total_for_day(entries, date(2026, 10, 14)), 200)


if __name__ == "__main__":
    unittest.main()

class ChicagoDateOfTests(unittest.TestCase):
    """chicago_date_of was added in A4 (#50)."""

    def test_evening_after_utc_midnight_is_still_chicago_today(self):
        from datetime import date, datetime, timezone
        from src.core.day import chicago_date_of
        self.assertEqual(chicago_date_of(datetime(2026, 10, 27, 1, 0, tzinfo=timezone.utc)), date(2026, 10, 26))
        self.assertEqual(chicago_date_of(datetime(2026, 10, 27, 5, 0, tzinfo=timezone.utc)), date(2026, 10, 27))
