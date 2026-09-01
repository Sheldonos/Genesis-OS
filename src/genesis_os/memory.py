from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .types import Goal, ObjectiveRecord, ObjectiveStatus


class MemoryStore:
    """Durable run, procedure, objective, provider and curiosity state."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS episodes (
                run_id TEXT, capability TEXT, provider TEXT, success INTEGER,
                score REAL, payload TEXT
            );
            CREATE TABLE IF NOT EXISTS procedures (
                signature TEXT PRIMARY KEY, successes INTEGER NOT NULL,
                procedure TEXT NOT NULL, compiled INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS objectives (
                objective_id TEXT PRIMARY KEY, objective TEXT NOT NULL,
                required_capabilities TEXT NOT NULL, domain TEXT NOT NULL,
                metadata TEXT NOT NULL, status TEXT NOT NULL,
                heartbeat_count INTEGER NOT NULL DEFAULT 0,
                last_run_id TEXT, last_error TEXT
            );
            CREATE TABLE IF NOT EXISTS curiosity (
                id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT,
                question TEXT NOT NULL, reason TEXT NOT NULL,
                priority REAL NOT NULL, resolved INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        self.conn.commit()

    def close(self) -> None:
        """Release the SQLite connection. Use as a context-manager or call explicitly."""
        self.conn.close()

    def __enter__(self) -> MemoryStore:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def remember_episode(
        self,
        run_id: str,
        capability: str,
        success: bool,
        score: float,
        payload: Any,
        provider: str = "local",
    ) -> None:
        self.conn.execute(
            "INSERT INTO episodes VALUES (?, ?, ?, ?, ?, ?)",
            (run_id, capability, provider, int(success), score, json.dumps(payload, default=str)),
        )
        self.conn.commit()

    def episodes(self, capability: str | None = None) -> list[dict[str, Any]]:
        sql = "SELECT run_id, capability, provider, success, score, payload FROM episodes"
        args: tuple[Any, ...] = ()
        if capability:
            sql += " WHERE capability=?"
            args = (capability,)
        rows = self.conn.execute(sql, args).fetchall()
        return [
            {
                "run_id": row["run_id"],
                "capability": row["capability"],
                "provider": row["provider"],
                "success": bool(row["success"]),
                "score": row["score"],
                "payload": json.loads(row["payload"]),
            }
            for row in rows
        ]

    def provider_stats(self, capability: str, provider: str) -> dict[str, float]:
        row = self.conn.execute(
            """
            SELECT COUNT(*) AS attempts, COALESCE(AVG(success), 0) AS success_rate,
                   COALESCE(AVG(score), 0) AS avg_score
            FROM episodes WHERE capability=? AND provider=?
            """,
            (capability, provider),
        ).fetchone()
        return {
            "attempts": float(row["attempts"]),
            "success_rate": float(row["success_rate"]),
            "avg_score": float(row["avg_score"]),
        }

    def record_procedure_success(self, signature: str, procedure: list[str]) -> int:
        """Increment success counter. The procedure steps are set only on first insert
        so the compiled canonical form is always the first-observed successful plan."""
        row = self.conn.execute(
            "SELECT successes FROM procedures WHERE signature=?", (signature,)
        ).fetchone()
        if row:
            successes = int(row["successes"]) + 1
            self.conn.execute(
                "UPDATE procedures SET successes=? WHERE signature=?",
                (successes, signature),
            )
        else:
            successes = 1
            self.conn.execute(
                "INSERT INTO procedures(signature, successes, procedure, compiled) "
                "VALUES (?, ?, ?, 0)",
                (signature, successes, json.dumps(procedure)),
            )
        self.conn.commit()
        return successes

    def compile_procedure(self, signature: str) -> None:
        self.conn.execute("UPDATE procedures SET compiled=1 WHERE signature=?", (signature,))
        self.conn.commit()

    def procedure(self, signature: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT successes, procedure, compiled FROM procedures WHERE signature=?",
            (signature,),
        ).fetchone()
        if not row:
            return None
        return {
            "successes": int(row["successes"]),
            "steps": json.loads(row["procedure"]),
            "compiled": bool(row["compiled"]),
        }

    def save_objective(self, record: ObjectiveRecord) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO objectives(
                objective_id, objective, required_capabilities, domain, metadata,
                status, heartbeat_count, last_run_id, last_error
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.objective_id,
                record.goal.objective,
                json.dumps(record.goal.required_capabilities),
                record.goal.domain,
                json.dumps(record.goal.metadata, default=str),
                record.status.value,
                record.heartbeat_count,
                record.last_run_id,
                record.last_error,
            ),
        )
        self.conn.commit()

    def load_objective(self, objective_id: str) -> ObjectiveRecord | None:
        row = self.conn.execute(
            "SELECT * FROM objectives WHERE objective_id=?", (objective_id,)
        ).fetchone()
        if not row:
            return None
        return ObjectiveRecord(
            objective_id=row["objective_id"],
            goal=Goal(
                objective=row["objective"],
                required_capabilities=tuple(json.loads(row["required_capabilities"])),
                domain=row["domain"],
                metadata=json.loads(row["metadata"]),
            ),
            status=ObjectiveStatus(row["status"]),
            heartbeat_count=int(row["heartbeat_count"]),
            last_run_id=row["last_run_id"],
            last_error=row["last_error"],
        )

    def add_curiosity(
        self,
        run_id: str | None,
        question: str,
        reason: str,
        priority: float,
    ) -> None:
        self.conn.execute(
            "INSERT INTO curiosity(run_id, question, reason, priority, resolved) "
            "VALUES (?, ?, ?, ?, 0)",
            (run_id, question, reason, priority),
        )
        self.conn.commit()

    def curiosity(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT run_id, question, reason, priority, resolved "
            "FROM curiosity ORDER BY priority DESC"
        ).fetchall()
        return [dict(row) for row in rows]
