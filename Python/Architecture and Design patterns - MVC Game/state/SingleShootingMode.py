from state.IShootingMode import ShootingMode
from MVCGameConfig import DAMAGE


class SingleShootingMode(ShootingMode):
    def __init__(self):
        super().__init__(DAMAGE)

    def shoot(self, cannon, damage):
        cannon.primitiveShoot(cannon.getPosition(), damage)

    def name(self):
        return "Single"
