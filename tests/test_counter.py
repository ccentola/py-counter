import os
import pytest
from app.database import initialize_db, get_connection
from app.counter import Counter
from main import run

DB = "test_counter.db"


@pytest.fixture(autouse=True)
def fresh_db():
    """Give every test a clean, initialized database."""
    initialize_db(DB)
    yield
    if os.path.exists(DB):
        os.remove(DB)


# UNIT TESTS: instantiation ====================================================
def test_creates_counter_with_default_value():
    c = Counter("steps", DB)
    assert c.value == 0


def test_returns_existing_counter():
    Counter("steps", DB)
    with get_connection(DB) as conn:
        conn.execute("UPDATE counters SET value = 5 WHERE name = 'steps'")
    c = Counter("steps", DB)
    assert c.value == 5


def test_different_counters_are_independent():
    steps = Counter("steps", DB)
    pushups = Counter("pushups", DB)
    steps.increment()
    steps.increment()
    steps.increment()
    assert steps.value == 3
    assert pushups.value == 0


# UNIT TESTS: increment ========================================================
def test_increment_increases_value_by_one():
    c = Counter("default", DB)
    c.increment()
    assert c.value == 1


def test_increment_multiple_times():
    c = Counter("default", DB)
    c.increment()
    c.increment()
    c.increment()
    assert c.value == 3


def test_increment_logs_event():
    c = Counter("default", DB)
    c.increment()
    assert len(c.history) == 1
    assert c.history[0]["operation"] == "increment"
    assert c.history[0]["value_after"] == 1


# UNIT TESTS: decrement ========================================================
def test_decrement_decreases_value_by_one():
    c = Counter("default", DB)
    c.increment()
    c.decrement()
    assert c.value == 0


def test_decrement_raises_when_at_zero():
    c = Counter("default", DB)
    with pytest.raises(ValueError, match="Counter cannot be negative"):
        c.decrement()


def test_decrement_does_not_log_event_on_error():
    c = Counter("default", DB)
    try:
        c.decrement()
    except ValueError:
        pass
    assert len(c.history) == 0


def test_decrement_logs_event_on_success():
    c = Counter("default", DB)
    c.increment()
    c.decrement()
    assert c.history[-1]["operation"] == "decrement"
    assert c.history[-1]["value_after"] == 0


# UNIT TESTS: reset ============================================================
def test_reset_sets_value_to_zero():
    c = Counter("default", DB)
    c.increment()
    c.increment()
    c.reset()
    assert c.value == 0


def test_reset_logs_event():
    c = Counter("default", DB)
    c.increment()
    c.reset()
    assert c.history[-1]["operation"] == "reset"
    assert c.history[-1]["value_after"] == 0


# UNIT TESTS: history ==========================================================
def test_history_is_ordered_oldest_first():
    c = Counter("default", DB)
    c.increment()
    c.increment()
    c.decrement()
    operations = [row["operation"] for row in c.history]
    assert operations == ["increment", "increment", "decrement"]


def test_history_includes_occurred_at_timestamp():
    c = Counter("default", DB)
    c.increment()
    assert "occurred_at" in c.history[0].keys()


def test_history_is_empty_for_new_counter():
    c = Counter("default", DB)
    assert c.history == []


def test_history_is_scoped_to_counter():
    steps = Counter("steps", DB)
    pushups = Counter("pushups", DB)
    steps.increment()
    steps.increment()
    pushups.increment()
    assert len(steps.history) == 2
    assert len(pushups.history) == 1


# UNIT TESTS: string representation ============================================
def test_string_representation():
    c = Counter("default", DB)
    c.increment()
    assert str(c) == "1"


# INTEGRATION TESTS: CLI =======================================================
def test_counter_flow_capture_prompt(monkeypatch):
    captured_prompts = []
    inputs = iter(["i", "i", "d", "quit"])

    def mocked_input(prompt):
        captured_prompts.append(prompt)
        return next(inputs)

    monkeypatch.setattr("builtins.input", mocked_input)
    run(db=DB)

    all_prompts = "".join(captured_prompts)
    assert "Current: 1" in all_prompts
    assert "Current: 2" in all_prompts
    assert "Current: 1" in all_prompts


def test_counter_cli_error_handling(monkeypatch, capsys):
    inputs = iter(["d", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run(db=DB)
    captured = capsys.readouterr().out

    assert "Error: Counter cannot be negative" in captured
