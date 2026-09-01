from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class WorldModel:
    """Small structured world graph: entities plus typed relationships."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS entities (
                entity_id TEXT PRIMARY KEY, kind TEXT NOT NULL, state TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS relations (
                source TEXT NOT NULL, relation TEXT NOT NULL, target TEXT NOT NULL,
                metadata TEXT NOT NULL,
                PRIMARY KEY(source, relation, target)
            );
            """
        )
        self.conn.commit()

    def close(self) -> None:
        """Release the SQLite connection. Use as a context-manager or call explicitly."""
        self.conn.close()

    def __enter__(self) -> WorldModel:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def upsert_entity(self, entity_id: str, kind: str, state: dict[str, Any] | None = None) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO entities(entity_id, kind, state) VALUES (?, ?, ?)",
            (entity_id, kind, json.dumps(state or {}, default=str)),
        )
        self.conn.commit()

    def entity(self, entity_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT entity_id, kind, state FROM entities WHERE entity_id=?", (entity_id,)
        ).fetchone()
        if not row:
            return None
        return {
            "entity_id": row["entity_id"],
            "kind": row["kind"],
            "state": json.loads(row["state"]),
        }

    def link(
        self,
        source: str,
        relation: str,
        target: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO relations VALUES (?, ?, ?, ?)",
            (source, relation, target, json.dumps(metadata or {}, default=str)),
        )
        self.conn.commit()

    def neighbors(self, entity_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT source, relation, target, metadata FROM relations WHERE source=? OR target=?",
            (entity_id, entity_id),
        ).fetchall()
        return [
            {
                "source": row["source"],
                "relation": row["relation"],
                "target": row["target"],
                "metadata": json.loads(row["metadata"]),
            }
            for row in rows
        ]
