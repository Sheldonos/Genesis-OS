from genesis_os.acquisition import CapabilityAcquirer
from genesis_os.catalog import demo_registry, objective_demo_source
from genesis_os.memory import MemoryStore
from genesis_os.objectives import ObjectiveEngine
from genesis_os.runtime import GenesisRuntime
from genesis_os.types import Goal
from genesis_os.world import WorldModel


def test_objective_heartbeat_acquires_compiles_and_reuses():
    registry = demo_registry()
    memory = MemoryStore()
    runtime = GenesisRuntime(
        registry,
        memory=memory,
        acquirer=CapabilityAcquirer(registry, [objective_demo_source()]),
    )
    world = WorldModel()
    engine = ObjectiveEngine(runtime, memory, world)
    record = engine.create(
        Goal(
            "learn signal analysis",
            ("analyze.signal",),
            metadata={"event": {"kind": "signal"}},
        )
    )

    first = engine.heartbeat(record.objective_id)
    second = engine.heartbeat(record.objective_id)
    third = engine.heartbeat(record.objective_id)

    assert first.metadata["acquired_capabilities"] == ["analyze.signal"]
    assert second.metadata["procedure_compiled"]
    assert third.metadata["procedure_reused"]
    assert memory.load_objective(record.objective_id).heartbeat_count == 3
    assert world.neighbors(record.objective_id)
