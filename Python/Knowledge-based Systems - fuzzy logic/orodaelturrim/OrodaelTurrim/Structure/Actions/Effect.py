from xml.etree.ElementTree import SubElement

from OrodaelTurrim.Structure.Actions.Abstract import GameAction
from OrodaelTurrim.Structure.GameObjects.Effect import Effect
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class EffectApplyAction(GameAction):
    """ Represents game action of effect being applied on game object """


    def __init__(self, game_engine: "GameEngine", effect: Effect, owner: GameObject):
        super().__init__(game_engine)
        self.__effect = effect
        self.__owner = owner


    def execute(self) -> None:
        self._game_engine.apply_effect(self.__owner, self.__effect)


    def undo(self) -> None:
        self._game_engine.remove_effect(self.__owner, self.__effect.effect_type)


    @property
    def text(self) -> str:
        return '{} effect has been attached to {} {}'.format(self.__effect.effect_type, self.__owner.object_type,
                                                             self.__owner.position.offset)


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, owner=str(id(self.__owner)),
                   effect=self.__effect.__class__.__name__)


class EffectDamageAction(GameAction):
    """ Represents game action of effect damaging its owner game object """


    def __init__(self, game_engine: "GameEngine", effect: Effect, owner: GameObject, damage: float):
        super().__init__(game_engine)

        self.__effect = effect
        self.__owner = owner
        self.__damage = damage


    def execute(self) -> None:
        self._game_engine.damage(self.__owner, self.__damage)


    def undo(self) -> None:
        self._game_engine.heal(self.__owner, self.__damage)


    @property
    def text(self) -> str:
        return '{} {} suffered {} damage from {}'.format(self.__owner.object_type, self.__owner.position.offset,
                                                         str(self.__damage),
                                                         self.__effect.effect_type.name.capitalize())


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, owner=str(id(self.__owner)),
                   effect=self.__effect.__class__.__name__, damage=str(self.__damage))


class EffectExpireAction(GameAction):
    """ Represents game action of effect expiring on game object """


    def __init__(self, game_engine: "GameEngine", effect: Effect, owner: GameObject):
        super().__init__(game_engine)

        self.__effect = effect
        self.__owner = owner


    def execute(self) -> None:
        self._game_engine.remove_effect(self.__owner, self.__effect.effect_type)


    def undo(self) -> None:
        self._game_engine.apply_effect(self.__owner, self.__effect)


    @property
    def text(self) -> str:
        return '{} effect attached to {} {} has expired'.format(self.__effect.effect_type, self.__owner.object_type,
                                                                self.__owner.position.offset)


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, owner=str(id(self.__owner)),
                   effect=self.__effect.__class__.__name__)


class EffectRefreshAction(GameAction):
    """  Represents game action of effect being refreshed """


    def __init__(self, game_engine: "GameEngine", effect: Effect, owner: GameObject):
        super().__init__(game_engine)

        self.__effect = effect
        self.__owner = owner

        self.__previous_remaining_duration = effect.remaining_duration


    def execute(self) -> None:
        self.__effect.refresh()


    def undo(self) -> None:
        self.__effect.remaining_duration = self.__previous_remaining_duration


    @property
    def text(self) -> str:
        return '{} effect attached to {} {} has been refreshed'.format(self.__effect.effect_type,
                                                                       self.__owner.object_type,
                                                                       self.__owner.position.offset)


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, owner=str(id(self.__owner)),
                   effect=self.__effect.__class__.__name__)


class EffectTickAction(GameAction):
    """ Represents game action of effect ticking out on game object """


    def __init__(self, game_engine: "GameEngine", effect: Effect, owner: GameObject):
        super().__init__(game_engine)
        self.__effect = effect
        self.__owner = owner

        self.__remaining_duration = self.__effect.remaining_duration - 1


    def execute(self) -> None:
        self.__effect.tick()


    def undo(self) -> None:
        self.__effect.un_tick()


    @property
    def text(self) -> str:
        return '{} effect attached to {} {} has ticked (remaining duration: {})'.format(self.__effect.effect_type,
                                                                                        self.__owner.object_type,
                                                                                        self.__owner.position.offset,
                                                                                        self.__remaining_duration)


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, owner=str(id(self.__owner)),
                   effect=self.__effect.__class__.__name__, remaining_duration=str(self.__remaining_duration))
