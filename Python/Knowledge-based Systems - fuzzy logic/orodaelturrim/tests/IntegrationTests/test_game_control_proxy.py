import pytest
from flexmock import flexmock

from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Exceptions import IllegalActionException
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.GameObjects.Prototypes.Defenders import Ent, Archer
from OrodaelTurrim.Structure.Position import OffsetPosition


@pytest.fixture(scope='module')
def game_control_proxy(game_instance):
    return game_instance[2]


def test_spawn_unit_not_visible_tile(game_control_proxy, defender):
    with pytest.raises(IllegalActionException) as exc:
        si = SpawnInformation(defender, GameObjectType.ARCHER, OffsetPosition(0, -2), [], [])
        game_control_proxy.spawn_unit(si)

    assert 'Attempt to spawn unit at not visible tile!' in str(exc.value)


def test_spawn_unit_out_of_map(game_control_proxy, defender):
    with pytest.raises(IllegalActionException) as exc:
        si = SpawnInformation(defender, GameObjectType.ARCHER, OffsetPosition(0, -5), [], [])
        game_control_proxy.spawn_unit(si)

    assert 'Position is not on the map!' in str(exc.value)


@pytest.mark.parametrize('position', [
    OffsetPosition(0, 0),
    OffsetPosition(-1, -1),
])
def test_spawn_unit_occupied_position(game_control_proxy, defender, position):
    with pytest.raises(IllegalActionException) as exc:
        si = SpawnInformation(defender, GameObjectType.ARCHER, position, [], [])
        game_control_proxy.spawn_unit(si)

    assert 'Tile is already occupied!' in str(exc.value)


def test_spawn_second_base(game_control_proxy, defender):
    with pytest.raises(IllegalActionException) as exc:
        si = SpawnInformation(defender, GameObjectType.BASE, OffsetPosition(1, 1), [], [])
        game_control_proxy.spawn_unit(si)

    assert 'You cannot spawn additional base!' in str(exc.value)


def test_spawn_on_edge(game_control_proxy, defender):
    with pytest.raises(IllegalActionException) as exc:
        si = SpawnInformation(defender, GameObjectType.ARCHER, OffsetPosition(-1, -2), [], [])
        game_control_proxy.spawn_unit(si)

    assert 'Cannot spawn unit defender unit on the map edge.' in str(exc.value)


def test_spawn_different_role(game_control_proxy, defender):
    with pytest.raises(IllegalActionException) as exc:
        si = SpawnInformation(defender, GameObjectType.DEMON, OffsetPosition(1, 1), [], [])
        game_control_proxy.spawn_unit(si)

    assert 'Attempt to spawn unit of different role!' in str(exc.value)


def test_spawn_insufficient_resources(game_control_proxy, defender):
    flexmock(Ent).should_receive('cost').and_return(5000)
    with pytest.raises(IllegalActionException) as exc:
        si = SpawnInformation(defender, GameObjectType.ENT, OffsetPosition(1, 1), [], [])
        game_control_proxy.spawn_unit(si)

    assert 'Insufficient resources!' in str(exc.value)
