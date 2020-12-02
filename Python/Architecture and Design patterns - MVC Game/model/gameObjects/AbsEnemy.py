from model.gameObjects.GameObject import GameObject
from visitor.IGameObjectVisitor import IGameObjectVisitor
from abc import abstractmethod


class AbsEnemy(GameObject):
    def __init__(self, position, icon, health, points):
        super().__init__(position, icon)
        self.health = health
        self.points = points

    def acceptVisitor(self, visitor: IGameObjectVisitor):
        visitor.visitEnemy(self)

    def isDead(self):
        return self.health <= 0

    @abstractmethod
    def hitBy(self, missile):
        pass
