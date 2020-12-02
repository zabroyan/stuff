from abc import abstractmethod
from model.gameObjects.AbsCannon import AbsCannon
from model.gameObjects.AbsEnemy import AbsEnemy
from model.gameObjects.AbsCollision import AbsCollision
from model.gameObjects.AbsGameInfo import AbsGameInfo
from model.gameObjects.AbsMissile import AbsMissile


class IGameObjectFactory:
    @abstractmethod
    def createCannon(self, position) -> AbsCannon:
        pass

    @abstractmethod
    def createMissile(self, position) -> AbsMissile:
        pass

    @abstractmethod
    def createEnemy(self, position, angle, damage) -> AbsEnemy:
        pass

    @abstractmethod
    def createCollision(self, position) -> AbsCollision:
        pass

    @abstractmethod
    def createGameInfo(self) -> AbsGameInfo:
        pass
