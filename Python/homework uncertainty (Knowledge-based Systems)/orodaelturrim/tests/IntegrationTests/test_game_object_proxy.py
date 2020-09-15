import pytest

from OrodaelTurrim.Structure.Enums import AttributeType, EffectType, GameObjectType, GameRole
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition


@pytest.fixture(scope='module')
def game_object_proxy(game_instance):

    return game_instance[1]


@pytest.mark.parametrize('position,attribute,value', [
    (OffsetPosition(0, 0), AttributeType.ATTACK, 5),
    (OffsetPosition(-1, -1), AttributeType.ATTACK, 25),
    (OffsetPosition(1, -1), AttributeType.ATTACK, None),
    (OffsetPosition(0, -2), AttributeType.ATTACK, None),
])
def test_get_attribute(game_object_proxy, position, attribute, value):
    assert game_object_proxy.get_attribute(position, attribute) == value


@pytest.mark.parametrize('position,value', [
    (OffsetPosition(0, 0), 500),
    (OffsetPosition(-1, -1), 150),
    (OffsetPosition(1, -1), None),
    (OffsetPosition(0, -2), None),
])
def test_get_current_hit_points(game_object_proxy, position, value):
    assert game_object_proxy.get_current_hit_points(position) == value


@pytest.mark.parametrize('position,value', [
    (OffsetPosition(0, 0), set()),
    (OffsetPosition(-1, -1), {EffectType.BURN}),
    (OffsetPosition(1, -1), None),
    (OffsetPosition(0, -2), None),
])
def test_get_attack_effects(game_object_proxy, position, value):
    assert game_object_proxy.get_attack_effects(position) == value


@pytest.mark.parametrize('position,value', [
    (OffsetPosition(0, 0), {EffectType.BLIND}),
    (OffsetPosition(-1, -1), {EffectType.BURN, EffectType.FREEZE}),
    (OffsetPosition(1, -1), None),
    (OffsetPosition(0, -2), None),
])
def test_get_resistances(game_object_proxy, position, value):
    assert game_object_proxy.get_resistances(position) == value


@pytest.mark.parametrize('position,value', [
    (OffsetPosition(0, 0), {}),
    (OffsetPosition(-1, -1), {}),
    (OffsetPosition(1, -1), None),
    (OffsetPosition(0, -2), None),
])
def test_get_active_effects(game_object_proxy, position, value):
    assert game_object_proxy.get_active_effects(position) == value


@pytest.mark.parametrize('position,value', [
    (OffsetPosition(0, 0), GameObjectType.BASE),
    (OffsetPosition(-1, -1), GameObjectType.DEMON),
    (OffsetPosition(1, -1), GameObjectType.NONE),
    (OffsetPosition(0, -2), None),
])
def test_get_object_type(game_object_proxy, position, value):
    assert game_object_proxy.get_object_type(position) == value


@pytest.mark.parametrize('position,value', [
    (OffsetPosition(0, 0), GameRole.DEFENDER),
    (OffsetPosition(-1, -1), GameRole.ATTACKER),
    (OffsetPosition(1, -1), GameRole.NEUTRAL),
    (OffsetPosition(0, -2), None),
])
def test_get_role(game_object_proxy, position, value):
    assert game_object_proxy.get_role(position) == value


@pytest.mark.parametrize('position,value', [
    (OffsetPosition(0, 0), {
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
    }),
    (OffsetPosition(1, -1), None),
    (OffsetPosition(0, -2), None),
])
def test_get_visible_tiles(game_object_proxy, position, value):
    assert game_object_proxy.get_visible_tiles(position) == value


@pytest.mark.parametrize('position,value', [
    (OffsetPosition(0, 0), {OffsetPosition(-1, -1): 1}),
    (OffsetPosition(-1, -1), {OffsetPosition(0, 0): 1}),
    (OffsetPosition(1, -1), None),
    (OffsetPosition(0, -2), None),
])
def test_get_visible_enemies(game_object_proxy, position, value):
    assert game_object_proxy.get_visible_enemies(position) == value


def test_get_income(game_object_proxy, defender, attacker):
    assert game_object_proxy.get_income(defender) == 10
    assert game_object_proxy.get_income(attacker) == 0


def test_get_resources(game_object_proxy, defender, attacker):
    assert game_object_proxy.get_resources(defender) == 1000
    assert game_object_proxy.get_resources(attacker) == 40
