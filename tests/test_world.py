from genesis_os.world import WorldModel


def test_world_model_round_trip_and_relationships():
    world = WorldModel()
    world.upsert_entity("a", "company", {"stage": "seed"})
    world.upsert_entity("b", "market", {"name": "AI"})
    world.link("a", "operates_in", "b", {"confidence": 0.9})
    assert world.entity("a")["state"]["stage"] == "seed"
    assert world.neighbors("a")[0]["target"] == "b"
