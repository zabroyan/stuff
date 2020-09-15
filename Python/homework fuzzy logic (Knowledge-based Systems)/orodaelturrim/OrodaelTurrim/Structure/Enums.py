from enum import Enum
from typing import List, Optional

from OrodaelTurrim.Structure.Position import CubicPosition, AxialPosition, OffsetPosition
from OrodaelTurrim.Structure.Terrain import Field, Forest, Hill, Mountain, River, Village


class AutoNumber(Enum):
    """ Subclass of Enum to automatic number value generate"""


    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class TerrainType(Enum):
    """ Types of terrains on map"""
    FIELD = Field()
    FOREST = Forest()
    HILL = Hill()
    MOUNTAIN = Mountain()
    RIVER = River()
    VILLAGE = Village()


    @staticmethod
    def from_char(char: str) -> Optional["TerrainType"]:
        for terrain_type in TerrainType:
            if terrain_type.value.char() == char:
                return terrain_type
        return None


    @staticmethod
    def from_string(string: str) -> Optional['TerrainType']:
        for terrain_type in TerrainType:
            if str(terrain_type.name).lower() == string.lower():
                return terrain_type
        return None


class Nudge(Enum):
    """ Nudge position to one direction for line draw purpose """
    POSITIVE = 1
    NEGATIVE = -1


    def nudge(self, value: float) -> float:
        return self.value * value


class HexDirection(Enum):
    """ Direction of neighbours on hexagon grid defined with Cubic position"""
    UPPER = CubicPosition(0, 1, -1)
    RIGHT_UPPER = CubicPosition(1, 0, -1)
    RIGHT_LOWER = CubicPosition(1, -1, 0)
    LOWER = CubicPosition(0, -1, 1)
    LEFT_LOWER = CubicPosition(-1, 0, 1)
    LEFT_UPPER = CubicPosition(-1, 1, 0)


    @staticmethod
    def direction_list():
        return [HexDirection.UPPER, HexDirection.RIGHT_UPPER, HexDirection.RIGHT_LOWER, HexDirection.LOWER,
                HexDirection.LEFT_LOWER, HexDirection.LEFT_UPPER]


class AxialDirection(Enum):
    """ Direction of neighbours on hexagon grid defined with Axial position"""
    UPPER = AxialPosition(0, -1)
    RIGHT_UPPER = AxialPosition(+1, -1)
    RIGHT_LOWER = AxialPosition(+1, 0)
    LOWER = AxialPosition(0, 1)
    LEFT_LOWER = AxialPosition(-1, 1)
    LEFT_UPPER = AxialPosition(-1, 0)


class OddOffsetDirection(Enum):
    """
    Direction of neighbours on hexagon grid defined with Offset position
    Be careful that directions are different for odd and even columns
    """
    UPPER = OffsetPosition(0, -1)
    RIGHT_UPPER = OffsetPosition(+1, -1)
    RIGHT_LOWER = OffsetPosition(+1, 0)
    LOWER = OffsetPosition(0, 1)
    LEFT_LOWER = OffsetPosition(-1, 0)
    LEFT_UPPER = OffsetPosition(-1, -1)


class EvenOffsetDirection(Enum):
    """
        Direction of neighbours on hexagon grid defined with Offset position
        Be careful that directions are different for odd and even columns
    """
    UPPER = OffsetPosition(0, -1)
    RIGHT_UPPER = OffsetPosition(+1, 0)
    RIGHT_LOWER = OffsetPosition(+1, +1)
    LOWER = OffsetPosition(0, 1)
    LEFT_LOWER = OffsetPosition(-1, 1)
    LEFT_UPPER = OffsetPosition(-1, 0)


class EffectType(AutoNumber):
    """
    List of all effect that could units cause

    * BLIND - reduce sight to half
    * BURN - remove 5 HP each round
    * FREEZE - reduce actions to half and reduce defence by 25%
    * ROOT - reduce attack power to half
    """
    BLIND = ()
    BURN = ()
    FREEZE = ()
    ROOT = ()


class AttributeType(AutoNumber):
    """
    Enum for all attributes of unit

    * ACTIONS - Used for unit movement. Moving from terrain to terrain cost difference amount of actions
    * ATTACK - Attack power, compute attack life cost based on defender armor
    * DEFENSE - Define armor of the unit, subtract from attack number
    * HIT_POINTS - maximum hit points
    * ATTACK_RANGE - how far unit could attack, same computation as sight
    * SIGHT - How far unit see, some tiles cost more than 1 sight
    """
    ACTIONS = ()
    ATTACK = ()
    DEFENSE = ()
    HIT_POINTS = ()
    ATTACK_RANGE = ()
    SIGHT = ()


class GameRole(AutoNumber):
    """ Enum for partition users to attacker and defenders """
    ATTACKER = ()
    DEFENDER = ()
    NEUTRAL = ()


    def is_enemy(self, role: "GameRole") -> bool:
        """
        Determinate if target role is enemy for me
        :param role: target role
        :return: True if target is enemy, False otherwise
        """
        if self == role or self == GameRole.NEUTRAL or role == GameRole.NEUTRAL:
            return False
        return True


class GameObjectType(Enum):
    """
    Enum for all units. Enum is tuple of GameRole, place cost and ID
    """
    NONE = (GameRole.NEUTRAL, 1)
    BASE = (GameRole.DEFENDER, 2)

    ARCHER = (GameRole.DEFENDER, 3)
    DRUID = (GameRole.DEFENDER, 4)
    ENT = (GameRole.DEFENDER, 5)
    KNIGHT = (GameRole.DEFENDER, 6)
    MAGICIAN = (GameRole.DEFENDER, 7)

    CYCLOPS = (GameRole.ATTACKER, 8)
    DEMON = (GameRole.ATTACKER, 9)
    ELEMENTAL = (GameRole.ATTACKER, 10)
    GARGOYLE = (GameRole.ATTACKER, 11)
    MINOTAUR = (GameRole.ATTACKER, 12)
    NECROMANCER = (GameRole.ATTACKER, 13)
    ORC = (GameRole.ATTACKER, 14)
    SKELETON = (GameRole.ATTACKER, 15)


    @staticmethod
    def defenders() -> List["GameObjectType"]:
        """ Get list of all defender unit """
        return [x for x in list(GameObjectType) if x.value[0] == GameRole.DEFENDER]


    @staticmethod
    def attackers() -> List["GameObjectType"]:
        """ Get list of all attacker units"""
        return [x for x in list(GameObjectType) if x.value[0] == GameRole.ATTACKER]


    @property
    def price(self) -> int:
        """ Return price of the unit """
        from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototypePool
        return GameObjectPrototypePool[self].COST


    @property
    def role(self) -> GameRole:
        """ Return role of the unit """
        return self.value[0]


class GameOverStates(AutoNumber):
    """ Enum for what to do after Game is over """
    FIND_REASON = ()
    LET_HIM_DIE = ()
