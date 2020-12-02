from MVCGameConfig import APP_ROOT, MOVE_STEP
from abstractfactory.IGameObjectFactory import IGameObjectFactory
from model.gameObjects.AbsCannon import AbsCannon
from state.SingleShootingMode import SingleShootingMode


class Cannon_A(AbsCannon):
    def __init__(self, initialPosition, goFact: IGameObjectFactory):
        icon = f'{APP_ROOT}/ui/assets/cannon.png'
        self.shootingMode = SingleShootingMode()
        super().__init__(initialPosition, icon, goFact, MOVE_STEP)

    def aimUp(self):
        if self.angle + 10 > -80:
            self.angle -= 10

    def aimDown(self):
        if self.angle + 10 < 80:
            self.angle += 10
