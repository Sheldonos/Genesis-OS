from __future__ import annotations

import json
from pathlib import Path

from .acquisition import StaticCapabilitySource
from .registry import CapabilityRegistry
from .types import AcquiredCapability, CapabilityManifest, RiskTier


def load_manifest(path: str | Path) -> CapabilityManifest:
    """Load a CapabilityManifest from a JSON file.

    Raises:
        ValueError: if required fields are missing or the risk tier is invalid.
    """
    raw = json.loads(Path(path).read_text())
    try:
        return CapabilityManifest(
            name=raw["name"],
            description=raw["description"],
            tags=tuple(raw.get("tags", [])),
            risk=RiskTier[raw.get("risk", "LOW")],
            requires=tuple(raw.get("requires", [])),
            permissions=tuple(raw.get("permissions", [])),
            domains=tuple(raw.get("domains", [])),
            provider=raw.get("provider", "local"),
            learnable=bool(raw.get("learnable", True)),
            version=str(raw.get("version", "1")),
            cost=float(raw.get("cost", 0.0)),
            latency_ms=float(raw.get("latency_ms", 0.0)),
        )
    except KeyError as exc:
        raise ValueError(f"invalid manifest at {path}: missing or invalid field {exc}") from exc


def demo_registry() -> CapabilityRegistry:
    registry = CapabilityRegistry()
    registry.register(
        CapabilityManifest(
            name="sense.local_event",
            description="Observe a structured local event supplied to the run",
            tags=("sensor", "observation"),
            risk=RiskTier.READ_ONLY,
        ),
        lambda state: state.get("event", {"status": "no-event"}),
    )
    registry.register(
        CapabilityManifest(
            name="analyze.event",
            description="Create a deterministic analysis record from an observed event",
            tags=("analysis", "reasoning"),
            requires=("sense.local_event",),
            risk=RiskTier.READ_ONLY,
        ),
        lambda state: {"analysis": state["sense.local_event"], "confidence": 1.0},
    )
    registry.register(
        CapabilityManifest(
            name="act.record_decision",
            description="Record a low-risk decision artifact",
            tags=("action", "audit"),
            requires=("analyze.event",),
            permissions=("write_artifact",),
            risk=RiskTier.LOW,
        ),
        lambda state: {"decision": "recorded", "basis": state["analyze.event"]},
    )
    return registry


def objective_demo_source() -> StaticCapabilitySource:
    candidate = AcquiredCapability(
        manifest=CapabilityManifest(
            name="analyze.signal",
            description=(
                "Analyze a structured signal acquired from a trusted local capability source"
            ),
            tags=("analysis", "acquired"),
            requires=("sense.local_event",),
            risk=RiskTier.READ_ONLY,
            provider="trusted-catalog",
        ),
        handler=lambda state: {
            "signal": state["sense.local_event"],
            "finding": "novel pattern detected",
        },
        source="trusted-demo-catalog",
        verified=True,
        trust_score=1.0,
    )
    return StaticCapabilitySource([candidate])
