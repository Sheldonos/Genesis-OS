from __future__ import annotations

import argparse
import json

from .acquisition import CapabilityAcquirer
from .catalog import demo_registry, objective_demo_source
from .memory import MemoryStore
from .objectives import ObjectiveEngine
from .runtime import GenesisRuntime
from .types import ExecutionContext, Goal
from .world import WorldModel


def _result_payload(result):
    return {
        "run_id": result.run_id,
        "success": result.success,
        "metadata": result.metadata,
        "steps": [step.__dict__ for step in result.steps],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="genesis",
        description="Genesis OS reference runtime",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("capabilities")
    demo = sub.add_parser("demo")
    demo.add_argument("--event", default='{"kind":"market-shift","severity":2}')
    objective_demo = sub.add_parser("objective-demo")
    objective_demo.add_argument("--heartbeats", type=int, default=3)
    args = parser.parse_args()

    registry = demo_registry()
    if args.command == "capabilities":
        print("\n".join(registry.names()))
        return

    if args.command == "demo":
        runtime = GenesisRuntime(registry)
        goal = Goal(
            objective="Observe, analyze, and record a low-risk event",
            required_capabilities=("act.record_decision",),
            metadata={"event": json.loads(args.event)},
        )
        result = runtime.run(
            goal,
            ExecutionContext(approved_permissions={"write_artifact"}),
        )
        print(json.dumps(_result_payload(result), indent=2, default=str))
        return

    memory = MemoryStore()
    acquirer = CapabilityAcquirer(registry, [objective_demo_source()])
    runtime = GenesisRuntime(registry, memory=memory, acquirer=acquirer)
    world = WorldModel()
    objectives = ObjectiveEngine(runtime, memory, world)
    record = objectives.create(
        Goal(
            objective="Continuously inspect a signal and learn a reusable analysis procedure",
            required_capabilities=("analyze.signal",),
            metadata={"event": {"kind": "new-domain-signal", "value": 7}},
        )
    )
    runs = []
    for _ in range(max(args.heartbeats, 1)):
        runs.append(_result_payload(objectives.heartbeat(record.objective_id)))
    current = memory.load_objective(record.objective_id)
    print(
        json.dumps(
            {
                "objective_id": record.objective_id,
                "objective": current.__dict__ if current else None,
                "runs": runs,
                "world": world.entity(record.objective_id),
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
