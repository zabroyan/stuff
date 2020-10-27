import pytest

from OrodaelTurrim.Structure.Enums import TerrainType, GameObjectType
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition


@pytest.fixture(scope='module')
def map_proxy(game_instance):
    return game_instance[0]


def test_map_height(map_proxy):
    assert map_proxy.get_map_height() == 5


def test_map_width(map_proxy):
    assert map_proxy.get_map_height() == 5


@pytest.mark.parametrize('position,terrain', [
    (OffsetPosition(-1, -1), TerrainType.FIELD),
    (OffsetPosition(-2, 1), TerrainType.VILLAGE),
])
def test_get_terrain_type(map_proxy, position, terrain):
    assert map_proxy.get_terrain_type(position) == terrain


@pytest.mark.parametrize('position,result', [
    (OffsetPosition(-1, -1), True),
    (OffsetPosition(0, 0), True),
    (OffsetPosition(0, -3), False),
])
def test_is_position_on_map(map_proxy, position, result):
    assert map_proxy.is_position_on_map(position) == result


@pytest.mark.parametrize('position,result', [
    (OffsetPosition(-1, -1), True),
    (OffsetPosition(0, 0), True),
    (OffsetPosition(0, -1), False),
    (OffsetPosition(0, -2), None),
])
def test_is_position_occupied(map_proxy, position, result):
    assert map_proxy.is_position_occupied(position) == result


def test_get_bases_positions(map_proxy):
    assert map_proxy.get_bases_positions() == {OffsetPosition(0, 0)}


def test_get_border_tiles(map_proxy):
    assert map_proxy.get_border_tiles() == {
        OffsetPosition(-2, -2),
        OffsetPosition(-1, -2),
        OffsetPosition(0, -2),
        OffsetPosition(1, -2),
        OffsetPosition(2, -2),
        OffsetPosition(2, -1),
        OffsetPosition(2, 0),
        OffsetPosition(2, 1),
        OffsetPosition(2, 2),
        OffsetPosition(1, 2),
        OffsetPosition(0, 2),
        OffsetPosition(-1, 2),
        OffsetPosition(-2, 2),
        OffsetPosition(-2, 1),
        OffsetPosition(-2, 0),
        OffsetPosition(-2, -1),
    }


def test_get_player_visible_tiles(map_proxy):
    assert map_proxy.get_player_visible_tiles() == {
        OffsetPosition(-2, -1),
        OffsetPosition(-1, -2),
        OffsetPosition(-2, 0),
        OffsetPosition(-1, -1),
        OffsetPosition(0, -1),
        OffsetPosition(1, -2),
        OffsetPosition(-1, 0),
        OffsetPosition(0, 0),
        OffsetPosition(1, -1),
        OffsetPosition(2, -1),
        OffsetPosition(-1, 1),
        OffsetPosition(0, 1),
        OffsetPosition(1, 0),
        OffsetPosition(2, 0),
        OffsetPosition(0, 2),
        OffsetPosition(1, 1),
        OffsetPosition(2, 1),
    }


def test_compute_visible_tiles(map_proxy):
    assert map_proxy.compute_visible_tiles(OffsetPosition(0, 0), 2) == {
        OffsetPosition(-2, -1),
        OffsetPosition(-1, -2),
        OffsetPosition(-2, 0),
        OffsetPosition(-1, -1),
        OffsetPosition(0, -1),
        OffsetPosition(1, -2),
        OffsetPosition(-1, 0),
        OffsetPosition(0, 0),
        OffsetPosition(1, -1),
        OffsetPosition(2, -1),
        OffsetPosition(-1, 1),
        OffsetPosition(0, 1),
        OffsetPosition(1, 0),
        OffsetPosition(2, 0),
        OffsetPosition(0, 2),
        OffsetPosition(1, 1),
        OffsetPosition(2, 1),
    }


def test_compute_accessible_tiles(map_proxy):
    assert map_proxy.compute_accessible_tiles(OffsetPosition(0, 0), 2) == {
        OffsetPosition(-1, -2): 0,
        OffsetPosition(-1, -1): 1,
        OffsetPosition(1, -1) : 1,
        OffsetPosition(1, 0)  : 0,
        OffsetPosition(0, 1)  : 0,
        OffsetPosition(0, 0)  : 2,
    }


def test_player_have_base(map_proxy, defender):
    assert map_proxy.player_have_base(defender)
