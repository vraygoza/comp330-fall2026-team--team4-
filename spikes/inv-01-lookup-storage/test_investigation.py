"""INV-01 checks for storage, restart, isolation, the Chicago day and the never-save rules.

Run: python3 -m unittest -v test_investigation.py

AI-assisted (Claude). Human review: Adiya (pending), second reviewer: TODO.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import calorie_core as core

HERE = Path(__file__).parent
FIXTURE = HERE / "fixtures" / "fdc_synthetic.json"
FOOD_MAP = {k: v for k, v in json.loads((HERE / "fixtures" / "food_map_synthetic.json").read_text()).items()
            if not k.startswith("_")}


def chicago(y, mo, d, h, mi, s=0, fold=0):
    """A Chicago wall-clock time converted to UTC."""
    return datetime(y, mo, d, h, mi, s, tzinfo=core.CHICAGO, fold=fold).astimezone(timezone.utc)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "bot.db")
        self.db = core.connect(self.path)
        self.client = core.FixtureClient(FIXTURE)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def log(self, user, text, when):
        return core.handle_text(self.db, user, text, when, self.client, FOOD_MAP)


class NeverSaveRules(Base):
    """AC-6.1 and AC-6.2: nothing is saved unless the result is reliable."""

    def test_failure_outcomes_save_nothing(self):
        when = chicago(2026, 10, 14, 12, 0)
        for msg in ["150g rice", "mystery stew", "xyzfood", "apple", "100g oats",
                    "a cup of rice", "eggs 2", "1/2 banana", "25 eggs", "0 eggs"]:
            outcome, _, entry_id = self.log(1, msg, when)
            self.assertNotEqual(outcome, core.Outcome.LOGGED, msg)
            self.assertIsNone(entry_id, msg)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM entries").fetchone()[0], 0)

    def test_lookup_failure_saves_nothing(self):
        failing = core.FixtureClient(FIXTURE, fail=True)
        outcome, _, entry_id = core.handle_text(self.db, 1, "2 eggs", chicago(2026, 10, 14, 12, 0),
                                                failing, FOOD_MAP)
        self.assertEqual(outcome, core.Outcome.LOOKUP_FAILED)
        self.assertIsNone(entry_id)

    def test_schema_rejects_zero_calories(self):
        with self.assertRaises(Exception):
            self.db.execute("INSERT INTO users VALUES (1, '2026-10-14 00:00:00')")
            self.db.execute("INSERT INTO entries (telegram_user_id, food_text, quantity, unit, grams,"
                            " kcal, source, logged_at_utc) VALUES (1,'x',1,'g',1,0,'fdc','2026-10-14 00:00:00')")


class Conversion(Base):
    def test_count_uses_portion_and_reply_states_assumption(self):
        outcome, reply, _ = self.log(1, "2 eggs", chicago(2026, 10, 14, 8, 0))
        self.assertEqual(outcome, core.Outcome.LOGGED)
        self.assertIn("2 x 1 large egg (50 g each) = 100 g", reply)
        self.assertIn("143 kcal", reply)  # 143 kcal/100 g x 100 g (synthetic value)

    def test_default_serving_is_stated(self):
        _, reply, _ = self.log(1, "banana", chicago(2026, 10, 14, 8, 0))
        self.assertIn("assumed because no amount was given", reply)

    def test_atwater_energy_is_used_when_1008_missing(self):
        status, parsed = core.parse_message("120g apple")
        res = core.resolve(parsed, self.client, FOOD_MAP)
        self.assertEqual(res.energy_nutrient_id, 2047)


class StorageAndRestart(Base):
    def test_repeat_start_creates_one_user(self):
        now = datetime.now(timezone.utc)
        self.assertTrue(core.ensure_user(self.db, 7, now))
        self.assertFalse(core.ensure_user(self.db, 7, now))
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM users").fetchone()[0], 1)

    def test_entries_survive_process_restart(self):
        """Write in one Python process, read in a brand new one (simulates a host reload)."""
        self.db.close()
        writer = ("import calorie_core as c, json, sys;"
                  "from datetime import datetime, timezone;"
                  "db=c.connect(sys.argv[1]);"
                  "m={k:v for k,v in json.load(open(sys.argv[2])).items() if not k.startswith('_')};"
                  "cl=c.FixtureClient(sys.argv[3]);"
                  "print(c.handle_text(db,42,'2 eggs',datetime(2026,10,14,15,tzinfo=timezone.utc),cl,m)[0])")
        reader = ("import calorie_core as c, sys;"
                  "from datetime import date;"
                  "db=c.connect(sys.argv[1]);"
                  "print(c.total_for_day(db,42,date(2026,10,14)))")
        env = {**os.environ, "PYTHONPATH": str(HERE)}
        w = subprocess.run([sys.executable, "-c", writer, self.path,
                            str(HERE / "fixtures" / "food_map_synthetic.json"), str(FIXTURE)],
                           capture_output=True, text=True, env=env, check=True)
        r = subprocess.run([sys.executable, "-c", reader, self.path],
                           capture_output=True, text=True, env=env, check=True)
        self.assertEqual(w.stdout.strip(), "LOGGED")
        self.assertEqual(float(r.stdout.strip()), 143.0)
        self.db = core.connect(self.path)


class Isolation(Base):
    """AC-7.1: each tester sees only their own entries."""

    def test_two_testers(self):
        when = chicago(2026, 10, 14, 9, 0)
        self.log(1, "2 eggs", when)
        self.log(2, "banana", when)
        day = date(2026, 10, 14)
        self.assertEqual([r[0] for r in core.entries_for_day(self.db, 1, day)], ["eggs"])
        self.assertEqual([r[0] for r in core.entries_for_day(self.db, 2, day)], ["banana"])

    def test_fifteen_synthetic_testers(self):
        """NFR-2 capacity check through the handler (not through Telegram)."""
        when = chicago(2026, 10, 14, 12, 0)
        durations = []
        for user in range(1, 16):
            for _ in range(10):
                start = time.perf_counter()
                outcome, _, _ = self.log(user, "1 egg", when)
                durations.append(time.perf_counter() - start)
                self.assertEqual(outcome, core.Outcome.LOGGED)
        for user in range(1, 16):
            self.assertEqual(len(core.entries_for_day(self.db, user, date(2026, 10, 14))), 10)
        self.__class__.max_handler_ms = max(durations) * 1000


class ChicagoDay(Base):
    """AC-5.3 and the OQ-7 boundary rules."""

    def test_midnight_boundary(self):
        self.log(1, "2 eggs", chicago(2026, 10, 14, 23, 59, 59))
        self.log(1, "banana", chicago(2026, 10, 15, 0, 0, 0))
        self.assertEqual(core.total_for_day(self.db, 1, date(2026, 10, 14)), 143.0)
        self.assertAlmostEqual(core.total_for_day(self.db, 1, date(2026, 10, 15)), 105.02)

    def test_utc_date_differs_from_chicago_date(self):
        # 8:30 PM Chicago on Oct 14 is already Oct 15 in UTC. It must count for Oct 14.
        when = chicago(2026, 10, 14, 20, 30)
        self.assertEqual(when.date(), date(2026, 10, 15))
        self.log(1, "2 eggs", when)
        self.assertEqual(core.total_for_day(self.db, 1, date(2026, 10, 14)), 143.0)

    def test_fall_back_day_is_25_hours(self):
        start, end = core.chicago_day_window(date(2026, 11, 1))
        fmt = core.TS
        span = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
        self.assertEqual(span, timedelta(hours=25))
        # 1:30 AM happens twice on Nov 1. Both belong to Nov 1.
        self.log(1, "2 eggs", chicago(2026, 11, 1, 1, 30, fold=0))
        self.log(1, "2 eggs", chicago(2026, 11, 1, 1, 30, fold=1))
        self.assertEqual(core.total_for_day(self.db, 1, date(2026, 11, 1)), 286.0)

    def test_spring_forward_day_is_23_hours(self):
        start, end = core.chicago_day_window(date(2027, 3, 14))
        fmt = core.TS
        span = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
        self.assertEqual(span, timedelta(hours=23))
        self.log(1, "2 eggs", chicago(2027, 3, 14, 23, 59))
        self.log(1, "2 eggs", chicago(2027, 3, 15, 0, 1))
        self.assertEqual(core.total_for_day(self.db, 1, date(2027, 3, 14)), 143.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
