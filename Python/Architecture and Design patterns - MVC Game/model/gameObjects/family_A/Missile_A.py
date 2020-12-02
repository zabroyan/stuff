from MVCGameConfig import APP_ROOT
from model.gameObjects.AbsMissile import AbsMissile
from strategy.IMovingStrategy import MovingStrategy


class Missile_A(AbsMissile):
    def __init__(self, initialPosition, angle, ms: MovingStrategy, damage):
        icon = f'{APP_ROOT}/ui/assets/missile.png'
        super().__init__(initialPosition, angle, icon, ms, damage)
