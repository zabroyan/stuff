from abstractfactory.IGameObjectFactory import IGameObjectFactory
from model.gameObjects.family_A.Cannon_A import Cannon_A
from model.gameObjects.family_A.Missile_A import Missile_A
from model.gameObjects.family_A.Enemy_A import Enemy_A
from model.gameObjects.family_A.Collision_A import Collision_A
from strategy.SimpleMovingStrategy import SimpleMovingStrategy
from strategy.RealisticMovingStrategy import RealisticMovingStrategy
from MVCGameConfig import ENEMY_A_HEALTH, ENEMY_A_POINTS


class GameObjectFactory_A(IGameObjectFactory):
    def createCannon(self, position):
        return Cannon_A(position, self)

    def createMissile(self, position, angle, damage):
        return Missile_A(position, angle, SimpleMovingStrategy(), damage)

    def createEnemy(self, position):
        return Enemy_A(position, ENEMY_A_HEALTH, ENEMY_A_POINTS)

    def createCollision(self, position):
        return Collision_A(position)

    def createGameInfo(self, position):
        pass
