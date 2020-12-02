from model.gameObjects.GameObject import GameObject
from datetime import datetime


class LifetimeLimitedGameObject(GameObject):
    def __init__(self, position, icon):
        self.position = position
        self.bornAt = datetime.now()
        super().__init__(position, icon)

    def getAge(self):
        return (datetime.now() - self.bornAt).total_seconds()