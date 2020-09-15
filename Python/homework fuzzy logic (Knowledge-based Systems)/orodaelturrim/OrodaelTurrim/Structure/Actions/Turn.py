from xml.etree.ElementTree import SubElement

from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Actions.Abstract import GameAction


class EndTurnAction(GameAction):
    """ Represents game action of player ending their turn """


    def __init__(self, game_engine: GameEngine, player: IPlayer):
        super().__init__(game_engine)

        self.__player = player


    def execute(self) -> None:
        pass


    def undo(self) -> None:
        pass


    @property
    def text(self) -> str:
        return 'Player {} finished their turn'.format(self.__player.name)


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, player=str(id(self.__player)))


class StartTurnAction(GameAction):
    """ Represents game action of player starting their turn """


    def __init__(self, game_engine: GameEngine, player: IPlayer):
        super().__init__(game_engine)

        self.__player = player


    def execute(self) -> None:
        pass


    def undo(self) -> None:
        pass


    @property
    def text(self) -> str:
        return 'Player {} started their turn'.format(self.__player.name)


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, player=str(id(self.__player)))
