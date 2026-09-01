# Genesis OS

[![CI](https://github.com/Sheldonos/genesis-os/actions/workflows/ci.yml/badge.svg)](https://github.com/Sheldonos/genesis-os/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-informational)](pyproject.toml)

**A policy-governed capability operating system for persistent, composable autonomous intelligence.**

Genesis OS is a Python kernel that turns long-lived objectives into auditable execution graphs. It acquires missing trusted capabilities, routes work across interchangeable providers, persists objective and world state across runs, learns from outcomes, and promotes repeated successful plans into reusable procedures — all through a single policy boundary.

> **Design thesis:** The system should resemble an operating system more than a chatbot framework. Models are processors. Agents are ephemeral processes. Capabilities are syscalls. Memory is a hierarchy. Policy is the kernel security boundary.

---

## Why this is different

Most agent systems stop at `model → tools → actions`. Genesis owns the layer above:

```text
Persistent Objective
      │
      ▼
Capability Graph ──── missing? ──▶ Trusted Capability Acquisition
      │                                      │
      ▼                                      ▼
Provider Router ◀──────── outcome history / cost / latency
      │
      ▼
Central Policy Gate
      │
      ▼
Execution → Evaluation → Episodic Memory
      │                         │
      ▼                         ▼
World Model              Procedure Compiler
      │                         │
      └────── Learning / Curiosity ◀────────┘
                    │
                    ▼
              next heartbeat
```

Agents, models, skills, browsers, sandboxes, APIs, humans, and machines are all **replaceable capability providers**. Genesis keeps the durable objective, policy, memory, learning, and capability-selection state — not the providers.

---

## Quick start

```bash
# install with dev dependencies
pip install -e '.[dev]'

# run the test suite (25 tests)
pytest -q

# basic 3-step capability demo
genesis demo

# 3-heartbeat objective demo: acquire → compile → reuse
genesis objective-demo
```

Expected output from `objective-demo`:

```
heartbeat 1: acquired_capabilities=["analyze.signal"], procedure_reused=false
heartbeat 2: procedure_compiled=true, procedure_reused=false
heartbeat 3: procedure_compiled=false, procedure_reused=true
```

---

## v0.2 runtime — what is implemented

| Feature | Module | Description |
|---|---|---|
| **Persistent objectives** | `objectives.py` | Objectives survive individual runs; advanced through explicit heartbeats |
| **Structured world model** | `world.py` | SQLite entity/relation graph holds durable state outside prompt context |
| **Safe capability acquisition** | `acquisition.py` | Registers only verified adapters with trust ≥ 0.8; rejects critical-risk and offensive-security candidates |
| **Provider routing** | `routing.py` | Multiple providers per capability; ranked by observed reliability minus cost and latency penalties |
| **Procedure compilation** | `compiler.py` | Repeatedly successful plans promoted to reusable deterministic procedures after N successes |
| **Learning / curiosity signals** | `learning.py` | Failures and weak outcomes generate stored questions for future investigation |
| **Central policy gate** | `policy.py` | Every execution crosses one gate; providers cannot override a denial |
| **Dependency planner** | `planner.py` | Topological sort of capability DAG with cycle detection |
| **Episodic memory** | `memory.py` | Per-provider run history, procedure store, objective state, curiosity log |
| **Evaluator** | `evaluator.py` | Outcome scoring per step; feeds routing and learning |
| **CLI** | `cli.py` | `genesis demo`, `genesis objective-demo`, `genesis capabilities` |

---

## Capability contract

A capability describes the logical operation independently of which provider performs it:

```json
{
  "name": "browser.navigate",
  "description": "Navigate an approved browser session",
  "tags": ["browser", "computer-use"],
  "risk": "MEDIUM",
  "permissions": ["browser_use"],
  "provider": "browser-use",
  "cost": 0.02,
  "latency_ms": 800
}
```

Multiple providers can register the same `name`. The router selects among them using observed outcomes, cost, and latency. Providers are swappable without changing the objective or policy.

---

## Runtime loop

On each heartbeat the runtime:

1. Loads the persistent objective.
2. Checks for a compiled procedure and reuses it if available.
3. Otherwise resolves the dependency graph (topological sort).
4. Attempts to acquire any missing capabilities from configured trusted sources.
5. Routes each capability to a provider via the outcome-aware router.
6. Authorises the selected provider through the policy gate.
7. Executes and evaluates each step; stores episodes.
8. Promotes the plan to a compiled procedure when the success threshold is reached.
9. Updates objective and world-model state.
10. Converts failures and weak scores into curiosity signals.

---

## Safety boundaries

Genesis is designed for long-running autonomy without making the base runtime unrestricted.

| Hard stop | Default |
|---|---|
| `CRITICAL`-risk capabilities | Always denied |
| `offensive-security` tagged capabilities | Always denied |
| `defensive-security` capabilities | Require explicit `owned_assets` scope |
| `live-trading` capabilities | Require `allow_live_finance=True` |
| `HIGH`-risk capabilities | Require `high_risk_execute` permission |
| Unverified capability acquisition | Rejected (must be `verified=True`, `trust_score ≥ 0.8`) |

These are reference defaults enforced in [`policy.py`](src/genesis_os/policy.py). They are not a substitute for production governance — they establish the minimum safe baseline.

See [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) for the full threat model.

---

## Architecture

```
src/genesis_os/
├── types.py          # Shared contracts: CapabilityManifest, Goal, RunResult, RiskTier, …
├── policy.py         # Central policy gate (the kernel security boundary)
├── registry.py       # Capability registry — multi-provider, discoverable
├── planner.py        # Dependency-aware topological planner with cycle detection
├── routing.py        # Outcome-aware provider router
├── acquisition.py    # Safe capability acquisition from trusted sources
├── compiler.py       # Procedure compilation: repeated success → reusable plan
├── evaluator.py      # Step outcome scorer
├── learning.py       # Curiosity signals from failures and weak outcomes
├── memory.py         # SQLite store: episodes, procedures, objectives, curiosity
├── world.py          # SQLite entity/relation world model
├── objectives.py     # Persistent objective control plane and heartbeats
├── runtime.py        # Closed-loop orchestration (the kernel)
├── catalog.py        # Demo registry, manifest loader, example capability source
├── cli.py            # CLI entry point
└── __init__.py       # Public API
```

### Kernel invariants

Every design decision traces to one of these:

1. Every action has a named capability.
2. Every capability has a manifest and risk tier.
3. Every execution crosses the policy gate.
4. Every run has an immutable run identifier.
5. Every meaningful outcome is evaluated and stored.
6. Providers never write directly into another provider's private state.
7. Long-lived knowledge is outside prompt history.
8. A domain pack cannot weaken kernel policy.
9. Self-extension means adding/versioning a capability, not silently rewriting the kernel.
10. High-risk actions require stronger authorisation than reasoning/research.

---

## Memory hierarchy

| Layer | Storage | Lifetime |
|---|---|---|
| Working memory | Current run `state` dict | Single run |
| Episodic memory | `episodes` table | Persistent across runs |
| World / semantic memory | `entities` + `relations` tables | Persistent |
| Procedural memory | `procedures` table | Persistent; versioned by signature |
| Curiosity / learning | `curiosity` table | Persistent until resolved |

---

## Extending Genesis

### Register a capability

```python
from genesis_os import CapabilityManifest, RiskTier
from genesis_os.registry import CapabilityRegistry

registry = CapabilityRegistry()
registry.register(
    CapabilityManifest(
        name="search.web",
        description="Execute a web search and return structured results",
        tags=("search", "web"),
        risk=RiskTier.LOW,
        permissions=("web_search",),
        provider="duckduckgo",
        cost=0.001,
        latency_ms=400,
    ),
    handler=lambda state: {"results": ["…"]},
)
```

### Run a goal

```python
from genesis_os import GenesisRuntime, Goal, ExecutionContext

runtime = GenesisRuntime(registry)
result = runtime.run(
    Goal(
        objective="Find recent news on AI safety",
        required_capabilities=("search.web",),
        metadata={"query": "AI safety 2025"},
    ),
    ExecutionContext(approved_permissions={"web_search"}),
)
print(result.success, result.metadata)
```

### Create a persistent objective

```python
from genesis_os import GenesisRuntime, ObjectiveEngine, Goal
from genesis_os.memory import MemoryStore
from genesis_os.world import WorldModel

memory = MemoryStore("objectives.db")
world  = WorldModel("world.db")
engine = ObjectiveEngine(GenesisRuntime(registry, memory=memory), memory, world)

record = engine.create(Goal("Monitor signals", ("analyze.signal",)))

# Each call advances the objective by one heartbeat
result = engine.heartbeat(record.objective_id)
```

---

## Development

```bash
# install
pip install -e '.[dev]'

# lint
ruff check src/ tests/

# test
pytest -q

# smoke tests
genesis demo
genesis objective-demo
genesis capabilities
```

### Project layout

```
genesis-os/
├── src/genesis_os/      # Library source
├── tests/               # 25 pytest tests
├── docs/                # Architecture, threat model, capability map, v0.2 spec
├── domains/             # Domain pack descriptors (capital-markets, defensive-security, research)
├── capabilities/        # manifest.schema.json — JSON Schema for capability manifests
├── research/            # Upstream project validation notes
├── pyproject.toml       # Build, test, and lint configuration
└── .github/workflows/   # CI: lint + tests + smoke tests on every push
```

---

## Roadmap

### v0.2 (current) — Closed-loop kernel
Persistent objectives, safe acquisition, provider routing, procedure compilation, learning signals, world model, policy gate.

### v0.3 (next)
- MCP adapter with capability-manifest translation
- A2A peer adapter
- E2B / Firecracker-class sandbox provider
- Durable scheduler / heartbeat worker
- Model router and context-budget manager
- Signed capability packages and provenance
- Human approval service for elevated permissions
- Distributed run ledger and observability exporter
- Semantic / graph memory adapter
- Control-plane UI (objectives, capabilities, permissions, runs, learning signals)

---

## What v0.2 does not pretend to be

The reference kernel does not ship production MCP/A2A adapters, distributed scheduling, a frontier-model router, remote sandbox execution, a human-approval service, or a web control plane. Those belong behind the interfaces already present — not inside the kernel.

---

## Contributing

1. Fork the repo and create a branch from `main`.
2. Make your change. Add or update tests — `pytest -q` must pass.
3. Run `ruff check src/ tests/` — zero errors required.
4. Open a pull request with a clear description of the change and its motivation.

Bug reports and feature proposals are welcome as GitHub Issues.

---

## Contributors

- [@sheldonOS](https://github.com/sheldonOS)
- [@sheldonibm](https://github.com/sheldonibm)

---

## License

The Genesis OS reference code in this repository is [Apache-2.0](LICENSE).  
Upstream projects referenced in `docs/CAPABILITY_MAP.md` and `research/` remain governed by their own licenses.
