from abc import abstractmethod
from typing import List
from Position import Position
from model.gameObjects.GameObject import GameObject
from state.SingleShootingMode import SingleShootingMode
from state.DoubleShootingMode import DoubleShootingMode
from visitor.IGameObjectVisitor import IGameObjectVisitor
from model.gameObjects.AbsMissile import AbsMissile


class AbsCannon(GameObject):

    def __init__(self, position, icon, goFact, step):
        super().__init__(position, icon)
        self.goFact = goFact
        self.step = step
        self.missileBatch = []
        self.singleShootingMode = SingleShootingMode()
        self.shootingMode = self.singleShootingMode
        self.doubleShootingMode = DoubleShootingMode()
        self.angle = 0

    def moveUp(self, canMove):
        self.move(Position(0, -self.step))
        if not canMove(self):
            self.move(Position(0, self.step))

    def moveDown(self, canMove):
        self.move(Position(0, self.step))
        if not canMove(self):
            self.move(Position(0, -self.step))

    def shoot(self, damage) -> List[AbsMissile]:
        self.missileBatch.clear()
        self.shootingMode.shoot(self, damage)
        return self.missileBatch

    def primitiveShoot(self, position, damage):
        self.missileBatch.append(self.goFact.createMissile(position, self.angle, damage))

    def toggleShootingMode(self):
        if self.shootingMode == self.singleShootingMode:
            self.shootingMode = self.doubleShootingMode
        else:
            self.shootingMode = self.singleShootingMode

    def increaseDamage(self, newDamage):
        self.shootingMode.damage = newDamage
        self.singleShootingMode.damage = newDamage
        self.doubleShootingMode.damage = newDamage / 2

    @abstractmethod
    def aimUp(self):
        pass

    @abstractmethod
    def aimDown(self):
        pass

    def acceptVisitor(self, visitor: IGameObjectVisitor):
        visitor.visitCannon(self)

    def getStep(self):
        return self.step
