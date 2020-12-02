from abc import abstractmethod
import math
from bridge.AbsGameGraphics import AbsGameGraphics
from model.gameObjects.AbsCannon import AbsCannon
from model.gameObjects.AbsEnemy import AbsEnemy
from model.gameObjects.AbsCollision import AbsCollision
from model.gameObjects.AbsGameInfo import AbsGameInfo
from model.gameObjects.AbsMissile import AbsMissile
from visitor.IGameObjectVisitor import IGameObjectVisitor
from Position import Position


class GameObjectRender(IGameObjectVisitor):
    def setGameGraphics(self, graphics: AbsGameGraphics):
        self.graphics = graphics

    def visitCannon(self, cannon: AbsCannon):
        self.graphics.drawImage(cannon.getIcon(), cannon.getPosition())
        x = math.cos(math.radians(cannon.angle)) * 50
        y = math.sin(math.radians(cannon.angle)) * 50
        self.graphics.drawLine(cannon.getPosition(), cannon.getPosition() + Position(x, y))

    def visitEnemy(self, enemy: AbsEnemy):
        self.graphics.drawImage(enemy.getIcon(), enemy.getPosition())

    def visitMissile(self, missile: AbsMissile):
        self.graphics.drawImage(missile.getIcon(), missile.getPosition())

    def visitCollision(self, collision: AbsCollision):
        self.graphics.drawImage(collision.getIcon(), collision.getPosition())

    def visitGameInfo(self, gi: AbsGameInfo):
        self.graphics.drawGameInfo(gi)
