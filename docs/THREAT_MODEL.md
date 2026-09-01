# Threat Model

## Primary risks

### 1. Prompt/tool injection

External content can try to redefine objectives or request tools. Treat retrieved content as data, not authority. Tool invocation is authorized from typed runtime state, never from free-form prompt text alone.

### 2. Excessive agency

A capable system can cause damage even without malicious intent. Use explicit capability permissions, spend/time limits, asset scope, staged approvals, and reversible actions where possible.

### 3. Generated-code escape

Generated tools run in isolated sandboxes with deny-by-default filesystem/network policy. Promotion requires tests, provenance, and policy review.

### 4. Memory poisoning

Memories require provenance, confidence, tenancy, and deletion/version semantics. No provider writes unreviewed facts directly into authoritative identity/policy state.

### 5. Credential leakage

Credentials are provider-scoped, never placed in prompts or general memory, and should be injected just-in-time by a broker. Logs must redact secrets.

### 6. Supply-chain risk

Upstream projects are adapters, not vendored source. Pin versions, verify signatures/checksums where possible, generate SBOMs, and quarantine unhealthy providers.

### 7. Cross-domain privilege escalation

A finance research capability should not inherit production trading permissions. A security research capability should not inherit arbitrary network scope. Domain packs can add restrictions but cannot bypass kernel policy.

## Base-runtime hard stops

- critical-risk actions denied
- offensive-security execution denied
- defensive-security actions require explicit owned-asset scope
- live trading denied unless separately enabled
- high-risk actions require `high_risk_execute`

These are reference defaults, not a substitute for production governance.
