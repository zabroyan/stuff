from typing import TYPE_CHECKING
from xml.etree.ElementTree import SubElement

from OrodaelTurrim.Structure.Actions.Abstract import GameAction

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class LogAction(GameAction):
    """ User custom log action """


    def __init__(self, game_engine: "GameEngine", log_message: str):
        super().__init__(game_engine)

        self.log_message = log_message


    def execute(self) -> None:
        pass


    def undo(self) -> None:
        pass


    @property
    def text(self) -> str:
        return self.log_message


    def xml(self, parent) -> SubElement:
        SubElement(parent, 'Action', type=self.__class__.__name__, msg=str(self.log_message))
