from genesis_os.memory import MemoryStore


def test_episode_round_trip():
    memory = MemoryStore()
    memory.remember_episode("r1", "cap", True, 1.0, {"x": 1})
    rows = memory.episodes("cap")
    assert rows[0]["payload"] == {"x": 1}
