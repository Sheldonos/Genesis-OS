from __future__ import annotations

from dataclasses import dataclass

from .types import CapabilityManifest, ExecutionContext, RiskTier


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


class PolicyEngine:
    """Central gate. Nothing executes without a decision from here."""

    def authorize(self, manifest: CapabilityManifest, context: ExecutionContext) -> PolicyDecision:
        missing = set(manifest.permissions) - context.approved_permissions
        if missing:
            return PolicyDecision(False, f"missing permissions: {sorted(missing)}")

        if manifest.risk >= RiskTier.CRITICAL:
            return PolicyDecision(
                False,
                "critical capabilities are disabled in the reference runtime",
            )

        if "offensive-security" in manifest.tags:
            return PolicyDecision(
                False,
                "offensive security execution is not available in the base runtime",
            )

        if "defensive-security" in manifest.tags and not context.owned_assets:
            return PolicyDecision(
                False,
                "defensive security actions require an explicit owned-asset scope",
            )

        if "live-trading" in manifest.tags and not context.allow_live_finance:
            return PolicyDecision(
                False,
                "live financial execution requires an explicit live-finance approval",
            )

        if (
            manifest.risk >= RiskTier.HIGH
            and "high_risk_execute" not in context.approved_permissions
        ):
            return PolicyDecision(
                False,
                "high-risk execution requires high_risk_execute approval",
            )

        return PolicyDecision(True, "allowed")
