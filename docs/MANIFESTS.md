# Capability and Domain Manifests

This document describes the JSON manifest formats used by Genesis OS to describe capabilities
and domain packs. Manifests are the primary mechanism for declaring what an agent can do,
what risks it carries, and where it is permitted to operate.

---

## Capability Manifests

A **capability manifest** is a JSON file that describes a single named action the runtime can
execute. Manifests are loaded via [`catalog.load_manifest(path)`](../src/genesis_os/catalog.py)
and registered into a [`CapabilityRegistry`](../src/genesis_os/registry.py).

### Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | `string` | ✅ | — | Dot-namespaced capability identifier, e.g. `sense.local_event` |
| `description` | `string` | ✅ | — | Human-readable summary of what the capability does |
| `tags` | `string[]` | | `[]` | Free-form labels used by `discover()` for text search |
| `risk` | `string` | | `"LOW"` | Risk tier: `READ_ONLY`, `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` |
| `requires` | `string[]` | | `[]` | Capabilities that must run before this one (DAG edges) |
| `permissions` | `string[]` | | `[]` | Named permissions the executor must hold |
| `domains` | `string[]` | | `[]` | Domain restriction list — empty means universal (no restriction) |
| `provider` | `string` | | `"local"` | Provider identifier, e.g. `"local"`, `"mcp"`, `"a2a"` |
| `learnable` | `boolean` | | `true` | Whether this capability participates in procedure compilation |
| `version` | `string` | | `"1"` | Capability version string |
| `cost` | `number` | | `0.0` | Estimated cost per invocation (arbitrary units) |
| `latency_ms` | `number` | | `0.0` | Expected latency in milliseconds |

### Risk Tiers

Risk tiers map to [`RiskTier`](../src/genesis_os/types.py) and govern policy authorization:

| Tier | Value | Typical use |
|------|-------|-------------|
| `READ_ONLY` | 0 | Observation, sensing, reading state |
| `LOW` | 1 | Writing non-sensitive artifacts, local decisions |
| `MEDIUM` | 2 | Network calls, user-visible writes |
| `HIGH` | 3 | Financial operations, external API mutations |
| `CRITICAL` | 4 | Irreversible system-level actions |

### Domain Scoping

The `domains` field restricts which domain packs may invoke a capability:

- **Empty list (`[]`)** — the capability is *universal* and available in any domain.
- **Non-empty list** — the capability is *restricted* to the listed domain slugs.
  A `discover()` call scoped to `domain="finance"` will exclude capabilities whose `domains`
  list does not include `"finance"`.

### Example

```json
{
  "name": "analyze.market_signal",
  "description": "Analyze a structured market signal from a trusted data feed",
  "tags": ["analysis", "finance", "signal"],
  "risk": "MEDIUM",
  "requires": ["sense.market_feed"],
  "permissions": ["read_market_data"],
  "domains": ["finance", "trading"],
  "provider": "local",
  "learnable": true,
  "version": "2",
  "cost": 0.02,
  "latency_ms": 120.0
}
```

### Loading a manifest file

```python
from genesis_os.catalog import load_manifest
from genesis_os.registry import CapabilityRegistry

registry = CapabilityRegistry()
manifest = load_manifest("capabilities/analyze.market_signal.json")
registry.register(manifest, handler=my_handler_fn)
```

`load_manifest` raises `ValueError` if `name` or `description` are missing, or if `risk`
is not a valid `RiskTier` name.

---

## Domain Pack Manifests

A **domain pack** groups capabilities, permissions, and constraints into a named operating
context. Domains allow the same capability graph to be configured differently for different
use cases (e.g., `finance`, `healthcare`, `general`).

### Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `slug` | `string` | ✅ | — | Short identifier used in `Goal.domain` and capability `domains` arrays |
| `display_name` | `string` | ✅ | — | Human-readable name |
| `description` | `string` | | `""` | Purpose of this domain pack |
| `default_permissions` | `string[]` | | `[]` | Permissions granted to all actors in this domain |
| `max_risk` | `string` | | `"HIGH"` | Maximum risk tier allowed without explicit override |
| `capabilities` | `string[]` | | `[]` | Explicit capability allow-list (empty = all registered capabilities) |
| `tags` | `string[]` | | `[]` | Free-form labels for discovery |

### Example

```json
{
  "slug": "finance",
  "display_name": "Financial Analysis",
  "description": "Domain pack for read-only financial signal analysis and reporting",
  "default_permissions": ["read_market_data"],
  "max_risk": "MEDIUM",
  "capabilities": [
    "sense.market_feed",
    "analyze.market_signal",
    "act.record_decision"
  ],
  "tags": ["finance", "analysis", "read-only"]
}
```

### Domain pack at runtime

```python
from genesis_os.types import Goal, ExecutionContext

goal = Goal(
    objective="analyze latest market signal",
    required_capabilities=("sense.market_feed", "analyze.market_signal"),
    domain="finance",          # matched against CapabilityManifest.domains
)

ctx = ExecutionContext(
    actor="analyst",
    approved_permissions={"read_market_data"},
)

result = runtime.run(goal, ctx)
```

---

## File layout convention

There is no enforced directory structure — manifests can live anywhere that your loader code
references. A recommended layout is:

```
capabilities/
  sense.local_event.json
  analyze.event.json
  act.record_decision.json
  manifest.schema.json          # JSON Schema for validation (optional)

domains/
  general.json
  finance.json
```

Load them at startup and register each into a `CapabilityRegistry` before constructing a
`GenesisRuntime`.

---

## Validating manifests

To validate a directory of manifests programmatically:

```python
from pathlib import Path
from genesis_os.catalog import load_manifest

errors = []
for path in Path("capabilities").glob("*.json"):
    if path.name == "manifest.schema.json":
        continue
    try:
        load_manifest(path)
    except (ValueError, KeyError) as exc:
        errors.append(f"{path}: {exc}")

if errors:
    raise SystemExit("\n".join(errors))
```

---

## Related modules

| Module | Role |
|--------|------|
| [`catalog.py`](../src/genesis_os/catalog.py) | `load_manifest()` — parses JSON into `CapabilityManifest` |
| [`types.py`](../src/genesis_os/types.py) | `CapabilityManifest`, `RiskTier`, `Goal` dataclasses |
| [`registry.py`](../src/genesis_os/registry.py) | `CapabilityRegistry` — stores and discovers manifests |
| [`policy.py`](../src/genesis_os/policy.py) | `PolicyEngine` — authorizes against manifest risk + permissions |
| [`routing.py`](../src/genesis_os/routing.py) | `ProviderRouter` — selects provider for execution |
