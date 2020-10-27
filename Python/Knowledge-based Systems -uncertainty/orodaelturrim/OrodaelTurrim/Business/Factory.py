from typing import TYPE_CHECKING, Set, Optional, Dict

from PyQt5.QtGui import QColor

from OrodaelTurrim.Structure.Enums import EffectType, HexDirection
from OrodaelTurrim.Structure.GameObjects.Effect import Burn, Blind, Freeze, Root, Effect
from OrodaelTurrim.Structure.Map import Border

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Position import Position


class EffectFactory:
    """ Factory for easy Effect creation """


    @staticmethod
    def create(effect_type: EffectType) -> Optional[Effect]:
        """
        Create effect instance by Effect type Enum

        :param effect_type: Efect type Enum
        :return: Effect type instance of None if value doesn't exist
        """
        if effect_type == EffectType.BURN:
            return Burn()

        elif effect_type == EffectType.BLIND:
            return Blind()

        elif effect_type == EffectType.FREEZE:
            return Freeze()

        elif effect_type == EffectType.ROOT:
            return Root()

        else:
            return None


class BorderFactory:
    """
    Border factory for easy border structures creation.
    """


    @staticmethod
    def create(weight: int, color: QColor, positions: Set["Position"]) -> Dict["Position", Border]:
        """
        Create boarder over many tiles.

        :param weight: Weight of the line
        :param color:  Color of the line
        :param positions: Set of positions which should be  enclose with border

        :return: Dictionary acceptable by Map class
        """
        borders_dict = {}
        for position in positions:
            directions = {}
            for direction in HexDirection.direction_list():
                if position.cubic + direction.value not in positions:
                    directions[direction.name.lower()] = weight
            directions['color'] = color
            borders_dict[position] = Border(**directions)

        return borders_dict
