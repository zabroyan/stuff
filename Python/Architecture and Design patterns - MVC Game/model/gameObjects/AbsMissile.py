from abc import abstractmethod
from model.gameObjects.GameObject import GameObject
from strategy.IMovingStrategy import MovingStrategy
from visitor.IGameObjectVisitor import IGameObjectVisitor


class AbsMissile(GameObject):
    def __init__(self, position, angle, icon, ms: MovingStrategy, damage):
        self.movingStrategy = ms
        self.angle = angle
        self.damage = damage
        self.time = 0
        super().__init__(position, icon)

    def moveMissile(self):
        self.movingStrategy.updatePosition(self)

    def acceptVisitor(self, visitor: IGameObjectVisitor):
        visitor.visitMissile(self)
