# Implementation Strategy

## Phase 1 — Research and architecture

Completed in this reference build:

- clustered supplied repositories by primitive
- separated kernel invariants from replaceable providers
- selected capability manifest as the stable unit
- selected central policy gate as mandatory execution boundary
- selected heartbeat/persist/exit lifecycle over immortal agents
- selected episodic + semantic + procedural memory hierarchy
- selected sandbox-before-promotion for generated tools

## Phase 2 — Technical specification

### Services for a production build

1. `control-plane` — APIs/UI, goals, approvals, budgets
2. `runtime` — planner and run state machine
3. `capability-registry` — manifests, providers, versions, health
4. `policy` — ABAC/RBAC/risk decisions and immutable audit log
5. `memory` — working/episodic adapters plus graph/semantic interface
6. `evaluation` — online/offline evaluators and attribution
7. `sandbox-broker` — isolated execution providers
8. `event-ingress` — schedules, sensors, webhooks, queues
9. `model-router` — task/model selection and quotas
10. `compiler` — procedure -> workflow/skill/code promotion pipeline

### Suggested production substrate

- Postgres for authoritative run/capability/policy metadata
- object storage for artifacts
- graph/vector backend behind a memory abstraction
- queue/event bus for heartbeats
- OpenTelemetry-compatible tracing
- isolated sandbox provider(s)
- signed capability packages / SBOM / provenance

## Phase 3 — Market validation

Prototype with three sharply different workloads to prove generality:

1. **Research watch:** ingest public signals, correlate change, produce cited brief.
2. **Software task:** inspect a test repo, propose a patch in a sandbox, run tests, open a PR with approval.
3. **Business workflow:** intake a lead, research, draft a proposal, update CRM in dry-run mode.

The same kernel should execute all three; only capabilities/domain policy change.

## Phase 4 — Resource plan

A serious production build is a platform program, not a weekend monorepo merge. Minimum focused team:

- 2 runtime/platform engineers
- 1 security/sandbox engineer
- 1 data/memory engineer
- 1 frontend/control-plane engineer
- 1 evaluation/ML systems engineer
- domain owners added per pack

## Phase 5 — Prototype and testing

The v0.1 code in this repository is the first executable kernel. Exit criteria for v0.2:

- real MCP provider adapter
- sandbox provider adapter
- provider health/reliability scoring
- durable heartbeat queue
- Postgres run ledger
- graph memory adapter
- signed capability manifest
- approval event primitive
- integration tests with at least two external providers

## Promotion model

Capabilities move through:

```text
candidate -> sandboxed -> evaluated -> approved -> production -> degraded/quarantined
```

Provider versions are independent from capability names, enabling rollback and A/B evaluation.
