"""Tests for the Entry Store (issue #50, A4). Uses a temporary SQLite file."""

import os
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone

from src.adapters.store import EntryStore

UTC = timezone.utc
T1 = datetime(2026, 11, 3, 18, 0, tzinfo=UTC)
T2 = datetime(2026, 11, 3, 19, 0, tzinfo=UTC)
DAY_START = datetime(2026, 11, 3, 6, 0, tzinfo=UTC)
DAY_END = datetime(2026, 11, 4, 6, 0, tzinfo=UTC)

TESTER_A = 1001
TESTER_B = 2002


class StoreTests(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        self.store = EntryStore(self.path)
        self.addCleanup(os.remove, self.path)
        self.addCleanup(self.store.close)

    def add(self, user, kcal, when=T1):
        return self.store.add_entry(user, "eggs", "Egg", 2, "count", kcal, "sample", when)

    def test_register_creates_once(self):
        self.assertTrue(self.store.register(TESTER_A, T1))
        self.assertFalse(self.store.register(TESTER_A, T2))
        self.assertTrue(self.store.is_registered(TESTER_A))
        self.assertFalse(self.store.is_registered(TESTER_B))

    def test_repeat_start_keeps_entries(self):
        # AC-1.2: a second /start must not erase anything.
        self.store.register(TESTER_A, T1)
        self.add(TESTER_A, 140)
        self.store.register(TESTER_A, T2)
        self.assertEqual(len(self.store.entries_between(TESTER_A, DAY_START, DAY_END)), 1)

    def test_entries_are_returned_in_time_window(self):
        self.store.register(TESTER_A, T1)
        self.add(TESTER_A, 100, T1)
        self.add(TESTER_A, 200, T2)
        self.add(TESTER_A, 999, DAY_END)  # end is exclusive
        rows = self.store.entries_between(TESTER_A, DAY_START, DAY_END)
        self.assertEqual([r["kcal"] for r in rows], [100, 200])
        self.assertEqual(rows[0]["logged_at_utc"], T1)

    def test_tester_a_never_sees_tester_b(self):
        # AC-7.1: every read is scoped to the requesting tester.
        self.store.register(TESTER_A, T1)
        self.store.register(TESTER_B, T1)
        self.add(TESTER_A, 100)
        self.add(TESTER_B, 555)
        self.assertEqual([r["kcal"] for r in self.store.entries_between(TESTER_A, DAY_START, DAY_END)], [100])
        self.assertEqual([r["kcal"] for r in self.store.entries_between(TESTER_B, DAY_START, DAY_END)], [555])

    def test_zero_or_negative_calories_are_refused(self):
        # AC-6.2: never save a zero or guessed calorie value.
        self.store.register(TESTER_A, T1)
        with self.assertRaises(sqlite3.IntegrityError):
            self.add(TESTER_A, 0)

    def test_entry_needs_a_registered_tester(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.add(TESTER_B, 100)

    def test_naive_time_is_refused(self):
        self.store.register(TESTER_A, T1)
        with self.assertRaises(ValueError):
            self.add(TESTER_A, 100, datetime(2026, 11, 3, 18, 0))

    def test_entries_survive_reopening_the_file(self):
        # ADR-0006: entries persist in the SQLite file across restarts.
        self.store.register(TESTER_A, T1)
        self.add(TESTER_A, 140)
        self.store.close()
        reopened = EntryStore(self.path)
        self.addCleanup(reopened.close)
        self.assertTrue(reopened.is_registered(TESTER_A))
        self.assertEqual(len(reopened.entries_between(TESTER_A, DAY_START, DAY_END)), 1)


if __name__ == "__main__":
    unittest.main()
