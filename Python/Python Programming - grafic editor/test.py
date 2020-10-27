import pytest
import Image as img
from PIL import Image
import numpy as np


def test_rotation():
    target = np.array(Image.open('im.jpg'))
    result = target.copy()
    for _ in range(4):
        result = img.rotate(result)

    assert np.array_equal(target, result) is True


def test_mirror():
    target = np.array(Image.open('im.jpg'))
    result = target.copy()
    for _ in range(2):
        result = img.mirror(result)

    assert np.array_equal(target, result) is True


def test_negative():
    target = np.array(Image.open('im.jpg'))
    result = target.copy()
    for _ in range(2):
        result = img.negative(result)

    assert np.array_equal(target, result) is True


def test_lighten():
    target = np.array(Image.open('im.jpg'))
    result = target.copy()
    result = img.lighten(result, 0)

    assert np.array_equal(target, result) is True


def test_darken():
    target = np.array(Image.open('im.jpg'))
    result = target.copy()
    result = img.darken(result, 100)

    assert np.array_equal(target, result) is True


def test():
    target = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ])
    rotate = np.array([
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3],
    ])
    mirror = np.array([
        [3, 2, 1],
        [6, 5, 4],
        [9, 8, 7],
    ])
    inverse = np.array([
        [254, 253, 252],
        [251, 250, 249],
        [248, 247, 246],
    ])
    lighten = np.array([
        [1, 3, 4],
        [6, 7, 9],
        [10, 12, 13],
    ])
    darken = np.array([
        [0, 1, 1],
        [2, 2, 3],
        [3, 4, 4],
    ])
    sharp = np.array([
        [0, 1, 7],
        [7, 5, 13],
        [23, 19, 31],
    ])
    assert np.array_equal(rotate, img.rotate(target)) is True
    assert np.array_equal(mirror, img.mirror(target)) is True
    assert np.array_equal(inverse, img.negative(target)) is True
    assert np.array_equal(lighten, img.lighten(target, 50)) is True
    assert np.array_equal(darken, img.darken(target, 50)) is True
    assert np.array_equal(sharp, img.sharpening(target)) is True
