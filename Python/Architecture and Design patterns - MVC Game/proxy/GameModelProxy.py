from model.IGameModel import IGameModel
from command.AbsCommand import AbsCommand


class GameModelProxy(IGameModel):
    def __init__(self, subject: IGameModel):
        self.subject = subject

    def moveCannonUp(self):
        self.subject.moveCannonUp()

    def moveCannonDown(self):
        self.subject.moveCannonDown()

    def aimCannonUp(self):
        self.subject.aimCannonUp()

    def aimCannonDown(self):
        self.subject.aimCannonDown()

    def cannonShoot(self):
        self.subject.cannonShoot()

    def toggleShootingMode(self):
        self.subject.toggleShootingMode()

    def changeLanguage(self):
        self.subject.changeLanguage()

    def createMemento(self):
        return self.subject.createMemento()

    def restoreMemento(self, memento):
        self.subject.restoreMemento(memento)

    def registerCommand(self, command: AbsCommand):
        self.subject.registerCommand(command)

    def undoLastCommand(self):
        self.subject.undoLastCommand()

    def isInsideGameArea(self, obj):
        return self.gameArea.contains(obj.getRect())
