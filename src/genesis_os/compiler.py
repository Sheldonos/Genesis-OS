from __future__ import annotations

from .memory import MemoryStore


class ProcedureCompiler:
    """Promotes repeatedly successful plans into reusable deterministic procedures."""

    def __init__(self, memory: MemoryStore, threshold: int = 2) -> None:
        if threshold < 1:
            raise ValueError("threshold must be >= 1")
        self.memory = memory
        self.threshold = threshold

    def signature(self, domain: str, required_capabilities: tuple[str, ...]) -> str:
        return f"{domain}:{'|'.join(required_capabilities)}"

    def compiled_steps(self, signature: str) -> tuple[str, ...] | None:
        procedure = self.memory.procedure(signature)
        if not procedure or not procedure["compiled"]:
            return None
        return tuple(procedure["steps"])

    def observe_success(self, signature: str, steps: tuple[str, ...]) -> bool:
        """Record a successful run.

        Returns True exactly once: when the success count first reaches the threshold.
        """
        successes = self.memory.record_procedure_success(signature, list(steps))
        if successes == self.threshold:
            self.memory.compile_procedure(signature)
            return True
        return False
