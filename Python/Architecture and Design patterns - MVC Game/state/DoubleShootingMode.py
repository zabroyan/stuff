from state.IShootingMode import ShootingMode
from Position import Position
from MVCGameConfig import DAMAGE


class DoubleShootingMode(ShootingMode):
    def __init__(self):
        super().__init__(DAMAGE / 2)

    def shoot(self, cannon, damage):
        cannon.primitiveShoot(cannon.getPosition(), damage / 2)
        cannon.primitiveShoot(cannon.getPosition() + Position(50, 0), damage / 2)

    def name(self):
        return "Double"
