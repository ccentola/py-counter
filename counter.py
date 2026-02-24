from database import get_connection


class Counter:
    def __init__(self, name: str, db_path: str) -> None:
        self.name = name
        self._db_path = db_path
        with get_connection(self._db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO counters (name, value) VALUES (?, 0)",
                (self.name,),
            )

    @property
    def value(self) -> int:
        with get_connection(self._db_path) as conn:
            row = conn.execute(
                "SELECT value FROM counters WHERE name = ?", (self.name,)
            ).fetchone()
        return row["value"]

    @property
    def history(self) -> list:
        with get_connection(self._db_path) as conn:
            rows = conn.execute(
                """
                SELECT e.operation, e.value_after, e.occurred_at
                FROM events e
                JOIN counters c ON c.id = e.counter_id
                WHERE c.name = ?
                ORDER BY e.id ASC
                """,
                (self.name,),
            ).fetchall()
        return [dict(row) for row in rows]

    def increment(self) -> None:
        """Adds 1 to the current value"""
        with get_connection(self._db_path) as conn:
            conn.execute(
                "UPDATE counters SET value = value + 1 WHERE name = ?",
                (self.name,),
            )
            conn.execute(
                """
                INSERT INTO events (counter_id, operation, value_after)
                SELECT id, 'increment', value FROM counters WHERE name = ?
                """,
                (self.name,),
            )

    def decrement(self) -> None:
        """
        Subtracts 1 from the current value.

        Raises:
            ValueError: If the current value is 0, to prevent negative counts.
        """
        if self.value <= 0:
            raise ValueError("Counter cannot be negative")
        with get_connection(self._db_path) as conn:
            conn.execute(
                "UPDATE counters SET value = value - 1 WHERE name = ?",
                (self.name,),
            )
            conn.execute(
                """
                INSERT INTO events (counter_id, operation, value_after)
                SELECT id, 'decrement', value FROM counters WHERE name = ?
                """,
                (self.name,),
            )

    def reset(self) -> None:
        """Resets the current counter to 0"""
        with get_connection(self._db_path) as conn:
            conn.execute(
                "UPDATE counters SET value = 0 WHERE name = ?",
                (self.name,),
            )
            conn.execute(
                """
                INSERT INTO events (counter_id, operation, value_after)
                SELECT id, 'reset', value FROM counters WHERE name = ?
                """,
                (self.name,),
            )

    def __str__(self) -> str:
        return str(self.value)
