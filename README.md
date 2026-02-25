# py-counter

A simple counter application built with Python, SQLite, FastAPI, and HTMX. Supports both a CLI and a web interface, with full operation history persisted to a local database.

---

## Features

- Increment, decrement, and reset a named counter
- Persistent state via SQLite — counter survives restarts
- Full operation history with timestamps
- Web UI powered by FastAPI and HTMX (no page reloads)
- CLI interface for terminal use
- Test-driven development throughout

---

## Project Structure

```
py-counter/
├── app/
│   ├── __init__.py
│   ├── api.py          # FastAPI app and route definitions
│   ├── counter.py      # Counter class with database persistence
│   ├── database.py     # SQLite connection management and schema
│   └── templates/
│       ├── index.html  # Full page template
│       └── counter.html # HTMX fragment returned on each action
├── tests/
│   ├── test_api.py
│   ├── test_counter.py
│   └── test_database.py
├── main.py             # CLI entry point
├── pyproject.toml
└── README.md
```

---

## Installation

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/ccentola/py-counter.git
cd py-counter
uv sync --all-groups
```

---

## Usage

### Web

Start the development server:

```bash
uv run uvicorn app.api:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser. Use the `+` and `-` buttons to increment and decrement the counter, and the reset icon to return it to zero.

### CLI

```bash
uv run python main.py
```

Available commands at the prompt:

| Command | Action |
|---------|--------|
| `i` | Increment |
| `d` | Decrement |
| `r` | Reset to 0 |
| `quit` | Exit |

---

## Running Tests

```bash
uv run pytest
```

---

## Architecture

### Separation of concerns

The application is split into three distinct layers:

- **`database.py`** — manages the SQLite connection lifecycle. The `get_connection` context manager handles commits, rollbacks, and connection cleanup automatically. Schema initialization is idempotent and safe to call on every startup.

- **`counter.py`** — the `Counter` class encapsulates all counter logic. State is never held in memory — `value` and `history` are properties that read directly from the database on every access, ensuring consistency. Mutations (`increment`, `decrement`, `reset`) use atomic SQL operations and log to an `events` table in the same transaction.

- **`api.py`** — FastAPI routes that sit on top of the counter layer. Uses dependency injection (`get_db`) to supply the database path, which makes the routes fully testable without touching the real database.

### HTMX

The web UI avoids JavaScript by using HTMX. Each button POSTs to a FastAPI route which returns a small HTML fragment (`counter.html`). HTMX swaps the fragment into the page in place, giving the feel of a dynamic app without a frontend framework or a full page reload.

### Testing

All three layers have isolated test suites. Database tests use temporary `.db` files cleaned up after each test. API tests use FastAPI's `TestClient` with dependency overrides to inject a test database. This means no test ever touches the real `counter.db`.

### Database schema

```sql
CREATE TABLE counters (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL UNIQUE,
    value   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    counter_id  INTEGER NOT NULL REFERENCES counters(id),
    operation   TEXT    NOT NULL,
    value_after INTEGER NOT NULL,
    occurred_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

The `counters` table supports multiple named counters. The `events` table provides a full audit log of every operation with a timestamp written at the database level.
