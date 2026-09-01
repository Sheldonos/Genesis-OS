from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from .registry import CapabilityRegistry
from .types import AcquiredCapability, RiskTier


class CapabilitySource(Protocol):
    def discover(self, capability: str, domain: str) -> Iterable[AcquiredCapability]: ...


class CapabilityAcquirer:
    """Registers only verified adapters from explicit trusted sources."""

    def __init__(
        self,
        registry: CapabilityRegistry,
        sources: Iterable[CapabilitySource] = (),
    ) -> None:
        self.registry = registry
        self.sources = list(sources)

    def acquire(self, capability: str, domain: str = "general") -> list[AcquiredCapability]:
        accepted: list[AcquiredCapability] = []
        for source in self.sources:
            for candidate in source.discover(capability, domain):
                manifest = candidate.manifest
                if manifest.name != capability or not candidate.verified:
                    continue
                if candidate.trust_score < 0.8:
                    continue
                if manifest.risk >= RiskTier.CRITICAL or "offensive-security" in manifest.tags:
                    continue
                try:
                    self.registry.register(manifest, candidate.handler)
                except ValueError:
                    continue
                accepted.append(candidate)
        return accepted


class StaticCapabilitySource:
    """Deterministic source for tests/examples and trusted local catalogs."""

    def __init__(self, capabilities: Iterable[AcquiredCapability]) -> None:
        self.capabilities = list(capabilities)

    def discover(self, capability: str, domain: str) -> Iterable[AcquiredCapability]:
        del domain
        return [c for c in self.capabilities if c.manifest.name == capability]
