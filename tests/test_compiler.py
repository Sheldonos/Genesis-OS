from genesis_os.compiler import ProcedureCompiler
from genesis_os.memory import MemoryStore


def test_compiler_promotes_repeated_success():
    memory = MemoryStore()
    compiler = ProcedureCompiler(memory, threshold=2)
    signature = compiler.signature("general", ("a",))
    assert not compiler.observe_success(signature, ("a",))
    assert compiler.observe_success(signature, ("a",))
    assert compiler.compiled_steps(signature) == ("a",)
