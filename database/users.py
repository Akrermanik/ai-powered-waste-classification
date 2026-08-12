"""User database operations."""

import sqlite3

from database.connection import get_connection, init_db


def create_user(username: str, name: str, password_hash: str) -> bool:
    init_db()
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, name, password_hash) VALUES (?, ?, ?)",
            (username, name, password_hash),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_username(username: str) -> dict | None:
    init_db()
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, username, name, password_hash, created_at FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> dict | None:
    init_db()
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, username, name, password_hash, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_users_credentials() -> dict:
    """Return credentials dict for streamlit-authenticator compatibility."""
    init_db()
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT username, name, password_hash FROM users"
        ).fetchall()
    finally:
        conn.close()

    credentials = {"usernames": {}}
    for row in rows:
        credentials["usernames"][row["username"]] = {
            "name": row["name"],
            "password": row["password_hash"],
        }
    return credentials
