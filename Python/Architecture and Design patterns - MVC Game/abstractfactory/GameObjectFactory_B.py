from abstractfactory.IGameObjectFactory import IGameObjectFactory
from model.gameObjects.family_B.Cannon_B import Cannon_B
from model.gameObjects.family_B.Missile_B import Missile_B
from model.gameObjects.family_B.Enemy_B import Enemy_B
from model.gameObjects.family_B.Collision_B import Collision_B
from strategy.SimpleMovingStrategy import SimpleMovingStrategy
from strategy.RealisticMovingStrategy import RealisticMovingStrategy
from MVCGameConfig import ENEMY_B_HEALTH, ENEMY_B_POINTS


class GameObjectFactory_B(IGameObjectFactory):
    def createCannon(self, position):
        return Cannon_B(position, self)

    def createMissile(self, position, angle, damage):
        return Missile_B(position, angle, RealisticMovingStrategy(), damage)

    def createEnemy(self, position):
        return Enemy_B(position, ENEMY_B_HEALTH, ENEMY_B_POINTS)

    def createCollision(self, position):
        return Collision_B(position)

    def createGameInfo(self, position):
        pass
