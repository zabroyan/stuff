from visitor.IGameObjectVisitor import IGameObjectVisitor
from visitor.IGameObjectVisitable import GameObjectVisitable
from abc import abstractmethod


class AbsGameInfo(GameObjectVisitable):
    def __init__(self, damage, angle, gravity, score, sm):
        self.damage = damage
        self.angle = angle
        self.gravity = gravity
        self.score = score
        self.shootingMode = sm
        self.level = 1

    def acceptVisitor(self, visitor: IGameObjectVisitor):
        visitor.visitGameInfo(self)

    def getAll(self):
        return [self.damage, self.angle, self.gravity, self.score,
                self.shootingMode, self.level]

    def setAll(self, attributes):
        self.damage, self.angle, self.gravity, self.score, \
        self.shootingMode, self.level = attributes

    def getDamage(self):
        return self.damage

    def setDamage(self, damage):
        self.damage = damage

    def getAngle(self):
        return self.angle

    def setAngle(self, angle):
        self.angle = angle

    def getGravity(self):
        return self.gravity

    def setGravity(self, gravity):
        self.gravity = gravity

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def getShootingMode(self):
        return self.shootingMode

    def setShootingMode(self, sm):
        self.shootingMode = sm

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def addScore(self, score):
        self.score += score

    @abstractmethod
    def getNames(self):
        pass
