from typing import TYPE_CHECKING

from PyQt5.QtCore import pyqtSlot, QObject

from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Structure.Exceptions import IllegalLogMessage

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


class Logger:
    """ Class for emitting custom user logs to the game log """


    @staticmethod
    def log(text: str) -> None:
        """ Log message to the game history. Log message must be string """
        if type(text) != str:
            raise IllegalLogMessage('Log messages must be string type')

        Connector().emit('log_message', text)


class LogReceiver(QObject):
    """ Class that handle log signal and create new message in the game engine. """


    def __init__(self, game_engine: "GameEngine"):
        super().__init__()
        self.game_engine = game_engine

        Connector().subscribe('log_message', self.create_log_record_slot)


    @pyqtSlot(str)
    def create_log_record_slot(self, message: str) -> None:
        """ Insert log message to game history """
        self.game_engine.create_log_action(message)
