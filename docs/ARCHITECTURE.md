# Architecture

## Design thesis

The system should resemble an operating system more than a chatbot framework. Models are processors; agents are ephemeral processes; capabilities are syscalls; memory is a hierarchy; domain packs are applications; policy is the kernel security boundary.

## Kernel invariants

These rules keep a growing agent ecosystem coherent:

1. Every action has a named capability.
2. Every capability has a manifest and risk tier.
3. Every execution crosses the policy gate.
4. Every run has an immutable run identifier.
5. Every meaningful outcome is evaluated and stored.
6. Providers never write directly into another provider's private state.
7. Long-lived knowledge is outside prompt history.
8. A domain pack cannot weaken kernel policy.
9. Self-extension means adding/versioning a capability, not silently rewriting the kernel.
10. High-risk actions require stronger authorization than reasoning/research.

## Layers

### 1. Intent layer

Normalizes goals from chat, voice, API calls, schedules, sensors, or application events.

### 2. World-state layer

Production Genesis should maintain a typed graph of entities, relationships, observations, confidence, provenance, and time. Vector retrieval is useful, but it is not the source of truth.

### 3. Capability graph

Capabilities describe what can be done, not which library performs it. Dependencies form a DAG when possible. Composite procedures can be promoted into new capabilities after successful repetition.

### 4. Planner

The v0 planner resolves dependencies deterministically. Production planning can add model-based decomposition, cost/reliability scoring, simulation, and replanning, while preserving the same executable plan contract.

### 5. Policy kernel

Policy is separate from prompts. It receives the requested capability, actor context, permissions, asset scope, and risk class. A provider cannot override a denial.

### 6. Provider mesh

Adapters can expose:

- MCP tools and tasks
- A2A remote agents
- browser/computer-use systems
- local functions / internal APIs
- workflow systems
- code sandboxes
- model inference
- human approvals
- sensor/data feeds

### 7. Evaluation and attribution

Success must be measured using task-specific evaluators, not model confidence alone. Store expected result, observed result, score, cost, latency, provider, and downstream outcome.

### 8. Learning / capability compilation

A safe learning loop is:

```text
reason -> execute -> evaluate -> repeat -> detect stable procedure
       -> compile workflow/skill -> test in sandbox -> version -> promote
```

The system improves by converting repeated successful reasoning into cheaper, testable procedures.

## Memory hierarchy

- **Working memory:** current run state; aggressively bounded.
- **Episodic memory:** what happened during prior runs.
- **Semantic/world memory:** facts, entities, relations, provenance.
- **Procedural memory:** reusable plans, skills, workflows, code.
- **Outcome memory:** delayed business/real-world effects used for attribution.

Cognee, Supermemory, memU, OpenMemory, claude-mem, Onyx, AppFlowy/Obsidian-style systems can sit behind specialized adapters rather than becoming the kernel database.

## Heartbeats instead of immortal agents

Long-running autonomy should be driven by persisted state + triggers, not a single infinite agent process. A heartbeat loads the minimum required state, acts, persists results, then exits. This is easier to budget, debug, migrate, and recover.

## Protocol posture

- MCP: tool/data/task interoperability
- A2A: agent-to-agent interoperability
- Agent Skills: portable procedural knowledge
- Genesis manifests: internal capability/risk/policy identity

Genesis can speak all three while retaining its own stronger execution contract.
