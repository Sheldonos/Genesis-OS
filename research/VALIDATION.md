# Research Validation Notes — September 2026

The architecture was cross-checked against current public projects and standards before implementation.

## Findings that strengthened the design

- **MCP 2026-07-28** moved toward a stateless, routable core with stronger authorization and extension points. Genesis should not invent a competing tool protocol; it should put policy/state above MCP.
- **A2A** is positioned as a vendor-neutral protocol for communication between heterogeneous agents. Genesis should use it at organizational boundaries while keeping its own run ledger and policy.
- **OpenAI Agents SDK (2026)** explicitly supports long-horizon work in controlled sandboxes, reinforcing isolation as a first-class execution boundary.
- **Anthropic Agent Skills** uses progressive disclosure: load metadata first, then detailed procedural content only when relevant. Genesis capability discovery follows the same context-efficiency principle.
- **Paperclip** uses heartbeats and persisted agent identity rather than immortal processes, supporting Genesis's heartbeat lifecycle.
- **Cognee** exposes a minimal remember/recall/forget memory surface and combines graph + semantic retrieval, supporting a layered memory provider interface.
- **E2B** provides isolated, long-running agent environments, supporting an interchangeable sandbox broker.
- **NemoClaw** demonstrates deny-by-default sandbox filesystem/network policy.
- **DeerFlow/OpenSpace** package tools, skills, memory, sandboxes, and subagents as runtime components, reinforcing provider modularity.
- **Crucix/WorldMonitor** demonstrate continuously updated world sensing and cross-stream correlation as a distinct sensor layer.
- **ASI-Evolve** demonstrates a closed knowledge -> hypothesis -> experiment -> analysis loop that can become a research-domain learning loop.
- **OpenBB** demonstrates normalized access to many financial data providers behind one interface, a strong model for domain capability adapters.

## Findings that changed the original plan

### Do not create one universal monorepo of upstream source

The supplied repositories span incompatible licenses, stacks, release cadences, and security assumptions. The integration unit must be a versioned provider adapter, not copied source.

### Do not use one agent framework as the kernel

Agent frameworks are replaceable. The stable layer is goals, capabilities, policy, run state, memory, and evaluated outcomes.

### Do not equate self-improvement with autonomous source-code mutation

The safe unit of self-improvement is a versioned capability/procedure that is sandboxed, tested, evaluated, and promoted. Kernel mutation remains ordinary software engineering.

### Do not make live action the default in sensitive domains

Research/simulation should be separable from financial execution, security actions, credential writes, and irreversible external changes.
