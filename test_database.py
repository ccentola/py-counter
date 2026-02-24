import pytest
from database import initialize_db, get_connection


# UNIT TESTS ===================================================================
def test_initialize_db_creates_counters_table():
    initialize_db(":memory:")
    with get_connection(":memory:") as conn:
        result = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='counters'"
        ).fetchone()
        assert result is None


def test_initialize_db_creates_both_tables():
    db = ":memory:"
    initialize_db(db)


def test_get_connection_commits_on_success():
    """Data written inside the context manager should be readable afterward."""
    db = "test_temp.db"
    initialize_db(db)
    with get_connection(db) as conn:
        conn.execute(
            "INSERT INTO counters (name, value) VALUES (?, ?)", ("test", 42)
        )
    # Open a fresh connection to confirm the data was committed
    with get_connection(db) as conn:
        row = conn.execute(
            "SELECT value FROM counters WHERE name = ?", ("test",)
        ).fetchone()
    assert row["value"] == 42


def test_get_connection_rolls_back_on_exception():
    """Data written inside a failing block should not be persisted."""
    db = "test_temp.db"
    initialize_db(db)
    try:
        with get_connection(db) as conn:
            conn.execute(
                "INSERT INTO counters (name, value) VALUES (?, ?)",
                ("should_not_exist", 99),
            )
            raise RuntimeError("simulated failure")
    except RuntimeError:
        pass  # expected

    with get_connection(db) as conn:
        row = conn.execute(
            "SELECT value FROM counters WHERE name = ?", ("should_not_exist",)
        ).fetchone()
    assert row is None


def test_get_connection_raises_original_exception():
    """The context manager should re-raise, not swallow, exceptions."""
    db = "test_temp.db"
    initialize_db(db)
    with pytest.raises(RuntimeError, match="simulated failure"):
        with get_connection(db):
            raise RuntimeError("simulated failure")


def test_row_factory_allows_column_name_access():
    """Rows should be accessible by column name, not just index."""
    db = "test_temp.db"
    initialize_db(db)
    with get_connection(db) as conn:
        conn.execute(
            "INSERT INTO counters (name, value) VALUES (?, ?)", ("named", 7)
        )
        row = conn.execute(
            "SELECT name, value FROM counters WHERE name = ?", ("named",)
        ).fetchone()
    assert row["name"] == "named"
    assert row["value"] == 7


# INTEGRATION TESTS ============================================================
def test_initialize_db_creates_tables():
    """
    Uses a real temp file so we can verify schema across connections.
    The fixture below handles cleanup.
    """
    db = "test_schema.db"
    initialize_db(db)
    with get_connection(db) as conn:
        tables = {
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    assert "counters" in tables
    assert "events" in tables


def test_initialize_db_is_idempotent():
    """Calling initialize_db twice should not raise or wipe data."""
    db = "test_schema.db"
    initialize_db(db)
    with get_connection(db) as conn:
        conn.execute(
            "INSERT INTO counters (name, value) VALUES (?, ?)",
            ("idempotent", 1),
        )
    initialize_db(db)
    with get_connection(db) as conn:
        row = conn.execute(
            "SELECT value FROM counters WHERE name = ?", ("idempotent",)
        ).fetchone()
    assert row["value"] == 1


# CLEANUP ======================================================================
@pytest.fixture(autouse=True)
def cleanup_test_dbs():
    """Remove temp database files after each test."""
    yield
    import os

    for db_file in ["test_temp.db", "test_schema.db"]:
        if os.path.exists(db_file):
            os.remove(db_file)
