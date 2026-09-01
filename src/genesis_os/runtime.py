from __future__ import annotations

import uuid

from .acquisition import CapabilityAcquirer
from .compiler import ProcedureCompiler
from .evaluator import Evaluator
from .learning import LearningEngine
from .memory import MemoryStore
from .planner import Plan, Planner
from .policy import PolicyEngine
from .registry import CapabilityRegistry
from .routing import ProviderRouter
from .types import ExecutionContext, Goal, RunResult, StepResult


class GenesisRuntime:
    def __init__(
        self,
        registry: CapabilityRegistry,
        *,
        memory: MemoryStore | None = None,
        policy: PolicyEngine | None = None,
        evaluator: Evaluator | None = None,
        acquirer: CapabilityAcquirer | None = None,
        compiler: ProcedureCompiler | None = None,
        learning: LearningEngine | None = None,
    ) -> None:
        self.registry = registry
        self.memory = memory or MemoryStore()
        self.policy = policy or PolicyEngine()
        self.evaluator = evaluator or Evaluator()
        self.planner = Planner(registry)
        self.acquirer = acquirer or CapabilityAcquirer(registry)
        self.compiler = compiler or ProcedureCompiler(self.memory)
        self.learning = learning or LearningEngine(self.memory)
        self.router = ProviderRouter(registry, self.memory)

    def _ensure_capability(self, capability: str, domain: str) -> bool:
        if self.registry.has(capability):
            return False
        acquired = self.acquirer.acquire(capability, domain)
        if not acquired:
            raise KeyError(f"unknown capability and acquisition failed: {capability}")
        return True

    def _build_plan(self, goal: Goal) -> tuple[Plan, bool, list[str]]:
        signature = self.compiler.signature(goal.domain, goal.required_capabilities)
        compiled = self.compiler.compiled_steps(signature)
        if compiled:
            return Plan(compiled), True, []

        acquired: list[str] = []
        for capability in goal.required_capabilities:
            if self._ensure_capability(capability, goal.domain):
                acquired.append(capability)

        while True:
            try:
                return self.planner.build(goal), False, acquired
            except KeyError as exc:
                message = str(exc)
                marker = "unknown capability: "
                if marker not in message:
                    raise
                missing = message.split(marker, 1)[1].strip("'\"")
                if self._ensure_capability(missing, goal.domain):
                    acquired.append(missing)

    @staticmethod
    def _run_metadata(
        *,
        acquired: list[str],
        procedure_reused: bool = False,
        procedure_compiled: bool = False,
    ) -> dict:
        return {
            "acquired_capabilities": acquired,
            "procedure_reused": procedure_reused,
            "procedure_compiled": procedure_compiled,
        }

    def run(self, goal: Goal, context: ExecutionContext | None = None) -> RunResult:
        context = context or ExecutionContext()
        run_id = str(uuid.uuid4())
        try:
            plan, reused_procedure, acquired = self._build_plan(goal)
        except KeyError as exc:
            result = RunResult(
                goal=goal,
                success=False,
                steps=[StepResult(capability="capability.acquire", success=False, error=str(exc))],
                run_id=run_id,
                metadata=self._run_metadata(acquired=[]),
            )
            self.learning.observe(result)
            return result

        state = dict(goal.metadata)
        results: list[StepResult] = []

        for capability in plan.steps:
            route = self.router.choose(capability)
            manifest = route.manifest
            decision = self.policy.authorize(manifest, context)
            if not decision.allowed:
                result = StepResult(
                    capability=capability,
                    success=False,
                    error=decision.reason,
                    score=0.0,
                    metadata={"provider": manifest.provider},
                )
                results.append(result)
                self.memory.remember_episode(
                    run_id,
                    capability,
                    False,
                    0.0,
                    {"error": decision.reason},
                    provider=manifest.provider,
                )
                run = RunResult(
                    goal=goal,
                    success=False,
                    steps=results,
                    run_id=run_id,
                    metadata=self._run_metadata(
                        acquired=acquired,
                        procedure_reused=reused_procedure,
                    ),
                )
                self.learning.observe(run)
                return run

            try:
                output = self.registry.handler(capability, manifest.provider)(state)
                state[capability] = output
                result = StepResult(
                    capability=capability,
                    success=True,
                    output=output,
                    metadata={"provider": manifest.provider},
                )
            except Exception as exc:
                result = StepResult(
                    capability=capability,
                    success=False,
                    error=str(exc),
                    metadata={"provider": manifest.provider},
                )

            result.score = self.evaluator.score(result)
            results.append(result)
            self.memory.remember_episode(
                run_id,
                capability,
                result.success,
                result.score,
                {"output": result.output, "error": result.error},
                provider=manifest.provider,
            )
            if not result.success:
                run = RunResult(
                    goal=goal,
                    success=False,
                    steps=results,
                    run_id=run_id,
                    metadata=self._run_metadata(
                        acquired=acquired,
                        procedure_reused=reused_procedure,
                    ),
                )
                self.learning.observe(run)
                return run

        signature = self.compiler.signature(goal.domain, goal.required_capabilities)
        compiled_now = self.compiler.observe_success(signature, plan.steps)
        run = RunResult(
            goal=goal,
            success=True,
            steps=results,
            run_id=run_id,
            metadata=self._run_metadata(
                acquired=acquired,
                procedure_reused=reused_procedure,
                procedure_compiled=compiled_now,
            ),
        )
        self.learning.observe(run)
        return run
