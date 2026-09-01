from genesis_os.memory import MemoryStore
from genesis_os.registry import CapabilityRegistry
from genesis_os.routing import ProviderRouter
from genesis_os.types import CapabilityManifest


def test_router_prefers_provider_with_better_observed_outcomes():
    registry = CapabilityRegistry()
    registry.register(
        CapabilityManifest(name="cap", description="cap", provider="a"),
        lambda _: "a",
    )
    registry.register(
        CapabilityManifest(name="cap", description="cap", provider="b"),
        lambda _: "b",
    )
    memory = MemoryStore()
    memory.remember_episode("1", "cap", False, 0.0, {}, provider="a")
    memory.remember_episode("2", "cap", True, 1.0, {}, provider="b")
    assert ProviderRouter(registry, memory).choose("cap").manifest.provider == "b"
