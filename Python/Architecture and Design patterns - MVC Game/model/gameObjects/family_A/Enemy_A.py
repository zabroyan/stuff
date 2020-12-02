from MVCGameConfig import APP_ROOT
from model.gameObjects.AbsEnemy import AbsEnemy


class Enemy_A(AbsEnemy):
    def __init__(self, position, health, points):
        icon = f'{APP_ROOT}/ui/assets/enemy1.png'
        super().__init__(position, icon, health, points)

    def hitBy(self, missile):
        self.health -= missile.damage
