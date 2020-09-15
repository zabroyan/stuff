from OrodaelTurrim.Structure.Enums import AttributeType


class AttributeBundle:
    """ Represents data class holding attribute values for game objects """


    def __init__(self, attack: float, defense: float, hit_points: float, attack_range: int, sight: int,
                 actions: int = 0):
        self.actions = actions
        self.attack = attack
        self.defense = defense
        self.hit_points = hit_points
        self.attack_range = attack_range
        self.sight = sight


class AttributeAffection:
    """ Class that representing affection of the target attribute """


    def affect_actions(self, original_value: int) -> int:
        return original_value


    def affect_attack(self, original_value: float) -> float:
        return original_value


    def affect_defense(self, original_value: float) -> float:
        return original_value


    def affect_hit_points(self, original_value: float) -> float:
        return original_value


    def affect_attack_range(self, original_value: int) -> int:
        return original_value


    def affect_sight(self, original_value: int) -> int:
        return original_value


    def affect_attribute(self, attribute: AttributeType, original_value: float) -> float:
        if attribute == AttributeType.ACTIONS:
            return float(self.affect_actions(int(original_value)))
        elif attribute == AttributeType.ATTACK:
            return self.affect_attack(original_value)
        elif attribute == AttributeType.DEFENSE:
            return self.affect_defense(original_value)
        elif attribute == AttributeType.HIT_POINTS:
            return self.affect_hit_points(original_value)
        elif attribute == AttributeType.ATTACK_RANGE:
            return float(self.affect_attack_range(int(original_value)))
        elif attribute == AttributeType.SIGHT:
            return float(self.affect_sight(int(original_value)))

        return original_value
