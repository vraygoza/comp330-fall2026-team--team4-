"""Duplicate update protection (T-30, contract C-1, ADR-0005). A6 boundary hardening.

Telegram can deliver the same update more than once: a webhook retry after a slow
or failed response, or polling again after a crash. The rule under test:
the same update_id produces at most one entry and at most one reply.

Three levels, matching the A5 feedback on contract tests at each boundary:
1. Entry Store: the update_id and the entry are written in one transaction.
2. Parser to store (route_update with a real store): repeat messages are idempotent.
3. Webhook to service (Flask test client with a real store): a resent POST is
   answered 200, sends no second reply and saves nothing.

Done criterion from the task ID map (#74): "The same update_id sent twice produces
one entry; verified by a unit test." Calorie values come from the sample list.
"""

import logging
import os
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from unittest import mock
from zoneinfo import ZoneInfo

from src.adapters.store import EntryStore
from src.bot.router import WELCOME, route_update
from src.bot.web import create_app
from src.core.food_lookup import lookup
from src.core.ports import DuplicateUpdate

UTC = timezone.utc
NOON = datetime(2026, 11, 20, 12, 0, tzinfo=ZoneInfo("America/Chicago")).astimezone(UTC)
EVERYTHING = (datetime(2000, 1, 1, tzinfo=UTC), datetime(2100, 1, 1, tzinfo=UTC))
TESTER = 1001
SECRET = "test-secret-not-real"
TACO = lookup("taco").kcal_per_serving


def update(text, update_id, user=TESTER):
    return {
        "update_id": update_id,
        "message": {"chat": {"id": user, "type": "private"}, "from": {"id": user}, "text": text},
    }


class TempStoreMixin:
    def make_store(self):
        handle, self.path = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        store = EntryStore(self.path)
        self.addCleanup(os.remove, self.path)
        self.addCleanup(store.close)
        return store

    def saved(self, store, user=TESTER):
        return store.entries_between(user, *EVERYTHING)


# 1. Entry Store

class StoreDuplicateTests(TempStoreMixin, unittest.TestCase):
    def setUp(self):
        self.store = self.make_store()
        self.store.register(TESTER, NOON)

    def add(self, update_id, kcal=140):
        return self.store.add_entry(TESTER, "eggs", "Egg", 2, "count", kcal, "sample", NOON, update_id=update_id)

    def test_mark_processed_records_once(self):
        self.assertFalse(self.store.is_processed(50))
        self.assertTrue(self.store.mark_processed(50, NOON))
        self.assertFalse(self.store.mark_processed(50, NOON))
        self.assertTrue(self.store.is_processed(50))

    def test_same_update_id_saves_one_entry(self):
        self.add(51)
        with self.assertRaises(DuplicateUpdate):
            self.add(51)
        self.assertEqual(len(self.saved(self.store)), 1)

    def test_refused_entry_does_not_record_the_update_id(self):
        # One transaction: if the entry is refused (kcal must be > 0), the ID is rolled back too,
        # so a corrected resend is not wrongly skipped.
        with self.assertRaises(sqlite3.IntegrityError):
            self.add(52, kcal=0)
        self.assertFalse(self.store.is_processed(52))
        self.assertEqual(self.saved(self.store), [])

    def test_entry_without_update_id_still_works(self):
        # Existing callers that pass no update_id keep the A4 behavior.
        self.add(None)
        self.add(None)
        self.assertEqual(len(self.saved(self.store)), 2)

    def test_ids_older_than_48_hours_are_removed(self):
        self.store.mark_processed(53, NOON - timedelta(hours=49))
        self.store.mark_processed(54, NOON - timedelta(hours=47))
        self.store.mark_processed(55, NOON)  # cleanup runs here
        self.assertFalse(self.store.is_processed(53))
        self.assertTrue(self.store.is_processed(54))

    def test_processed_ids_survive_a_restart(self):
        # Polling after a crash can see the same update again; the record is in the file.
        self.add(56)
        self.store.close()
        reopened = EntryStore(self.path)
        self.addCleanup(reopened.close)
        self.assertTrue(reopened.is_processed(56))


# 2. Parser to store, through the router

