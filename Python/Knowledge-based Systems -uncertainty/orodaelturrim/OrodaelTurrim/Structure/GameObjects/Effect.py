from abc import ABC, abstractmethod

from OrodaelTurrim.Structure.Enums import AttributeType, EffectType
from OrodaelTurrim.Structure.GameObjects.Attributes import AttributeAffection


class Effect(ABC):
    """ Abstract class defining common behavior of effects """
    DEFAULT_DURATION = 3


    def __init__(self, duration: int, affection: AttributeAffection):
        self.__duration = duration
        self.__affection = affection


    def affect_attribute(self, attribute: AttributeType, original_value: float) -> float:
        return self.__affection.affect_attribute(attribute, original_value)


    def compute_damage(self, hit_points: float) -> float:
        """
        Computes, how much damage will this effect inflict on start of each turn

        :param hit_points: Previous value of hit points of game object
        :return: Amount of damage to be inflicted to game object
        """
        return 0


    def refresh(self) -> None:
        """ Refreshes the effect back to default duration """
        self.__duration = self.DEFAULT_DURATION


    def tick(self) -> None:
        """ Sends signal to effect to diminish its timer """
        self.__duration -= 1


    def un_tick(self) -> None:
        """ Sends signal to effect to increase its timer """
        self.__duration += 1


    @property
    @abstractmethod
    def effect_type(self) -> EffectType:
        pass


    @property
    def remaining_duration(self) -> int:
        """ Retrieves remaining duration of this effect """
        return self.__duration


    @remaining_duration.setter
    def remaining_duration(self, value: int) -> None:
        self.__duration = value


    @property
    def hax_expired(self) -> bool:
        """
        Check whether the effect expired or not

        :return: True in case effect expired and should be removed, false otherwise
        """
        return self.__duration <= 0


class Blind(Effect):
    """ Represents a state, when object has greatly reduced sight."""
    SIGHT_REDUCTION = 0.5


    def __init__(self, duration: int = Effect.DEFAULT_DURATION):
        affection = AttributeAffection()
        affection.affect_sight = lambda original_value: original_value * Blind.SIGHT_REDUCTION
        super().__init__(duration, affection)


    @property
    def effect_type(self) -> EffectType:
        return EffectType.BLIND


class Burn(Effect):
    """ Effect representing state of burning object """
    BURN_DAMAGE = 5.0


    def __init__(self, duration: int = Effect.DEFAULT_DURATION):
        super().__init__(duration, AttributeAffection())


    def compute_damage(self, hit_points: float):
        return self.BURN_DAMAGE


    @property
    def effect_type(self):
        return EffectType.BURN


class Freeze(Effect):
    """ Effect representing state of object, when it is frozen. """
    ACTION_REDUCTION = 0.5
    DEFENSE_REDUCTION = 0.75


    def __init__(self, duration: int = Effect.DEFAULT_DURATION):
        affection = AttributeAffection()
        affection.affect_actions = lambda original_value: original_value * Freeze.ACTION_REDUCTION
        affection.affect_defense = lambda original_value: original_value * Freeze.DEFENSE_REDUCTION
        super().__init__(duration, affection)


    @property
    def effect_type(self) -> EffectType:
        return EffectType.FREEZE


class Root(Effect):
    """ Represents a state, when object is rooted and therefore not able to inflict so much damage. """
    ATTACK_REDUCTION = 0.5


    def __init__(self, duration: int = Effect.DEFAULT_DURATION):
        affection = AttributeAffection()
        affection.affect_attack = lambda original_value: original_value * Root.ATTACK_REDUCTION
        super().__init__(duration, affection)


    @property
    def effect_type(self) -> EffectType:
        return EffectType.ROOT
