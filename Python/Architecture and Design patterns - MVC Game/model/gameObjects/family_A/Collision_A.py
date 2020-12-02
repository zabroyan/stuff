from model.gameObjects.AbsCollision import AbsCollision
from MVCGameConfig import APP_ROOT


class Collision_A(AbsCollision):
    def __init__(self, position):
        icon = f'{APP_ROOT}/ui/assets/collision.png'
        super().__init__(position, icon)
