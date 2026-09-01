from __future__ import annotations

from dataclasses import dataclass

from .registry import CapabilityRegistry
from .types import Goal


@dataclass(frozen=True)
class Plan:
    steps: tuple[str, ...]


class Planner:
    """Dependency-aware capability planner with cycle detection."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry

    def build(self, goal: Goal) -> Plan:
        ordered: list[str] = []
        visited: set[str] = set()
        active: set[str] = set()

        def visit(name: str) -> None:
            if name in visited:
                return
            if name in active:
                raise ValueError(f"capability dependency cycle at {name}")
            active.add(name)
            manifest = self.registry.manifest(name)
            for dep in manifest.requires:
                visit(dep)
            active.remove(name)
            visited.add(name)
            ordered.append(name)

        for capability in goal.required_capabilities:
            visit(capability)
        return Plan(tuple(ordered))
