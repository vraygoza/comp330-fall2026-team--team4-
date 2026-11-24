"""Entry Store (architecture.md, component 9; contract C-6).

The only module that runs SQL. Every method that reads or writes entries takes
a Telegram user ID, so one tester can never read another tester's entries
(FR-7, AC-7.1). Table and column names follow api-contracts.md C-6.

A4 scope (issue #50): the users and entries tables.
A6 scope (T-30): the processed_updates table. Each Telegram update_id is recorded
once. When an update saves an entry, the update_id and the entry are written in
one transaction, so a resent update can never save the meal twice (C-1, ADR-0005).
The food_cache table (T-31) comes later.

Uses the standard library sqlite3 module (ADR-0006). The database file is
ignored by git (*.db in .gitignore), so tester data never reaches the repo.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

from src.core.ports import DuplicateUpdate

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    telegram_user_id INTEGER PRIMARY KEY,
    created_at_utc   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS entries (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_user_id INTEGER NOT NULL REFERENCES users(telegram_user_id),
    food_text        TEXT NOT NULL,
    matched_description TEXT NOT NULL,
    quantity         REAL NOT NULL CHECK (quantity > 0),
    unit             TEXT NOT NULL CHECK (unit IN ('count', 'g', 'default')),
    kcal             REAL NOT NULL CHECK (kcal > 0),
    source           TEXT NOT NULL,
    logged_at_utc    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS entries_by_user_time ON entries (telegram_user_id, logged_at_utc);
CREATE TABLE IF NOT EXISTS processed_updates (
    update_id        INTEGER PRIMARY KEY,
    processed_at_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS processed_updates_by_time ON processed_updates (processed_at_utc);
"""

# ADR-0005 and architecture.md section 3: update IDs are kept 48 hours. Telegram
# resends within minutes, and it may restart its update_id numbering after a week
# with no updates, so old IDs must not block new messages.
PROCESSED_UPDATE_RETENTION = timedelta(hours=48)


def _to_text(moment: datetime) -> str:
    """Store UTC times as ISO text so they sort correctly."""
    if moment.tzinfo is None:
        raise ValueError("times must be timezone-aware UTC")
    return moment.astimezone(timezone.utc).isoformat()


def _from_text(value: str) -> datetime:
    return datetime.fromisoformat(value).astimezone(timezone.utc)


class EntryStore:
    def __init__(self, path: str):
        self._db = sqlite3.connect(path)
        self._db.execute("PRAGMA foreign_keys = ON")
        self._db.executescript(SCHEMA)
        self._db.commit()

    def close(self) -> None:
        self._db.close()

    # Users (FR-1)

    def register(self, user_id: int, now_utc: datetime) -> bool:
        """Create the tester if new. Returns True if created. Repeat /start keeps everything (AC-1.2)."""
        cursor = self._db.execute(
            "INSERT OR IGNORE INTO users (telegram_user_id, created_at_utc) VALUES (?, ?)",
            (user_id, _to_text(now_utc)),
        )
        self._db.commit()
        return cursor.rowcount == 1

    def is_registered(self, user_id: int) -> bool:
        row = self._db.execute(
            "SELECT 1 FROM users WHERE telegram_user_id = ?", (user_id,)
        ).fetchone()
        return row is not None

    # Entries (FR-2, FR-4, FR-7)

    def add_entry(self, user_id: int, food_text: str, matched_description: str,
                  quantity: float, unit: str, kcal: float, source: str,
                  now_utc: datetime, update_id: int | None = None) -> int:
        """Save one entry. With update_id, the ID is recorded in the same transaction (T-30).

        Raises DuplicateUpdate if that update_id was already recorded; nothing is saved.
        If the entry is refused (for example kcal <= 0), the update_id is not recorded either.
        """
        try:
            with self._db:  # one transaction: both rows commit, or neither does
                if update_id is not None:
                    self._db.execute(
                        "INSERT INTO processed_updates (update_id, processed_at_utc) VALUES (?, ?)",
                        (update_id, _to_text(now_utc)),
                    )
                cursor = self._db.execute(
                    "INSERT INTO entries (telegram_user_id, food_text, matched_description, quantity, unit, kcal, source, logged_at_utc)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, food_text, matched_description, quantity, unit, kcal, source, _to_text(now_utc)),
                )
        except sqlite3.IntegrityError as err:
            if update_id is not None and "processed_updates" in str(err):
                raise DuplicateUpdate(update_id) from err
            raise
        return cursor.lastrowid

    def entries_between(self, user_id: int, start_utc: datetime, end_utc: datetime) -> list[dict]:
        """One tester's entries with start <= logged_at_utc < end, as dicts for total_for_day."""
        rows = self._db.execute(
            "SELECT kcal, logged_at_utc, matched_description FROM entries"
            " WHERE telegram_user_id = ? AND logged_at_utc >= ? AND logged_at_utc < ?"
            " ORDER BY logged_at_utc",
            (user_id, _to_text(start_utc), _to_text(end_utc)),
        ).fetchall()
        return [
            {"kcal": kcal, "logged_at_utc": _from_text(logged), "matched_description": desc}
            for kcal, logged, desc in rows
        ]

    # Processed updates (C-1, T-30)

    def is_processed(self, update_id: int) -> bool:
        row = self._db.execute(
            "SELECT 1 FROM processed_updates WHERE update_id = ?", (update_id,)
        ).fetchone()
        return row is not None

    def mark_processed(self, update_id: int, now_utc: datetime) -> bool:
        """Record an update that saved no entry (/start, a refusal). Returns True if new.

        Also removes IDs older than 48 hours, so the table stays small.
        """
        with self._db:
            self._db.execute(
                "DELETE FROM processed_updates WHERE processed_at_utc < ?",
                (_to_text(now_utc - PROCESSED_UPDATE_RETENTION),),
            )
            cursor = self._db.execute(
                "INSERT OR IGNORE INTO processed_updates (update_id, processed_at_utc) VALUES (?, ?)",
                (update_id, _to_text(now_utc)),
            )
        return cursor.rowcount == 1
