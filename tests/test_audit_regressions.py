"""Regression tests for findings from the v0.2.0 engineering audit."""
from __future__ import annotations

import threading

from genesis_os.catalog import demo_registry
from genesis_os.compiler import ProcedureCompiler
from genesis_os.memory import MemoryStore
from genesis_os.registry import CapabilityRegistry
from genesis_os.runtime import GenesisRuntime
from genesis_os.types import ExecutionContext, Goal
from genesis_os.world import WorldModel

# ---------------------------------------------------------------------------
# CRITICAL-01: RunResult.metadata keys are consistent on ALL exit paths
# ---------------------------------------------------------------------------

def test_metadata_keys_consistent_on_acquisition_failure():
    """Acquisition failure path must include all three metadata keys."""
    runtime = GenesisRuntime(CapabilityRegistry())
    result = runtime.run(Goal("t", ("missing",)), ExecutionContext())
    assert not result.success
    assert "acquired_capabilities" in result.metadata
    assert "procedure_reused" in result.metadata
    assert "procedure_compiled" in result.metadata


def test_metadata_keys_consistent_on_policy_denial():
    """Policy denial path must include all three metadata keys."""
    runtime = GenesisRuntime(demo_registry())
    goal = Goal("t", ("act.record_decision",), metadata={"event": {}})
    result = runtime.run(goal, ExecutionContext())  # no write_artifact permission
    assert not result.success
    assert "acquired_capabilities" in result.metadata
    assert "procedure_reused" in result.metadata
    assert "procedure_compiled" in result.metadata


def test_metadata_keys_consistent_on_success():
    """Success path must include all three metadata keys."""
    runtime = GenesisRuntime(demo_registry())
    goal = Goal("t", ("act.record_decision",), metadata={"event": {}})
    result = runtime.run(goal, ExecutionContext(approved_permissions={"write_artifact"}))
    assert result.success
    assert "acquired_capabilities" in result.metadata
    assert "procedure_reused" in result.metadata
    assert "procedure_compiled" in result.metadata


# ---------------------------------------------------------------------------
# MEDIUM-01: procedure_compiled fires exactly once (at the crossing moment)
# ---------------------------------------------------------------------------

def test_procedure_compiled_fires_exactly_once():
    """observe_success must return True only on the run that crosses the threshold."""
    memory = MemoryStore()
    compiler = ProcedureCompiler(memory, threshold=2)
    sig = compiler.signature("dom", ("a",))
    assert compiler.observe_success(sig, ("a",)) is False   # run 1: below threshold
    assert compiler.observe_success(sig, ("a",)) is True    # run 2: crossing
    assert compiler.observe_success(sig, ("a",)) is False   # run 3: already compiled


# ---------------------------------------------------------------------------
# MEDIUM-02: Compiled procedure steps are frozen at first success
# ---------------------------------------------------------------------------

def test_compiled_steps_frozen_at_first_success():
    """Steps written on the first run must not be overwritten by later runs."""
    memory = MemoryStore()
    compiler = ProcedureCompiler(memory, threshold=2)
    sig = compiler.signature("dom", ("a", "b"))
    compiler.observe_success(sig, ("a", "b"))
    compiler.observe_success(sig, ("a", "b", "c"))  # different steps — must be ignored
    assert compiler.compiled_steps(sig) == ("a", "b")


# ---------------------------------------------------------------------------
# MEDIUM-04: SQLite connections accept cross-thread access
# ---------------------------------------------------------------------------

def test_memory_store_is_accessible_from_thread():
    memory = MemoryStore()
    errors: list[str] = []

    def write() -> None:
        try:
            memory.remember_episode("r_t", "cap", True, 1.0, {})
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    t = threading.Thread(target=write)
    t.start()
    t.join()
    assert errors == [], f"Cross-thread access failed: {errors}"


def test_world_model_is_accessible_from_thread():
    world = WorldModel()
    errors: list[str] = []

    def write() -> None:
        try:
            world.upsert_entity("t", "test", {})
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    t = threading.Thread(target=write)
    t.start()
    t.join()
    assert errors == [], f"Cross-thread access failed: {errors}"
