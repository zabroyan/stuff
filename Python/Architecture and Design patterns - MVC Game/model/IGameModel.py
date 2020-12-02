from abc import abstractmethod
from command.AbsCommand import AbsCommand


class IGameModel:
    def setGameArea(self, area):
        self.gameArea = area

    @abstractmethod
    def moveCannonUp(self):
        pass

    @abstractmethod
    def moveCannonDown(self):
        pass

    @abstractmethod
    def aimCannonUp(self):
        pass

    @abstractmethod
    def aimCannonDown(self):
        pass

    @abstractmethod
    def cannonShoot(self):
        pass

    @abstractmethod
    def toggleShootingMode(self):
        pass

    @abstractmethod
    def changeLanguage(self):
        pass

    @abstractmethod
    def createMemento(self):
        pass

    @abstractmethod
    def restoreMemento(self, memento):
        pass

    @abstractmethod
    def registerCommand(self, command: AbsCommand):
        pass

    @abstractmethod
    def undoLastCommand(self):
        pass
