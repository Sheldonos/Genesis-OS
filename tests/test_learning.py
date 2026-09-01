from genesis_os.learning import LearningEngine
from genesis_os.memory import MemoryStore
from genesis_os.types import Goal, RunResult, StepResult


def test_learning_engine_creates_curiosity_from_failure():
    memory = MemoryStore()
    result = RunResult(
        goal=Goal("g", ("x",)),
        success=False,
        steps=[StepResult(capability="x", success=False, error="boom")],
        run_id="r1",
    )
    signals = LearningEngine(memory).observe(result)
    assert signals[0].question.startswith("Why did capability")
    assert memory.curiosity()[0]["run_id"] == "r1"
