"""Chicago-day calculations for the daily calorie total.

Entries are stored with a UTC timestamp (see api-contracts.md C-6), but a
tester's "today" is a Chicago calendar day (ADR-0007 / P-8). This module
converts a Chicago date into the UTC window it covers, then sums the
calories inside that window.

The window is 23 hours on the spring-forward day and 25 hours on the
fall-back day, which is why it is computed per date instead of assuming 24.
"""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

CHICAGO = ZoneInfo("America/Chicago")
UTC = ZoneInfo("UTC")


def chicago_date_of(moment_utc):
    """Return the Chicago calendar date for a UTC moment (added in A4, #50).

    Example:
        chicago_date_of(datetime(2026, 10, 27, 1, 0, tzinfo=UTC)) -> date(2026, 10, 26)
        (01:00 UTC is 8:00 pm the evening before in Chicago)
    """
    return moment_utc.astimezone(CHICAGO).date()


def chicago_day_bounds(chicago_date):
    """Return the UTC start and end of one Chicago calendar day.

    The range is half-open: start is included, end is not.

    Example:
        chicago_day_bounds(date(2026, 10, 14))
        -> (2026-10-14 05:00 UTC, 2026-10-15 05:00 UTC)
    """
    start_local = datetime.combine(chicago_date, time.min, tzinfo=CHICAGO)
    end_local = datetime.combine(chicago_date + timedelta(days=1), time.min, tzinfo=CHICAGO)
    return start_local.astimezone(UTC), end_local.astimezone(UTC)


def total_for_day(entries, chicago_date):
    """Add up one tester's calories for a single Chicago day.

    entries is that tester's saved entries, each with a "logged_at_utc"
    datetime and a "kcal" number. Entries outside the day are ignored.
    Returns 0 when nothing was logged (AC-5.2).

    Example:
        entries = [{"logged_at_utc": datetime(2026, 10, 14, 18, 0, tzinfo=UTC), "kcal": 140}]
        total_for_day(entries, date(2026, 10, 14)) -> 140
    """
    start_utc, end_utc = chicago_day_bounds(chicago_date)
    total = 0
    for entry in entries:
        logged_at = entry["logged_at_utc"]
        if logged_at.tzinfo is None:
            logged_at = logged_at.replace(tzinfo=UTC)
        if start_utc <= logged_at < end_utc:
            total += entry["kcal"]
    return total