import sqlite3
from contextlib import contextmanager

DB_PATH = "counter.db"


def initialize_db(db_path: str = DB_PATH) -> None:
    """
    Creates the database tables if they don't already exist.
    """
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS counters (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT    NOT NULL UNIQUE,
                value   INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                counter_id  INTEGER NOT NULL REFERENCES counters(id),
                operation   TEXT    NOT NULL,
                value_after INTEGER NOT NULL,
                occurred_at TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)


@contextmanager
def get_connection(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
