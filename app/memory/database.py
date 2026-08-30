from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path


# =========================================================
# DATABASE PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "ace.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection() -> sqlite3.Connection:
    """Create a connection to the ACE AI SQLite database."""

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def initialize_database() -> None:
    """Create ACE AI database tables if they do not exist."""

    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.commit()


# =========================================================
# CONVERSATIONS
# =========================================================

def create_conversation(title: str = "New Chat") -> int:
    """Create a new conversation and return its ID."""

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO conversations (
                title,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?)
            """,
            (title, now, now),
        )

        connection.commit()

        return int(cursor.lastrowid)


def get_conversations() -> list[dict]:
    """Return all conversations, newest first."""

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT
                id,
                title,
                created_at,
                updated_at
            FROM conversations
            ORDER BY updated_at DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def get_conversation(conversation_id: int) -> dict | None:
    """Return one conversation by ID."""

    with get_connection() as connection:

        row = connection.execute(
            """
            SELECT
                id,
                title,
                created_at,
                updated_at
            FROM conversations
            WHERE id = ?
            """,
            (conversation_id,),
        ).fetchone()

    return dict(row) if row else None


def update_conversation_title(
    conversation_id: int,
    title: str,
) -> None:
    """Update the title of a conversation."""

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE conversations
            SET
                title = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (title, now, conversation_id),
        )

        connection.commit()


def delete_conversation(conversation_id: int) -> None:
    """Delete a conversation and its messages."""

    with get_connection() as connection:

        connection.execute(
            """
            DELETE FROM messages
            WHERE conversation_id = ?
            """,
            (conversation_id,),
        )

        connection.execute(
            """
            DELETE FROM conversations
            WHERE id = ?
            """,
            (conversation_id,),
        )

        connection.commit()


# =========================================================
# MESSAGES
# =========================================================

def add_message(
    conversation_id: int,
    role: str,
    content: str,
) -> None:
    """Save a message inside a conversation."""

    now = datetime.now().isoformat(timespec="seconds")

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO messages (
                conversation_id,
                role,
                content,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                conversation_id,
                role,
                content,
                now,
            ),
        )

        connection.execute(
            """
            UPDATE conversations
            SET updated_at = ?
            WHERE id = ?
            """,
            (
                now,
                conversation_id,
            ),
        )

        connection.commit()


def get_messages(
    conversation_id: int,
) -> list[dict]:
    """Return all messages for a conversation."""

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT
                id,
                conversation_id,
                role,
                content,
                created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            """,
            (conversation_id,),
        ).fetchall()

    return [dict(row) for row in rows]