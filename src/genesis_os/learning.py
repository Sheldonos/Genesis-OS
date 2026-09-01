from __future__ import annotations

from .memory import MemoryStore
from .types import CuriositySignal, RunResult


class LearningEngine:
    """Turns unexplained failures/weak outcomes into explicit learning questions."""

    def __init__(self, memory: MemoryStore) -> None:
        self.memory = memory

    def observe(self, result: RunResult) -> list[CuriositySignal]:
        signals: list[CuriositySignal] = []
        for step in result.steps:
            if not step.success:
                signals.append(
                    CuriositySignal(
                        question=f"Why did capability '{step.capability}' fail?",
                        reason=step.error or "execution failed without an explanation",
                        priority=1.0,
                        run_id=result.run_id,
                    )
                )
            elif step.score < 0.75:
                signals.append(
                    CuriositySignal(
                        question=f"How can '{step.capability}' improve its outcome?",
                        reason=f"evaluation score was {step.score:.2f}",
                        priority=0.75,
                        run_id=result.run_id,
                    )
                )
        for signal in signals:
            self.memory.add_curiosity(
                signal.run_id,
                signal.question,
                signal.reason,
                signal.priority,
            )
        return signals