class RepeatMessageTests(TempStoreMixin, unittest.TestCase):
    def setUp(self):
        self.store = self.make_store()
        route_update(update("/start", 1), store=self.store, now_utc=NOON)

    def send(self, text, update_id, store=None, when=NOON):
        return route_update(update(text, update_id), store=store or self.store, now_utc=when)

    def test_resent_food_message_logs_once_and_replies_once(self):
        first = self.send("2 tacos", 10)
        second = self.send("2 tacos", 10)
        self.assertEqual(first.outcome, "LOGGED")
        self.assertIn(f"Today's total: {2 * TACO:g} kcal", first.reply)
        self.assertEqual(second.outcome, "DUPLICATE")
        self.assertIsNone(second.chat_id)
        self.assertIsNone(second.reply)
        self.assertEqual(len(self.saved(self.store)), 1)

    def test_third_copy_is_also_skipped(self):
        for _ in range(3):
            self.send("2 tacos", 11)
        self.assertEqual(len(self.saved(self.store)), 1)

    def test_same_text_with_a_new_update_id_is_a_real_second_meal(self):
        self.send("2 tacos", 12)
        result = self.send("2 tacos", 13)
        self.assertEqual(result.outcome, "LOGGED")
        self.assertIn(f"Today's total: {4 * TACO:g} kcal", result.reply)
        self.assertEqual(len(self.saved(self.store)), 2)

    def test_resent_start_is_skipped(self):
        result = self.send("/start", 1)
        self.assertEqual(result.outcome, "DUPLICATE")
        self.assertIsNone(result.reply)

    def test_resent_refusal_is_skipped_and_saves_nothing(self):
        self.assertEqual(self.send("2 dragonfruit", 14).outcome, "NOT_FOUND")
        self.assertEqual(self.send("2 dragonfruit", 14).outcome, "DUPLICATE")
        self.assertEqual(self.saved(self.store), [])

    def test_two_copies_at_the_same_moment_save_once(self):
        # Both copies pass the early is_processed check before either has saved.
        # The transaction in add_entry still lets only one through.
        class RacingStore:
            def __init__(self, real):
                self.real = real

            def is_processed(self, update_id):
                return False

            def __getattr__(self, name):
                return getattr(self.real, name)

        racing = RacingStore(self.store)
        first = self.send("2 tacos", 15, store=racing)
        second = self.send("2 tacos", 15, store=racing)
        self.assertEqual(first.outcome, "LOGGED")
        self.assertEqual(second.outcome, "DUPLICATE")
        self.assertIsNone(second.reply)
        self.assertEqual(len(self.saved(self.store)), 1)

    def test_internal_error_is_not_recorded_so_a_resend_can_succeed(self):
        class FailOnceStore:
            def __init__(self, real):
                self.real = real
                self.failed = False

            def add_entry(self, *args, **kwargs):
                if not self.failed:
                    self.failed = True
                    raise RuntimeError("simulated disk error")
                return self.real.add_entry(*args, **kwargs)

            def __getattr__(self, name):
                return getattr(self.real, name)

        flaky = FailOnceStore(self.store)
        with self.assertLogs("src.bot.router", level=logging.ERROR):
            self.assertEqual(self.send("2 tacos", 16, store=flaky).outcome, "INTERNAL_ERROR")
        self.assertFalse(self.store.is_processed(16))
        self.assertEqual(self.send("2 tacos", 16, store=flaky).outcome, "LOGGED")
        self.assertEqual(len(self.saved(self.store)), 1)

    def test_reused_id_after_48_hours_is_processed(self):
        # Telegram may restart update_id numbering after a week without updates.
        self.send("2 tacos", 17)
        later = NOON + timedelta(days=8)
        self.send("an egg", 99, when=later)  # any new update runs the cleanup
        self.assertEqual(self.send("2 tacos", 17, when=later).outcome, "LOGGED")

    def test_without_a_store_nothing_is_tracked(self):
        # Skeleton behavior (#48) is unchanged: no store, no duplicate check.
        self.assertEqual(route_update(update("/start", 18)).reply, WELCOME)
        self.assertEqual(route_update(update("/start", 18)).reply, WELCOME)


# 3. Webhook to service

class FakeMessenger:
    def __init__(self):
        self.sent = []

    def send_message(self, chat_id, text):
        self.sent.append((chat_id, text))
        return True


@mock.patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": SECRET})
class WebhookDuplicateTests(TempStoreMixin, unittest.TestCase):
    def setUp(self):
        self.store = self.make_store()
        self.messenger = FakeMessenger()
        self.client = create_app(self.messenger, store=self.store).test_client()

    def post(self, body):
        return self.client.post(
            "/telegram/webhook", json=body, headers={"X-Telegram-Bot-Api-Secret-Token": SECRET}
        )

    def test_webhook_logs_food_end_to_end(self):
        self.assertEqual(self.post(update("/start", 1)).status_code, 200)
        self.assertEqual(self.post(update("2 tacos", 2)).status_code, 200)
        self.assertEqual(len(self.saved(self.store)), 1)
        self.assertIn(f"= {2 * TACO:g} kcal", self.messenger.sent[-1][1])

    def test_telegram_retry_gets_200_one_reply_and_one_entry(self):
        self.post(update("/start", 1))
        body = update("2 tacos", 2)
        first = self.post(body)
        retry = self.post(body)
        self.assertEqual((first.status_code, retry.status_code), (200, 200))  # 200 stops Telegram resending
        self.assertEqual(len(self.messenger.sent), 2)  # welcome + one food reply
        self.assertEqual(len(self.saved(self.store)), 1)

    def test_duplicate_log_line_has_no_food_text_or_ids(self):
        self.post(update("/start", 1))
        self.post(update("2 tacos", 2))
        with self.assertLogs("src.bot.web", level=logging.INFO) as logs:
            self.post(update("2 tacos", 2))
        line = " ".join(logs.output)
        self.assertIn("outcome=DUPLICATE", line)
        self.assertNotIn("taco", line.lower())
        self.assertNotIn(str(TESTER), line)


if __name__ == "__main__":
    unittest.main()
