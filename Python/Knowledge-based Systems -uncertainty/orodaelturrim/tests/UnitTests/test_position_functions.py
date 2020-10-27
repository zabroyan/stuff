import pytest

from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Structure.Position import OffsetPosition, CubicPosition


@pytest.mark.parametrize('position,result', [
    (OffsetPosition(0, 0), [OffsetPosition(0, -1), OffsetPosition(1, -1),
                            OffsetPosition(1, 0), OffsetPosition(0, 1),
                            OffsetPosition(-1, 0), OffsetPosition(-1, -1)]),
    (OffsetPosition(-4, 4), [OffsetPosition(-4, 3), OffsetPosition(-3, 3),
                             OffsetPosition(-3, 4), OffsetPosition(-4, 5),
                             OffsetPosition(-5, 4), OffsetPosition(-5, 3)]),
    (OffsetPosition(-5, 5), [OffsetPosition(-5, 4), OffsetPosition(-4, 5),
                             OffsetPosition(-4, 6), OffsetPosition(-5, 6),
                             OffsetPosition(-6, 6), OffsetPosition(-6, 5)]),
    (OffsetPosition(3, 2), [OffsetPosition(3, 1), OffsetPosition(4, 2),
                            OffsetPosition(4, 3), OffsetPosition(3, 3),
                            OffsetPosition(2, 3), OffsetPosition(2, 2)])
])
def test_neighbour_offset(position, result):
    assert position.get_all_neighbours() == result


@pytest.mark.parametrize('position,result', [
    (CubicPosition(0, 0, 0), [CubicPosition(0, 1, -1), CubicPosition(1, 0, -1),
                              CubicPosition(1, -1, 0), CubicPosition(0, -1, 1),
                              CubicPosition(-1, 0, 1), CubicPosition(-1, 1, 0)]),
    (CubicPosition(2, -4, 2), [CubicPosition(2, -3, 1), CubicPosition(3, -4, 1),
                               CubicPosition(3, -5, 2), CubicPosition(2, -5, 3),
                               CubicPosition(1, -4, 3), CubicPosition(1, -3, 2)]),
    (CubicPosition(-4, 6, -2), [CubicPosition(-4, 7, -3), CubicPosition(-3, 6, -3),
                                CubicPosition(-3, 5, -2), CubicPosition(-4, 5, -1),
                                CubicPosition(-5, 6, -1), CubicPosition(-5, 7, -2)]),
])
def test_neighbour_cubic(position, result):
    assert set(position.get_all_neighbours()) == set(result)


@pytest.mark.parametrize('position,state', [
    (OffsetPosition(-6, -6), False),
    (OffsetPosition(-5, -5), True),
    (OffsetPosition(6, 6), False),
    (OffsetPosition(5, 5), True),
    (OffsetPosition(-6, 6), False),
    (OffsetPosition(-5, 5), True),
    (OffsetPosition(6, -6), False),
    (OffsetPosition(5, -5), True),
    (OffsetPosition(0, 0), True),
])
def test_position_on_map(position, state):
    _map = GameMap(11, 11)
    assert _map.position_on_map(position) == state
