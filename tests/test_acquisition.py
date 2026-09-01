from genesis_os.acquisition import CapabilityAcquirer, StaticCapabilitySource
from genesis_os.registry import CapabilityRegistry
from genesis_os.types import AcquiredCapability, CapabilityManifest, RiskTier


def test_acquirer_registers_verified_trusted_capability():
    registry = CapabilityRegistry()
    candidate = AcquiredCapability(
        CapabilityManifest(name="new.cap", description="new", provider="trusted"),
        lambda _: 7,
        source="catalog",
        verified=True,
        trust_score=0.95,
    )
    acquirer = CapabilityAcquirer(registry, [StaticCapabilitySource([candidate])])
    assert acquirer.acquire("new.cap")
    assert registry.handler("new.cap", "trusted")({}) == 7


def test_acquirer_rejects_critical_or_unverified_capability():
    registry = CapabilityRegistry()
    critical = AcquiredCapability(
        CapabilityManifest(name="danger", description="danger", risk=RiskTier.CRITICAL),
        lambda _: True,
        source="catalog",
        verified=True,
        trust_score=1.0,
    )
    unverified = AcquiredCapability(
        CapabilityManifest(name="maybe", description="maybe"),
        lambda _: True,
        source="catalog",
        verified=False,
        trust_score=1.0,
    )
    acquirer = CapabilityAcquirer(
        registry,
        [StaticCapabilitySource([critical, unverified])],
    )
    assert not acquirer.acquire("danger")
    assert not acquirer.acquire("maybe")
