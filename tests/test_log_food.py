"""End-to-end tests for the Cycle 1 slice (issue #50, A4).

message -> parse (K2) -> lookup (A3) -> save under the tester ID -> daily total (B2) -> reply.
Runs through the router with a real EntryStore on a temporary file, so every
piece is exercised together. Calorie values come from the made-up sample list.
"""

import os
import tempfile
import unittest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from src.adapters.store import EntryStore
from src.bot.router import WELCOME, route_update
from src.core.food_lookup import lookup
from src.core.use_cases import (
    FORMAT_REPLY, GRAMS_REPLY, NOT_REGISTERED_REPLY, RANGE_REPLY,
)

UTC = timezone.utc
CHICAGO = ZoneInfo("America/Chicago")
NOON = datetime(2026, 11, 3, 12, 0, tzinfo=CHICAGO).astimezone(UTC)

TESTER_A = 1001
TESTER_B = 2002

TACO = lookup("taco").kcal_per_serving
BANANA = lookup("banana").kcal_per_serving
EGG = lookup("egg").kcal_per_serving


def chicago(y, m, d, hh, mm):
    return datetime(y, m, d, hh, mm, tzinfo=CHICAGO).astimezone(UTC)


def update(text, user=TESTER_A):
    return {
        "update_id": 1,
        "message": {"chat": {"id": user, "type": "private"}, "from": {"id": user}, "text": text},
    }


def n(value):
    return f"{value:g}"


class LogFoodTests(unittest.TestCase):
    def setUp(self):
        handle, path = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        self.store = EntryStore(path)
        self.addCleanup(os.remove, path)
        self.addCleanup(self.store.close)

    def send(self, text, user=TESTER_A, when=NOON):
        return route_update(update(text, user), store=self.store, now_utc=when)

    def saved(self, user=TESTER_A):
        start = datetime(2000, 1, 1, tzinfo=UTC)
        end = datetime(2100, 1, 1, tzinfo=UTC)
        return self.store.entries_between(user, start, end)

    # Registration

    def test_start_registers_and_welcomes(self):
        result = self.send("/start")
        self.assertEqual(result.reply, WELCOME)
        self.assertTrue(self.store.is_registered(TESTER_A))

    def test_food_before_start_is_refused(self):
        result = self.send("2 tacos")
        self.assertEqual(result.outcome, "NOT_REGISTERED")
        self.assertEqual(result.reply, NOT_REGISTERED_REPLY)
        self.assertEqual(self.saved(), [])

    # The happy path (AC-2.1, AC-3.1, AC-4.1)

    def test_logs_food_and_replies_with_total(self):
        self.send("/start")
        result = self.send("2 tacos")
        self.assertEqual(result.outcome, "LOGGED")
        self.assertIn(f"= {n(2 * TACO)} kcal", result.reply)
        self.assertIn(f"Today's total: {n(2 * TACO)} kcal", result.reply)
        self.assertEqual(len(self.saved()), 1)

    def test_running_total_adds_up(self):
        self.send("/start")
        self.send("2 tacos")
        result = self.send("an egg")
        self.assertIn(f"Today's total: {n(2 * TACO + EGG)} kcal", result.reply)

    def test_no_amount_assumes_one_serving_and_says_so(self):
        # AC-2.2
        self.send("/start")
        result = self.send("banana")
        self.assertEqual(result.outcome, "LOGGED")
        self.assertIn("assumed because no amount was given", result.reply)
        self.assertIn(f"= {n(BANANA)} kcal", result.reply)

    # Refusals save nothing (AC-2.4, AC-6.1, AC-6.2)

    def test_unknown_food_saves_nothing(self):
        self.send("/start")
        result = self.send("2 dragonfruit")
        self.assertEqual(result.outcome, "NOT_FOUND")
        self.assertIn("nothing was saved", result.reply)
        self.assertEqual(self.saved(), [])

    def test_unsupported_format_saves_nothing(self):
        self.send("/start")
        result = self.send("eggs 2")
        self.assertEqual(result.reply, FORMAT_REPLY)
        self.assertEqual(self.saved(), [])

    def test_out_of_range_saves_nothing(self):
        self.send("/start")
        self.assertEqual(self.send("25 eggs").reply, RANGE_REPLY)
        self.assertEqual(self.saved(), [])

    def test_grams_save_nothing_until_real_data(self):
        # Section 3 and architecture.md CC-2: the sample list has no per-gram values.
        self.send("/start")
        self.assertEqual(self.send("150g rice").reply, GRAMS_REPLY)
        self.assertEqual(self.saved(), [])

    # Chicago day (AC-5.3, ADR-0007)

    def test_total_resets_at_chicago_midnight(self):
        self.send("/start")
        self.send("2 tacos", when=chicago(2026, 11, 3, 23, 30))
        result = self.send("an egg", when=chicago(2026, 11, 4, 0, 10))
        self.assertIn(f"Today's total: {n(EGG)} kcal", result.reply)

    def test_evening_after_utc_midnight_is_still_today(self):
        # 8:00 pm Chicago is already the next day in UTC.
        self.send("/start")
        self.send("2 tacos", when=chicago(2026, 11, 3, 9, 0))
        result = self.send("an egg", when=chicago(2026, 11, 3, 20, 0))
        self.assertIn(f"Today's total: {n(2 * TACO + EGG)} kcal", result.reply)

    # Tester separation (AC-7.1)

    def test_two_testers_have_separate_totals(self):
        self.send("/start", user=TESTER_A)
        self.send("/start", user=TESTER_B)
        self.send("2 tacos", user=TESTER_A)
        result = self.send("an egg", user=TESTER_B)
        self.assertIn(f"Today's total: {n(EGG)} kcal", result.reply)
        self.assertEqual(len(self.saved(TESTER_A)), 1)
        self.assertEqual(len(self.saved(TESTER_B)), 1)

    def test_repeat_start_keeps_the_total(self):
        # AC-1.2
        self.send("/start")
        self.send("2 tacos")
        self.send("/start")
        result = self.send("an egg")
        self.assertIn(f"Today's total: {n(2 * TACO + EGG)} kcal", result.reply)


if __name__ == "__main__":
    unittest.main()
