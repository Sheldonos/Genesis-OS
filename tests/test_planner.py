import pytest

from genesis_os.planner import Planner
from genesis_os.registry import CapabilityRegistry
from genesis_os.types import CapabilityManifest, Goal


def test_planner_orders_dependencies():
    registry = CapabilityRegistry()
    registry.register(CapabilityManifest(name="a", description="a"), lambda _: 1)
    registry.register(CapabilityManifest(name="b", description="b", requires=("a",)), lambda _: 2)
    plan = Planner(registry).build(Goal("goal", ("b",)))
    assert plan.steps == ("a", "b")


def test_planner_detects_cycles():
    registry = CapabilityRegistry()
    registry.register(CapabilityManifest(name="a", description="a", requires=("b",)), lambda _: 1)
    registry.register(CapabilityManifest(name="b", description="b", requires=("a",)), lambda _: 2)
    with pytest.raises(ValueError):
        Planner(registry).build(Goal("goal", ("a",)))
