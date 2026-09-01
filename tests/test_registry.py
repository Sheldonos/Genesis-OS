import pytest

from genesis_os.registry import CapabilityRegistry
from genesis_os.types import CapabilityManifest


def test_registry_rejects_duplicate_names():
    registry = CapabilityRegistry()
    manifest = CapabilityManifest(name="x", description="test")
    registry.register(manifest, lambda _: True)
    with pytest.raises(ValueError):
        registry.register(manifest, lambda _: False)


def test_discovery_scores_matching_capabilities():
    registry = CapabilityRegistry()
    manifest = CapabilityManifest(
        name="browser.navigate",
        description="navigate a browser",
        tags=("web",),
    )
    registry.register(manifest, lambda _: 1)
    assert registry.discover("browser web")[0].name == "browser.navigate"
