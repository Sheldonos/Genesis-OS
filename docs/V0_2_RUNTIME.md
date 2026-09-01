# Genesis OS v0.2 Runtime

## Purpose

v0.2 moves Genesis from a fixed capability executor to a small persistent intelligence runtime. It implements the minimum closed loop needed for a system to become more operationally capable through use while retaining explicit safety boundaries.

## Runtime loop

1. Persist an objective.
2. On heartbeat, load its goal and current state.
3. Reuse a compiled procedure when one exists.
4. Otherwise resolve the dependency graph.
5. If a required capability is missing, ask configured trusted capability sources for a verified adapter.
6. Route each logical capability to a provider using historical outcome quality, cost, and latency.
7. Authorize the selected provider through the central policy gate.
8. Execute and evaluate each step.
9. Store provider-specific episodes.
10. Promote repeatedly successful plans into compiled procedures.
11. Update objective and world-model state.
12. Convert failures or weak scores into curiosity/learning signals.

## Core modules

- `objectives.py` — persistent objective creation and heartbeats.
- `world.py` — typed entity/relationship state.
- `acquisition.py` — verified capability-source interface.
- `routing.py` — outcome-aware provider selection.
- `compiler.py` — repeated-plan promotion and reuse.
- `learning.py` — curiosity signals from execution deltas.
- `runtime.py` — closed-loop orchestration.

## Capability acquisition boundary

The reference runtime deliberately distinguishes **capability acquisition** from **arbitrary self-modifying code**. A source may propose an `AcquiredCapability` only when it includes a concrete manifest, handler, source identity, verification flag, and trust score. The acquirer rejects unverified, low-trust, critical-risk, and offensive-security candidates. Execution remains subject to the normal policy gate after registration.

A production source can sit in front of MCP registries, A2A peers, signed skill catalogs, containerized tools, or a code-generation pipeline. Generated code should be built and evaluated in an isolated environment before a source marks it verified.

## Procedure compilation

A procedure is a versionable deterministic ordering of logical capabilities that has succeeded repeatedly for the same `(domain, required capabilities)` signature. v0.2 compiles after two successes and reuses on the next run. Production versions should add input/output schemas, semantic versioning, evaluator thresholds, invalidation rules, and rollback.

## Provider routing

The router starts unseen providers with a neutral prior, then uses stored episode quality while subtracting bounded cost and latency penalties. This is intentionally simple but establishes the contract for future contextual bandits, model routing, privacy constraints, hardware locality, and SLA-aware selection.

## World model

The current world model is a SQLite graph of entities and typed relations. It is deliberately small and transparent. Production adapters can project this interface onto graph databases or semantic-memory systems without changing the objective/runtime contract.

## Safety invariants

- One policy gate before every capability execution.
- No critical-risk execution in the reference kernel.
- No offensive-security execution in the base runtime.
- Defensive security requires owned-asset scope.
- Live financial execution requires explicit approval.
- Missing capabilities do not trigger arbitrary code execution.
- Provider learning affects routing, not authorization.

## v0.3 target

1. MCP adapter with capability-manifest translation.
2. A2A peer adapter.
3. E2B/OpenShell/Firecracker-class sandbox provider.
4. Durable scheduler/heartbeat worker.
5. Model router and context-budget manager.
6. Signed capability packages and provenance.
7. Human approval service for elevated permissions.
8. Distributed run ledger and observability exporter.
9. Semantic/graph memory adapter.
10. Control-plane UI for objectives, capabilities, permissions, runs, and learning signals.
