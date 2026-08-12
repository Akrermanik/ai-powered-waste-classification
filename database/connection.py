"""Database connection and schema initialization."""

import sqlite3
from pathlib import Path

from core.config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL DEFAULT (datetime('now')),
            label TEXT NOT NULL,
            confidence REAL NOT NULL,
            object_count INTEGER,
            inference_time_ms REAL,
            bbox_json TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id)"
    )

    _migrate_legacy_users(cursor)
    conn.commit()
    conn.close()


def _migrate_legacy_users(cursor: sqlite3.Cursor) -> None:
    """Migrate old users table (username PK, no id) if present."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
        return

    columns = {row[1] for row in cursor.execute("PRAGMA table_info(users)")}
    if "id" in columns:
        return

    cursor.execute("ALTER TABLE users RENAME TO users_legacy")
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    cursor.execute(
        """
        INSERT INTO users (username, name, password_hash)
        SELECT username, name, password_hash FROM users_legacy
        """
    )
    cursor.execute("DROP TABLE users_legacy")
