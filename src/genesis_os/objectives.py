from __future__ import annotations

import uuid

from .memory import MemoryStore
from .runtime import GenesisRuntime
from .types import ExecutionContext, Goal, ObjectiveRecord, ObjectiveStatus, RunResult
from .world import WorldModel


class ObjectiveEngine:
    """Persistent objective control plane with explicit heartbeats."""

    def __init__(self, runtime: GenesisRuntime, memory: MemoryStore, world: WorldModel) -> None:
        self.runtime = runtime
        self.memory = memory
        self.world = world

    def create(self, goal: Goal) -> ObjectiveRecord:
        record = ObjectiveRecord(objective_id=str(uuid.uuid4()), goal=goal)
        self.memory.save_objective(record)
        self.world.upsert_entity(
            record.objective_id,
            "objective",
            {"objective": goal.objective, "domain": goal.domain, "status": record.status.value},
        )
        return record

    def heartbeat(self, objective_id: str, context: ExecutionContext | None = None) -> RunResult:
        record = self.memory.load_objective(objective_id)
        if not record:
            raise KeyError(f"unknown objective: {objective_id}")
        if record.status not in {ObjectiveStatus.ACTIVE, ObjectiveStatus.BLOCKED}:
            raise ValueError(f"objective is not runnable: {record.status.value}")
        result = self.runtime.run(record.goal, context)
        record.heartbeat_count += 1
        record.last_run_id = result.run_id
        record.last_error = None if result.success else (result.steps[-1].error or "unknown error")
        record.status = ObjectiveStatus.ACTIVE if result.success else ObjectiveStatus.BLOCKED
        self.memory.save_objective(record)
        self.world.upsert_entity(
            objective_id,
            "objective",
            {
                "objective": record.goal.objective,
                "domain": record.goal.domain,
                "status": record.status.value,
                "heartbeat_count": record.heartbeat_count,
                "last_run_id": record.last_run_id,
            },
        )
        self.world.upsert_entity(result.run_id, "run", {"success": result.success})
        self.world.link(objective_id, "produced_run", result.run_id)
        return result
