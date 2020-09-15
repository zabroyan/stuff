import pytest


@pytest.mark.last
def test_artificial_intelligence(game_instance):
    attacker = game_instance[-2]
    game_engine = game_instance[-1]

    spawn_list = attacker.spawn_information_list[0]

    game_engine.get_game_history().end_turn()
    game_engine.get_game_history().active_player.act()

    units = game_engine._GameEngine__player_units[game_engine.get_game_history().active_player]

    units_compare = [(x.position, x.object_type) for x in units]
    spawn_compare = [(x.position, x.object_type) for x in spawn_list]

    assert set(spawn_compare).issubset(set(units_compare))

    game_engine.get_game_history().end_turn()
