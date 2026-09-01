# Capability Map

The user-supplied repository set is best understood as a library of primitives, not a list of packages to merge. Duplicates have been collapsed below.

| Layer | Representative upstreams | Genesis role | Default disposition |
|---|---|---|---|
| Control plane / org orchestration | Paperclip, crewAI, Agency Swarm, agency-agents, atomic-agents, ruflo, AgentGPT, Flowise | goal decomposition, agent lifecycle, org/budget patterns | extract patterns / adapters |
| Research / autonomous experimentation | ASI-Evolve, OpenSpace, DeerFlow, MiroFish, mad-professor-public, pi-autoresearch | hypothesis/experiment loops, deep research | adapter / domain pack |
| Skills / capability libraries | anthropics/skills, heygen/skills, awesome-agent-skills, awesome-claude-skills, superpowers, Product-Manager-Skills, customer-success-skills, scientific-agent-skills | progressive-disclosure procedural knowledge | native ingestion target |
| Memory / context | Cognee, Supermemory, memU, OpenMemory, agentmemory, claude-mem, context-hub, OpenViking, Onyx, Second-Brain projects | semantic, episodic, user/context memory | provider adapters |
| Browser / computer use | browser-use, CUA, Open Computer Use, ai-sdk-computer-use, mac_computer_use, nodriver, Browserbase MCP | web/GUI actuator | adapter with approvals |
| Sandboxes / execution | E2B, E2B infra/desktop/fragments/cookbook, Firecracker, NemoClaw/OpenShell patterns | isolated code/tool execution | mandatory boundary |
| Personal assistant / ambient interface | OpenClaw, NemoClaw, Hermes Agent, Airi, OpenHuman, Amurex, companion projects, Natively/Cluely variants | channels, voice, presence, personal state | UI/provider patterns |
| World sensing / OSINT | Crucix, WorldMonitor, NASA Worldview, Ominis-OSINT, airecon, Wiseflow, SearXNG | persistent sensing, search, correlation | read-only sensor pack |
| Defensive security | Atomic Red Team, HackTricks, Tulip, PentAGI, Sarenka, HostHunter, WiGLE tooling, awesome-ctf/cyber-skills | authorized detection, emulation, hardening knowledge | scoped defensive pack only |
| Finance data / analysis | OpenBB, FinceptTerminal, whisper-money, TaxHacker | normalized data/research | read/analysis adapters |
| Quant / trading research | Kronos, NautilusTrader, TradingAgents, AI-Trader, Vibe-Trading, AutoHedge | forecasting, backtest, simulation, portfolio/risk | simulation first; live separately gated |
| Workflow automation | n8n-mcp, n8n-skills, n8n-workflows, Activepieces, autoMate | durable deterministic procedures | compiler target |
| Developer / coding agents | oh-my-claudecode, ECC, Vibekit, Godel Agent, babyagi variants, evolving-ai, Open-Generative-AI | code generation/refactoring/tool building | sandboxed builder pack |
| Model routing / inference | MiniMax-01, ClawRouter, Vercel AI/AI SDK, model prompt repositories | replaceable model providers / routing | adapter |
| Voice / audio | VibeVoice, Fish Speech, Whisper/WhisperX, OpenVoice, Real-Time-Voice-Cloning, Speak-style assistants | speech I/O | provider adapters |
| Avatar / human perception | face-api, human, talking-avatar-with-ai, HeyGem, ai-iris-avatar | multimodal/avatar interfaces | optional UI pack |
| Video / media generation | Remotion, claude-code-video-toolkit, OpenMontage, Wan2GP, Fooocus, ACE Step UI, OpenToonz | media production capabilities | media domain pack |
| 3D / embodied worlds | Claw3D, dimos, OpenGame, Hunyuan/3D-class tools | simulation/embodiment | experimental pack |
| Productivity / knowledge apps | AppFlowy, Notabase, Obsidian companions, MolecularNotes, OpenOffice | document/object surfaces | UI/storage adapters |
| Design / UX | Penpot, ui-ux-pro-max skills, design-extract, uxie, awesome-design-md, animate.css | UI generation/evaluation | design pack |
| Analytics / growth | Plausible CE, lead-generator-ai, career-ops, claude-ads, YouTube automation agents | business outcome sensors/workflows | business domain packs |
| RAG / retrieval | AutoRAG, GLM-OCR, bilingual book maker, translation tools | ingestion, OCR, retrieval eval | data plane adapters |
| Agent UI | CopilotKit, assistant-ui, Open Assistant, executive-ai-assistant | operator control plane | UI layer |
| Deployment | Vercel, self-hosting stacks, Portable AI USB projects | deploy/local/edge footprints | deployment adapters |

## Repositories that should remain reference-only in the base kernel

Some upstreams are valuable research material but should not be dependencies of a general-purpose runtime:

- exploit/escalation-oriented security utilities
- watermark-removal/unredaction/privacy-sensitive utilities
- media download/copyright-circumvention utilities
- unrestricted trading/execution stacks
- prompt-leak/system-prompt collections

They can be reviewed for defensive research, interoperability, or domain-specific deployments under separate policy and licensing review.

## Integration classification

Every candidate upstream should end in one of five states:

1. **Core concept absorbed** — implement the invariant ourselves.
2. **Provider adapter** — integrate through stable API/protocol.
3. **Domain pack** — optional capability set with separate policy.
4. **UI/reference** — borrow interaction/architecture lessons only.
5. **Reject/quarantine** — unacceptable license, maintenance, security, or product overlap.

This prevents "GitHub stars as architecture" and keeps the system maintainable.
