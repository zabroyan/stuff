from typing import Set

from OrodaelTurrim.Structure.Enums import EffectType, GameObjectType, GameRole
from OrodaelTurrim.Structure.GameObjects.Attributes import AttributeBundle
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototype


class Cyclops(GameObjectPrototype):
    """ Represents an one-eyed warrior. This is what happens when you breed blind and seeing person -_- """
    ATTRIBUTES = AttributeBundle(20, 10, 80, 2, 2, 3)
    COST = 60
    ASSET_NAME = "cyclops"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BURN}


class Demon(GameObjectPrototype):
    """ Represents warrior of demon army. Overpowered range caster, what else to say? """
    ATTRIBUTES = AttributeBundle(35, 5, 150, 2, 3, 3)
    COST = 80
    ASSET_NAME = "demon"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return {EffectType.BURN}


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BURN, EffectType.FREEZE}


class Elemental(GameObjectPrototype):
    """ Represents a burning mass of energy. Good for lighting candles, bad for child keeping. """
    ATTRIBUTES = AttributeBundle(12, 10, 60, 3, 2, 3)
    COST = 35
    ASSET_NAME = "elemental"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return {EffectType.BURN}


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BURN}


class Gargoyle(GameObjectPrototype):
    """ Represents flying living status. Like frightening and stuff but have you looked at it?  """
    ATTRIBUTES = AttributeBundle(10, 10, 60, 2, 5, 3)
    COST = 30
    ASSET_NAME = "gargoyle"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.FREEZE}


class Minotaur(GameObjectPrototype):
    """Represents a half-human, half-bull. Somebody forgot to lock the Labyrinth and now they are all over the place!"""

    ATTRIBUTES = AttributeBundle(15, 20, 150, 2, 1, 2)
    COST = 50
    ASSET_NAME = "minotaur"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.ROOT}


class Necromancer(GameObjectPrototype):
    """
    Represents a dark magician with ability to raise dead. My mom always said: "If you don't have any friends,
    you should go out and raise some ...
    """
    ATTRIBUTES = AttributeBundle(30, 5, 75, 3, 2, 3)
    COST = 0
    ASSET_NAME = "necromancer"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.ROOT}


class Orc(GameObjectPrototype):
    """ Represents two hundred pounds of green hatred. Lok'tar Ogar, chief! """
    ATTRIBUTES = AttributeBundle(10, 5, 35, 2, 1, 3)
    COST = 8
    ASSET_NAME = "orc"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.ROOT}


class Skeleton(GameObjectPrototype):
    """ Represents a moving pile of bones. What do you mean by "Hit it straight to heart?" It ain't got one! """
    ATTRIBUTES = AttributeBundle(7, 2, 20, 2, 1, 2)
    COST = 5
    ASSET_NAME = "skeleton"


    def __init__(self):
        super().__init__(self.ATTRIBUTES, self.COST, GameObjectType.CYCLOPS, GameRole.ATTACKER, self.ASSET_NAME)


    @property
    def attack_effects(self) -> Set[EffectType]:
        return set()


    @property
    def resistances(self) -> Set[EffectType]:
        return {EffectType.BLIND}
