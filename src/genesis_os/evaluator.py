from __future__ import annotations

from .types import StepResult


class Evaluator:
    def score(self, result: StepResult) -> float:
        if not result.success:
            return 0.0
        if result.output is None:
            return 0.5
        return 1.0
