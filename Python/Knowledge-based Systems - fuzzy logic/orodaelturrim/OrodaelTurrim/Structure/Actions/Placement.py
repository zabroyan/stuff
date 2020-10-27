from xml.etree.ElementTree import SubElement

from OrodaelTurrim.Structure.Actions.Abstract import GameAction
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class DieAction(GameAction):
    """ Represents game action of game object dying """


    def __init__(self, game_engine: "GameEngine", dead_object: GameObject):
        super().__init__(game_engine)

        self.__dead_object = dead_object


    def execute(self) -> None:
        self._game_engine.remove(self.__dead_object)


    def undo(self) -> None:
        self._game_engine.place(self.__dead_object)


    @property
    def text(self) -> str:
        return '{} {} has perished'.format(self.__dead_object.object_type, self.__dead_object.position.offset)


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, dead_object=str(id(self.__dead_object)))


class SpawnAction(GameAction):
    """ Represents game action of game object being spawned """


    def __init__(self, game_engine: "GameEngine", spawned_object: GameObject):
        super().__init__(game_engine)
        self.__spawned_object = spawned_object


    def execute(self) -> None:
        self._game_engine.place(self.__spawned_object)


    def undo(self) -> None:
        self._game_engine.remove(self.__spawned_object)


    @property
    def text(self) -> str:
        return 'Player {} spawned {} on {}'.format(self.__spawned_object.owner.name,
                                                   self.__spawned_object.object_type.name.capitalize(),
                                                   self.__spawned_object.position.offset)


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, spawned_object=str(id(self.__spawned_object)),
                   position=self.__spawned_object.position.offset.xml_string(),
                   object_type=self.__spawned_object.__class__.__name__)
