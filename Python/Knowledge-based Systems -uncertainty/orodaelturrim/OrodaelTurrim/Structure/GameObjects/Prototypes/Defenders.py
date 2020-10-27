from typing import Set

from OrodaelTurrim.Structure.Enums import GameRole, GameObjectType, EffectType
from OrodaelTurrim.Structure.GameObjects.Attributes import AttributeBundle
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototype


class Archer(GameObjectPrototype):
    """
    Represents an elf archer with pointy ears and even pointier arrows. There used to be a lot adventurers,
    but then all of them got an arrow to the knee ...
    """
    ATTRIBUTES = AttributeBundle(10, 1, 30, 3, 4)
    COST = 5
    ASSET_NAME = "archer"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.ARCHER, GameRole.DEFENDER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BLIND}


class Base(GameObjectPrototype):
    """
    Represents defenders base as an object which defenders are trying to prevent attackers from destroying
    """
    ATTRIBUTES = AttributeBundle(5, 0, 500, 1, 2)
    COST = 0
    ASSET_NAME = "base"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.BASE, GameRole.DEFENDER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BLIND}


class Druid(GameObjectPrototype):
    """
    Represents the guardian of forest. He is usually calm but try to stomp on his favorite flower and
    his bear friends will stomp on you
    """
    ATTRIBUTES = AttributeBundle(30, 5, 100, 2, 5)
    COST = 25
    ASSET_NAME = "druid"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.DRUID, GameRole.DEFENDER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return {EffectType.FREEZE}


    @property
    def resistances(self) -> Set[EffectType]:
        return set()


class Ent(GameObjectPrototype):
    """ Represents a giant moving tree. Now you regret that little heart you curved into me, don't you?! """
    ATTRIBUTES = AttributeBundle(10, 15, 250, 1, 2)
    COST = 50
    ASSET_NAME = "ent"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.ENT, GameRole.DEFENDER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return {EffectType.ROOT}


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.FREEZE}


class Knight(GameObjectPrototype):
    """ Represents a knight in shining armor. That shine? Mr. Proper! """
    ATTRIBUTES = AttributeBundle(15, 12, 80, 1, 2)
    COST = 12
    ASSET_NAME = "knight"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.KNIGHT, GameRole.DEFENDER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return {EffectType.BLIND}


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.ROOT}


class Magician(GameObjectPrototype):
    """ Represents a powerful battle caster. You´re wizard ... uhm ... MAGICIAN, Harry! """
    ATTRIBUTES = AttributeBundle(40, 5, 75, 2, 3)
    COST = 30
    ASSET_NAME = "magician"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.MAGICIAN, GameRole.DEFENDER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return {EffectType.BURN}


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BURN}
