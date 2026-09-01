from genesis_os.catalog import demo_registry
from genesis_os.runtime import GenesisRuntime
from genesis_os.types import ExecutionContext, Goal


def test_end_to_end_demo_succeeds():
    runtime = GenesisRuntime(demo_registry())
    goal = Goal(
        "test",
        ("act.record_decision",),
        metadata={"event": {"kind": "test"}},
    )
    context = ExecutionContext(approved_permissions={"write_artifact"})
    result = runtime.run(goal, context)
    assert result.success
    assert [step.capability for step in result.steps] == [
        "sense.local_event",
        "analyze.event",
        "act.record_decision",
    ]


def test_runtime_stops_on_policy_denial():
    runtime = GenesisRuntime(demo_registry())
    goal = Goal(
        "test",
        ("act.record_decision",),
        metadata={"event": {"kind": "test"}},
    )
    result = runtime.run(goal, ExecutionContext())
    assert not result.success
    assert result.steps[-1].error.startswith("missing permissions")
