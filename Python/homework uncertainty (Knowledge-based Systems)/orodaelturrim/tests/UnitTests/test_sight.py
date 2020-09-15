import pytest

from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Structure.Enums import Nudge
from OrodaelTurrim.Structure.Position import OffsetPosition


@pytest.mark.parametrize('start,end,sight,result', [
    (OffsetPosition(0, 0), OffsetPosition(0, 0), 0, True),
    (OffsetPosition(0, 0), OffsetPosition(0, -1), 1, True),
    (OffsetPosition(0, 0), OffsetPosition(1, -2), 2, False),
])
def test_can_been_seen(start, end, sight, result, game_map):
    assert game_map.can_been_seen(start, end, sight, Nudge.POSITIVE) == result


ZERO_SIGHT = [
    OffsetPosition(0, 0)
]

ONE_SIGHT = [OffsetPosition(0, -1),
             OffsetPosition(0, 1),
             OffsetPosition(-1, 0),
             OffsetPosition(-1, -1),
             OffsetPosition(1, 0),
             OffsetPosition(1, -1),
             ] + ZERO_SIGHT

TWO_SIGHT = [
                OffsetPosition(-2, 0),
                OffsetPosition(-2, -1),
                OffsetPosition(-1, -2),
                OffsetPosition(1, -2),
                OffsetPosition(2, -1),
                OffsetPosition(2, 0),
                OffsetPosition(2, 1),
                OffsetPosition(1, 1),
                OffsetPosition(0, 2),
                OffsetPosition(-1, 1),
            ] + ONE_SIGHT

THREE_SIGHT = [
                  OffsetPosition(-2, -2),
                  OffsetPosition(2, 2)
              ] + TWO_SIGHT

FOUR_SIGHT = [
                 OffsetPosition(1, 2)
             ] + THREE_SIGHT

FIVE_SIGHT = [
                 OffsetPosition(2, -2)
             ] + FOUR_SIGHT


@pytest.mark.parametrize('sight,result', [
    (0, ZERO_SIGHT),
    (1, ONE_SIGHT),
    (2, TWO_SIGHT),
    (3, THREE_SIGHT),
    (4, FOUR_SIGHT),
    (5, FIVE_SIGHT)
])
def test_visible_tiles(sight, result, game_map: GameMap, utils):
    visible = game_map.get_visible_tiles(OffsetPosition(0, 0), sight)

    assert utils.compare_position_list(visible, result)


ZERO_ACCESS = [
    OffsetPosition(0, 0)
]

ONE_ACCESS = [
                 OffsetPosition(-1, -1),
                 OffsetPosition(1, -1),
                 OffsetPosition(1, 0),
             ] + ZERO_ACCESS

TWO_ACCESS = [
                 OffsetPosition(0, 1),
                 OffsetPosition(-1, -2)
             ] + ONE_ACCESS

THREE_ACCESS = [
                   OffsetPosition(-1, 0),
                   OffsetPosition(-2, 0),
                   OffsetPosition(0, -1),
                   OffsetPosition(0, -2),
                   OffsetPosition(1, -2),
                   OffsetPosition(2, 0),
                   OffsetPosition(2, 1),
                   OffsetPosition(1, 1),
               ] + TWO_ACCESS

FOUR_ACCESS = [
                  OffsetPosition(-2, -1),
                  OffsetPosition(-2, -2),
                  OffsetPosition(2, -2),
                  OffsetPosition(2, -1),
                  OffsetPosition(0, 2),
                  OffsetPosition(-1, 1),
                  OffsetPosition(-2, 1),
              ] + THREE_ACCESS

FIVE_ACCESS = [
                  OffsetPosition(2, 2),
                  OffsetPosition(1, 2),
                  OffsetPosition(-1, 2),
              ] + FOUR_ACCESS

SIX_ACCESS = [
                 OffsetPosition(-2, 2)
             ] + FIVE_ACCESS


@pytest.mark.parametrize('actions,result', [
    (0, ZERO_ACCESS),
    (1, ONE_ACCESS),
    (2, TWO_ACCESS),
    (3, THREE_ACCESS)
])
def test_accessible_ties(actions, result, game_map: GameMap, utils):
    accessible_tiles = game_map.get_accessible_tiles(OffsetPosition(0, 0), actions)

    assert utils.compare_position_list(accessible_tiles.keys(), result)
