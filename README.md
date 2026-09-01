# Genesis OS

**A policy-governed capability operating system for persistent, composable autonomous intelligence.**

Genesis OS turns objectives into auditable capability graphs, acquires missing trusted capabilities, routes work across interchangeable providers, persists objective/world state, learns from outcomes, and promotes repeated successful plans into reusable procedures.

It is intentionally **not** marketed as AGI. The engineering target is concrete:

> Given a persistent objective, determine the capabilities required to pursue it, acquire approved missing capabilities, choose providers using observed outcomes, execute through one policy boundary, update structured world state, create learning questions from failures, and compile repeated successful behavior into reusable procedures.

## Why this is different

Most agent systems stop at `model -> tools -> actions`. Genesis owns the layer above that:

```text
Persistent Objective
      |
      v
Capability Graph ---- missing? ----> Trusted Capability Acquisition
      |                                      |
      v                                      v
Provider Router <------- outcome history / cost / latency
      |
      v
Central Policy Gate
      |
      v
Execution -> Evaluation -> Episodic Memory
      |                         |
      v                         v
World Model              Procedure Compiler
      |                         |
      +------ Learning / Curiosity <------+
                    |
                    v
              next heartbeat
```

The goal is not a permanent zoo of named agents. Agents, models, skills, browsers, sandboxes, APIs, humans, and machines are replaceable capability providers. Genesis keeps the durable objective, policy, memory, learning, and capability-selection state.

## v0.2 implemented runtime

- **Persistent objectives** — objectives survive individual runs and advance through explicit heartbeats.
- **Structured world model** — typed entities and relationships hold durable state outside prompt context.
- **Safe capability acquisition** — missing capabilities may be registered from explicit verified sources; arbitrary generated code is not executed.
- **Provider routing** — multiple providers can implement one logical capability and are ranked using observed quality, cost, and latency.
- **Procedure compilation** — repeatedly successful plans are promoted into reusable procedures and bypass replanning on later runs.
- **Learning/curiosity signals** — unexplained failures and weak outcomes generate stored learning questions for future investigation.
- **Central policy boundary** — permissions, risk tiers, owned-asset scope, live-finance approval, and sensitive-domain restrictions still gate every execution.
- **Backward-compatible v0.1 kernel** — dependency planning, capability discovery, episodic memory, evaluation, and the original CLI demo remain intact.

## Quick start

```bash
python -m pip install -e '.[dev]'
pytest -q
python -m genesis_os.cli demo
python -m genesis_os.cli objective-demo
```

`objective-demo` performs three heartbeats. The first acquires a missing verified capability, the second reaches the compilation threshold, and the third reuses the compiled procedure.

Expected metadata pattern:

```text
heartbeat 1: acquired_capabilities=[analyze.signal], procedure_reused=false
heartbeat 2: procedure_compiled=true
heartbeat 3: procedure_reused=true
```

## Capability contract

Capabilities describe the logical operation independently from its provider:

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

Multiple providers can register the same `name`. The router chooses among them using observed outcomes and provider attributes.

## Safety boundaries

Genesis is designed for long-running autonomy without making the base runtime unrestricted.

- Offensive-security execution is disabled in the base runtime.
- Critical-risk capabilities are denied by default.
- Defensive-security actions require explicit owned-asset scope.
- Live financial execution is off by default and requires explicit authorization.
- Capability acquisition accepts only verified adapters above a trust threshold.
- Generated code should execute in an external isolated sandbox and pass evaluation before it is eligible for registration.

See `docs/THREAT_MODEL.md`.

## What v0.2 does not pretend to be

The reference kernel does not yet ship production MCP/A2A adapters, distributed scheduling, a frontier-model router, remote sandbox execution, a human-approval service, or a web control plane. Those belong behind the interfaces already present rather than inside the kernel.

The next milestone is v0.3: real protocol/provider adapters plus a durable heartbeat service. See `docs/V0_2_RUNTIME.md`.

## Upstream strategy

Genesis does **not** vendor the large set of upstream projects that informed the architecture. They remain replaceable providers/domain packs with their own licenses and security posture. This avoids turning the kernel into an unmaintainable transitive dependency graph.

See `docs/CAPABILITY_MAP.md` and `research/VALIDATION.md`.

## Contributors

- [@sheldonOS](https://github.com/sheldonOS)
- [@sheldonibm](https://github.com/sheldonibm)

## License

The Genesis OS reference code in this repository is Apache-2.0. Upstream projects remain governed by their own licenses.
