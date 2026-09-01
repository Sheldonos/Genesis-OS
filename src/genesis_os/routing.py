from __future__ import annotations

from dataclasses import dataclass

from .memory import MemoryStore
from .registry import CapabilityRegistry
from .types import CapabilityManifest


@dataclass(frozen=True)
class RouteDecision:
    manifest: CapabilityManifest
    score: float


class ProviderRouter:
    """Ranks interchangeable providers using outcomes, cost and latency."""

    def __init__(self, registry: CapabilityRegistry, memory: MemoryStore) -> None:
        self.registry = registry
        self.memory = memory

    def choose(self, capability: str) -> RouteDecision:
        candidates = self.registry.providers(capability)
        scored: list[RouteDecision] = []
        for manifest in candidates:
            stats = self.memory.provider_stats(capability, manifest.provider)
            reliability = stats["avg_score"] if stats["attempts"] else 0.75
            cost_penalty = min(max(manifest.cost, 0.0), 1.0) * 0.10
            latency_penalty = min(max(manifest.latency_ms, 0.0) / 10_000.0, 1.0) * 0.10
            score = reliability - cost_penalty - latency_penalty
            scored.append(RouteDecision(manifest, score))
        return max(scored, key=lambda item: (item.score, item.manifest.provider))
