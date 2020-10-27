from OrodaelTurrim import IMAGES_ROOT, ICONS_ROOT
from OrodaelTurrim.Structure.Enums import GameObjectType, TerrainType
from OrodaelTurrim.Structure.Actions.Combat import MoveAction, AttackAction
from OrodaelTurrim.Structure.Actions.Log import LogAction
from OrodaelTurrim.Structure.Actions.Placement import SpawnAction
from OrodaelTurrim.Structure.Actions.Resources import SpendResourcesAction, EarnResourcesAction, IncomeResourcesIncrease
from OrodaelTurrim.Structure.Actions.Terrain import TerrainDamageAction


class GetMetaAssets(type):
    """ Meta class that add getitem on assets dict on static class """


    def __getitem__(self, item):
        try:
            return AssetsEncoder.assets[item]
        except KeyError:
            return ''


class GetMetaIcons(type):
    """ Meta class that add getitem on assets dict on static class """


    def __getitem__(self, item):
        try:
            return IconEncoder.assets[item.__class__.__name__]
        except KeyError:
            return None


class AssetsEncoder(metaclass=GetMetaAssets):
    """ Decode GameObjectType Enum to image """
    assets = {
        GameObjectType.ARCHER: IMAGES_ROOT / 'Objects' / 'archer.png',
        GameObjectType.BASE: IMAGES_ROOT / 'Objects' / 'base.png',
        GameObjectType.DRUID: IMAGES_ROOT / 'Objects' / 'druid.png',
        GameObjectType.ENT: IMAGES_ROOT / 'Objects' / 'ent.png',
        GameObjectType.KNIGHT: IMAGES_ROOT / 'Objects' / 'knight.png',
        GameObjectType.MAGICIAN: IMAGES_ROOT / 'Objects' / 'magician.png',

        GameObjectType.CYCLOPS: IMAGES_ROOT / 'Objects' / 'cyclops.png',
        GameObjectType.DEMON: IMAGES_ROOT / 'Objects' / 'demon.png',
        GameObjectType.ELEMENTAL: IMAGES_ROOT / 'Objects' / 'elemental.png',
        GameObjectType.GARGOYLE: IMAGES_ROOT / 'Objects' / 'gargoyle.png',
        GameObjectType.MINOTAUR: IMAGES_ROOT / 'Objects' / 'minotaur.png',
        GameObjectType.NECROMANCER: IMAGES_ROOT / 'Objects' / 'necromancer.png',
        GameObjectType.ORC: IMAGES_ROOT / 'Objects' / 'orc.png',
        GameObjectType.SKELETON: IMAGES_ROOT / 'Objects' / 'skeleton.png',

        TerrainType.FIELD: IMAGES_ROOT / 'Terrain' / 'field.png',
        TerrainType.FOREST: IMAGES_ROOT / 'Terrain' / 'forest.png',
        TerrainType.HILL: IMAGES_ROOT / 'Terrain' / 'hill.png',
        TerrainType.MOUNTAIN: IMAGES_ROOT / 'Terrain' / 'mountain.png',
        TerrainType.RIVER: IMAGES_ROOT / 'Terrain' / 'river_0-2.png',
        TerrainType.VILLAGE: IMAGES_ROOT / 'Terrain' / 'village.png',

        'river_0-2': IMAGES_ROOT / 'Terrain' / 'river_0-2.png',
        'river_0-3': IMAGES_ROOT / 'Terrain' / 'river_0-3.png',
        'river_0-4': IMAGES_ROOT / 'Terrain' / 'river_0-4.png',
        'river_1-3': IMAGES_ROOT / 'Terrain' / 'river_1-3.png',
        'river_1-4': IMAGES_ROOT / 'Terrain' / 'river_1-4.png',
        'river_1-5': IMAGES_ROOT / 'Terrain' / 'river_1-5.png',
        'river_2-4': IMAGES_ROOT / 'Terrain' / 'river_2-4.png',
        'river_2-5': IMAGES_ROOT / 'Terrain' / 'river_2-5.png',
        'river_3-5': IMAGES_ROOT / 'Terrain' / 'river_3-5.png',

    }


class IconEncoder(metaclass=GetMetaIcons):
    assets = {
        MoveAction.__name__: ICONS_ROOT / 'log' / 'horse.png',
        AttackAction.__name__: ICONS_ROOT / 'log' / 'sword.png',

        SpendResourcesAction.__name__: ICONS_ROOT / 'log' / 'money.png',
        EarnResourcesAction.__name__: ICONS_ROOT / 'log' / 'money.png',
        IncomeResourcesIncrease: ICONS_ROOT / 'log' / 'money.png',

        LogAction.__name__: ICONS_ROOT / 'log' / 'log.png',
        SpawnAction.__name__: ICONS_ROOT / 'log' / 'unit.png',

        TerrainDamageAction.__name__: ICONS_ROOT / 'log' / 'mountain.png',


    }
