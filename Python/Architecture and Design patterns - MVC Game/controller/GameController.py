from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from command.AbsCommand import CannonMoveUp, CannonMoveDown, CannonShoot, CannonAimUp, CannonAimDown, \
    ToggleShootingMode, ChangeLanguage
from model.IGameModel import IGameModel


class GameController:
    def __init__(self, model: IGameModel):
        self.model = model

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Up:
            self.model.registerCommand(CannonMoveUp(self.model))
        elif event.key() == Qt.Key_Down:
            self.model.registerCommand(CannonMoveDown(self.model))
        elif event.key() == Qt.Key_Left:
            self.model.registerCommand(CannonAimUp(self.model))
        elif event.key() == Qt.Key_Right:
            self.model.registerCommand(CannonAimDown(self.model))
        elif event.key() == Qt.Key_Space:
            self.model.registerCommand(CannonShoot(self.model))
        elif event.key() == Qt.Key_M:
            self.model.registerCommand(ToggleShootingMode(self.model))
        elif event.key() == Qt.Key_C:
            self.model.registerCommand(ChangeLanguage(self.model))
        elif event.key() == Qt.Key_Z:
            self.model.undoLastCommand()
