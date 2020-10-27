from abc import ABC, abstractmethod
from typing import Set

from OrodaelTurrim import IMAGES_ROOT
from OrodaelTurrim.Structure.Enums import GameObjectType, GameRole, AttributeType, EffectType
from OrodaelTurrim.Structure.GameObjects.Attributes import AttributeBundle


class GameObjectPrototype(ABC):
    """ Represents core of game object prototypes """
    ASSET_FORMAT = '.png'
    ASSET_FOLDER = IMAGES_ROOT / 'Objects'


    def __init__(self, attributes: AttributeBundle, cost: int, object_type: GameObjectType, role: GameRole,
                 asset_name: str):
        self.__attributes = attributes
        self.__cost = cost
        self.__object_type = object_type
        self.__role = role
        self.__asset_name = asset_name


    def get_attribute_value(self, attribute_type: AttributeType) -> float:
        """ Get value based on attribute type """
        try:
            return getattr(self.__attributes, attribute_type.name.lower())
        except AttributeError:
            print('Unknown type of attribute - {}!'.format(attribute_type))
            return 0.0


    @property
    def cost(self) -> int:
        """ Cost of deploying instance of this prototype """
        return self.__cost


    @property
    def object_type(self) -> GameObjectType:
        """ Type of this game object """
        return self.__object_type


    @property
    def role(self) -> GameRole:
        """ Role of this game object """
        return self.__role


    @property
    @abstractmethod
    def attack_effects(self) -> Set[EffectType]:
        """
        Retrieves attack effects of this prototype
        :return: Set of effects, which should get applied on attack of unit of this prototype
        """
        pass


    @property
    @abstractmethod
    def resistances(self) -> Set[EffectType]:
        """
        Retrieves resistances of this prototype
        :return: Set of effects, which will get ignored, when effects are applied to unit of this prototype
        """
        pass


    @property
    def description(self) -> str:
        """ Text description of the unit attributes with current HP"""
        return '''        
        <table>
            <tr>
                <td> Actions: </td> <td> {} </td>
            </tr>
            <tr>
                <td> Attack: </td>       <td>{}</td>
            </tr>
            <tr>        
                <td> Defense: </td>      <td>{}</td>
            </tr>
            <tr>
                <td> Range: </td> <td>{}</td>
            </tr>
            <tr>
                <td> Sight: </td>        <td>{}</td>
            </tr>
            <tr>
                <td> Max HP: </td>   <td>{:0.1f}</td>
            </tr>
            <tr>
                <td style="padding-right:8px;"> Current HP: </td>   <td>{{:0.1f}}</td>
            </tr>
        </table>'''.format(
            self.get_attribute_value(AttributeType.ACTIONS),
            self.get_attribute_value(AttributeType.ATTACK),
            self.get_attribute_value(AttributeType.DEFENSE),
            self.get_attribute_value(AttributeType.ATTACK_RANGE),
            self.get_attribute_value(AttributeType.SIGHT),
            self.get_attribute_value(AttributeType.HIT_POINTS))


    @property
    def description_static(self):
        """ Text description of the unit attributes with without HP"""
        return '''        
                <table>
                    <tr>
                        <td> Actions: </td> <td> {} </td>
                    </tr>
                    <tr>
                        <td> Attack: </td>       <td>{}</td>
                    </tr>
                    <tr>        
                        <td> Defense: </td>      <td>{}</td>
                    </tr>
                    <tr>
                        <td> Range: </td> <td>{}</td>
                    </tr>
                    <tr>
                        <td> Sight: </td>        <td>{}</td>
                    </tr>
                    <tr>
                        <td> Max HP: </td>   <td>{:0.1f}</td>
                    </tr>
                </table>'''.format(
            self.get_attribute_value(AttributeType.ACTIONS),
            self.get_attribute_value(AttributeType.ATTACK),
            self.get_attribute_value(AttributeType.DEFENSE),
            self.get_attribute_value(AttributeType.ATTACK_RANGE),
            self.get_attribute_value(AttributeType.SIGHT),
            self.get_attribute_value(AttributeType.HIT_POINTS))


class GetMeta(type):
    """ Return Game object instance from Prototype pool based on Enum GameObjectType """
    def __getitem__(self, item: GameObjectType):
        return GameObjectPrototypePool.prototypes[item]


class GameObjectPrototypePool(metaclass=GetMeta):
    """ Holds the prototypes of game object classes """
    from OrodaelTurrim.Structure.GameObjects.Prototypes.Attackers import Cyclops, Demon, Elemental, Gargoyle, \
        Minotaur, Necromancer, Orc, Skeleton
    from OrodaelTurrim.Structure.GameObjects.Prototypes.Defenders import Base, Archer, Druid, Ent, Knight, Magician
    prototypes = {
        GameObjectType.BASE: Base(),
        GameObjectType.ARCHER: Archer(),
        GameObjectType.DRUID: Druid(),
        GameObjectType.ENT: Ent(),
        GameObjectType.KNIGHT: Knight(),
        GameObjectType.MAGICIAN: Magician(),

        GameObjectType.CYCLOPS: Cyclops(),
        GameObjectType.DEMON: Demon(),
        GameObjectType.ELEMENTAL: Elemental(),
        GameObjectType.GARGOYLE: Gargoyle(),
        GameObjectType.MINOTAUR: Minotaur(),
        GameObjectType.NECROMANCER: Necromancer(),
        GameObjectType.ORC: Orc(),
        GameObjectType.SKELETON: Skeleton()
    }
