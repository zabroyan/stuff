from typing import List

from OrodaelTurrim.Structure.Enums import GameObjectType, AttributeType
from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter
from OrodaelTurrim.Structure.Position import Position


class AttackBaseFilter(AttackFilter):
    """ Represents filter which prefers attacking base """


    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        return [x for x in tiles if self.game_object_proxy.get_object_type(position) == GameObjectType.BASE]


class AttackLeastVisibleFilter(AttackFilter):
    """ Represents filter which prefers attacking the unit which is closest to death (least HP) """


    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        min_hit_points = min([self.game_object_proxy.get_current_hit_points(x) for x in tiles])
        return [x for x in tiles if self.game_object_proxy.get_current_hit_points(x) == min_hit_points]


class AttackMostVulnerableFilter(AttackFilter):
    """ Represents filter which prefers attacking the most vulnerable unit (least defence) """


    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        min_defence = min([self.game_object_proxy.get_attribute(x, AttributeType.DEFENSE) for x in tiles])
        return [x for x in tiles if self.game_object_proxy.get_attribute(x, AttributeType.DEFENSE) == min_defence]


class AttackNearestFilter(AttackFilter):
    """ Represents filter which prefers attacking the nearest unit """


    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        min_distance = min([x.distance_from(position) for x in tiles])
        return [x for x in tiles if x.distance_from(position) == min_distance]


class AttackNoResistantFilter(AttackFilter):
    """
    Represents filter which prefers attacking units which are not resistant to attack effects
    of this game object (meaning at least one effect will get through)
    """


    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        attack_effect = self.game_object_proxy.get_attack_effects(position)
        if not attack_effect:
            return tiles

        filtered = []
        for tile in tiles:
            resistances = self.game_object_proxy.get_resistances(tile)
            if not all([x in attack_effect for x in resistances]):
                filtered.append(tile)

        return filtered


class AttackStrongestFilter(AttackFilter):
    """ Represents filter which prefers attacking the strongest unit (Maximum HP)"""
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        max_attack = max([self.game_object_proxy.get_attribute(x, AttributeType.ATTACK) for x in tiles])
        return [x for x in tiles if self.game_object_proxy.get_attribute(x, AttributeType.ATTACK) == max_attack]
