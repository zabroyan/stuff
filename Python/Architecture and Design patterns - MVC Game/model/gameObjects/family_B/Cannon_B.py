from MVCGameConfig import APP_ROOT, MOVE_STEP
from abstractfactory.IGameObjectFactory import IGameObjectFactory
from model.gameObjects.AbsCannon import AbsCannon
from state.DoubleShootingMode import DoubleShootingMode


class Cannon_B(AbsCannon):
    def __init__(self, initialPosition, goFact: IGameObjectFactory):
        icon = f'{APP_ROOT}/ui/assets/cannon2.png'
        self.shootingMode = DoubleShootingMode()
        super().__init__(initialPosition, icon, goFact, 2 * MOVE_STEP)

    def aimUp(self):
        if self.angle + 10 > -80:
            self.angle -= 10

    def aimDown(self):
        if self.angle + 10 < 80:
            self.angle += 10