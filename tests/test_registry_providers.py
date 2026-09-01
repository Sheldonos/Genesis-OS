from genesis_os.registry import CapabilityRegistry
from genesis_os.types import CapabilityManifest


def test_registry_supports_multiple_providers_per_capability():
    registry = CapabilityRegistry()
    registry.register(
        CapabilityManifest(name="x", description="x", provider="one"),
        lambda _: 1,
    )
    registry.register(
        CapabilityManifest(name="x", description="x", provider="two"),
        lambda _: 2,
    )
    assert {manifest.provider for manifest in registry.providers("x")} == {"one", "two"}
