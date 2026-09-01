from __future__ import annotations

from .types import CapabilityFn, CapabilityManifest


class CapabilityRegistry:
    """Logical capability registry with replaceable provider implementations."""

    def __init__(self) -> None:
        self._providers: dict[str, dict[str, tuple[CapabilityManifest, CapabilityFn]]] = {}

    def register(self, manifest: CapabilityManifest, handler: CapabilityFn) -> None:
        providers = self._providers.setdefault(manifest.name, {})
        if manifest.provider in providers:
            raise ValueError(
                f"capability provider already registered: {manifest.name}@{manifest.provider}"
            )
        providers[manifest.provider] = (manifest, handler)

    def has(self, name: str) -> bool:
        return name in self._providers and bool(self._providers[name])

    def providers(self, name: str) -> tuple[CapabilityManifest, ...]:
        try:
            providers = self._providers[name]
        except KeyError as exc:
            raise KeyError(f"unknown capability: {name}") from exc
        return tuple(providers[key][0] for key in sorted(providers))

    def manifest(self, name: str, provider: str | None = None) -> CapabilityManifest:
        try:
            providers = self._providers[name]
        except KeyError as exc:
            raise KeyError(f"unknown capability: {name}") from exc
        if provider is None:
            provider = sorted(providers)[0]
        try:
            return providers[provider][0]
        except KeyError as exc:
            raise KeyError(f"unknown provider for {name}: {provider}") from exc

    def handler(self, name: str, provider: str | None = None) -> CapabilityFn:
        manifest = self.manifest(name, provider)
        return self._providers[name][manifest.provider][1]

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._providers))

    def discover(self, query: str, *, domain: str | None = None) -> list[CapabilityManifest]:
        """Search registered capabilities by text and optional domain.

        A capability with an empty ``domains`` tuple is considered universal and
        will appear in any domain-scoped search (it is not restricted to a specific domain).
        To restrict a capability to one or more domains, set ``domains`` explicitly in its manifest.
        """
        tokens = {t.lower() for t in query.replace(".", " ").replace("-", " ").split()}
        scored: list[tuple[int, CapabilityManifest]] = []
        for name in self.names():
            manifest = self.manifest(name)
            if domain and manifest.domains and domain not in manifest.domains:
                continue
            haystack = " ".join((manifest.name, manifest.description, *manifest.tags)).lower()
            score = sum(1 for token in tokens if token in haystack)
            if score:
                scored.append((score, manifest))
        return [m for _, m in sorted(scored, key=lambda item: (-item[0], item[1].name))]
