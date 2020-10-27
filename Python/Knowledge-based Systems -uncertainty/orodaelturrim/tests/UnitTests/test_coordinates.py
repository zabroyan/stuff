from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Structure.Position import *
import pytest
from OrodaelTurrim.Structure.Enums import HexDirection


@pytest.mark.parametrize('cube,offset', [
    (CubicPosition(-2, 3, -1), OffsetPosition(-2, -2)),
    (CubicPosition(-2, -1, 3), OffsetPosition(-2, +2)),
    (CubicPosition(2, -3, 1), OffsetPosition(2, 2)),
    (CubicPosition(2, 1, -3), OffsetPosition(2, -2)),
    (CubicPosition(0, 0, 0), OffsetPosition(0, 0))
])
def test_cubic_to_offset(cube, offset):
    assert cube.offset == offset


@pytest.mark.parametrize('cube,offset', [
    (CubicPosition(-2, 3, -1), OffsetPosition(-2, -2)),
    (CubicPosition(-2, -1, 3), OffsetPosition(-2, +2)),
    (CubicPosition(2, -3, 1), OffsetPosition(2, 2)),
    (CubicPosition(2, 1, -3), OffsetPosition(2, -2)),
    (CubicPosition(0, 0, 0), OffsetPosition(0, 0))
])
def test_offset_to_cubic(cube, offset):
    assert offset.cubic == cube


@pytest.mark.parametrize('cube,axial', [
    (CubicPosition(-2, 2, 0), AxialPosition(-2, 0)),
    (CubicPosition(-2, 0, 2), AxialPosition(-2, 2)),
    (CubicPosition(2, -2, 0), AxialPosition(2, 0)),
    (CubicPosition(+2, 0, -2), AxialPosition(+2, -2)),
    (CubicPosition(0, 0, 0), AxialPosition(0, 0))
])
def test_axial_to_cubic(cube, axial):
    assert axial.cubic == cube


@pytest.mark.parametrize('cube,axial', [
    (CubicPosition(-2, 2, 0), AxialPosition(-2, 0)),
    (CubicPosition(-2, 0, 2), AxialPosition(-2, 2)),
    (CubicPosition(2, -2, 0), AxialPosition(2, 0)),
    (CubicPosition(+2, 0, -2), AxialPosition(+2, -2)),
    (CubicPosition(0, 0, 0), AxialPosition(0, 0))
])
def test_cubic_to_axial(cube, axial):
    assert axial == cube.axial





@pytest.mark.parametrize('position1, position2,result', [
    (CubicPosition(0, 0, 0), HexDirection.UPPER, CubicPosition(0, 1, -1)),
    (CubicPosition(0, 0, 0), HexDirection.RIGHT_UPPER, CubicPosition(1, 0, -1)),
    (CubicPosition(0, 0, 0), HexDirection.RIGHT_LOWER, CubicPosition(1, -1, 0)),
    (CubicPosition(0, 0, 0), HexDirection.LOWER, CubicPosition(0, -1, 1)),
    (CubicPosition(0, 0, 0), HexDirection.LEFT_LOWER, CubicPosition(-1, 0, 1)),
    (CubicPosition(0, 0, 0), HexDirection.LEFT_UPPER, CubicPosition(-1, 1, 0)),

    (CubicPosition(-4, -2, 6), HexDirection.UPPER, CubicPosition(-4, -1, 5)),
    (CubicPosition(-4, -2, 6), HexDirection.RIGHT_UPPER, CubicPosition(-3, -2, 5)),
    (CubicPosition(-4, -2, 6), HexDirection.RIGHT_LOWER, CubicPosition(-3, -3, 6)),
    (CubicPosition(-4, -2, 6), HexDirection.LOWER, CubicPosition(-4, -3, 7)),
    (CubicPosition(-4, -2, 6), HexDirection.LEFT_LOWER, CubicPosition(-5, -2, 7)),
    (CubicPosition(-4, -2, 6), HexDirection.LEFT_UPPER, CubicPosition(-5, -1, 6)),
])
def test_cubic_add_cubic(position1, position2, result):
    assert ((position1 + position2.value) == result)
    assert ((position2.value + position1) == result)


@pytest.mark.parametrize('position1, position2,result', [
    (OffsetPosition(0, 0), HexDirection.UPPER, CubicPosition(0, 1, -1)),
    (OffsetPosition(0, 0), HexDirection.RIGHT_UPPER, CubicPosition(1, 0, -1)),
    (OffsetPosition(0, 0), HexDirection.RIGHT_LOWER, CubicPosition(1, -1, 0)),
    (OffsetPosition(0, 0), HexDirection.LOWER, CubicPosition(0, -1, 1)),
    (OffsetPosition(0, 0), HexDirection.LEFT_LOWER, CubicPosition(-1, 0, 1)),
    (OffsetPosition(0, 0), HexDirection.LEFT_UPPER, CubicPosition(-1, 1, 0)),

    (OffsetPosition(-4, 4), HexDirection.UPPER, CubicPosition(-4, -1, 5)),
    (OffsetPosition(-4, 4), HexDirection.RIGHT_UPPER, CubicPosition(-3, -2, 5)),
    (OffsetPosition(-4, 4), HexDirection.RIGHT_LOWER, CubicPosition(-3, -3, 6)),
    (OffsetPosition(-4, 4), HexDirection.LOWER, CubicPosition(-4, -3, 7)),
    (OffsetPosition(-4, 4), HexDirection.LEFT_LOWER, CubicPosition(-5, -2, 7)),
    (OffsetPosition(-4, 4), HexDirection.LEFT_UPPER, CubicPosition(-5, -1, 6)),
])
def test_offset_add_cubic(position1, position2, result):
    assert ((position1 + position2.value) == result)
    assert ((position2.value + position1) == result)


@pytest.mark.parametrize('position1, position2,result', [
    (HexDirection.UPPER, OffsetPosition(0, 0), CubicPosition(0, 1, -1)),
    (HexDirection.RIGHT_UPPER, OffsetPosition(0, 0), CubicPosition(1, 0, -1)),
    (HexDirection.RIGHT_LOWER, OffsetPosition(0, 0), CubicPosition(1, -1, 0)),
    (HexDirection.LOWER, OffsetPosition(0, 0), CubicPosition(0, -1, 1)),
    (HexDirection.LEFT_LOWER, OffsetPosition(0, 0), CubicPosition(-1, 0, 1)),
    (HexDirection.LEFT_UPPER, OffsetPosition(0, 0), CubicPosition(-1, 1, 0)),

    (HexDirection.UPPER, OffsetPosition(-4, 4), CubicPosition(-4, -1, 5)),
    (HexDirection.RIGHT_UPPER, OffsetPosition(-4, 4), CubicPosition(-3, -2, 5)),
    (HexDirection.RIGHT_LOWER, OffsetPosition(-4, 4), CubicPosition(-3, -3, 6)),
    (HexDirection.LOWER, OffsetPosition(-4, 4), CubicPosition(-4, -3, 7)),
    (HexDirection.LEFT_LOWER, OffsetPosition(-4, 4), CubicPosition(-5, -2, 7)),
    (HexDirection.LEFT_UPPER, OffsetPosition(-4, 4), CubicPosition(-5, -1, 6)),
])
def test_cubic_add_offset(position1, position2, result):
    assert ((position1.value + position2) == result)
    assert ((position2 + position1.value) == result)
