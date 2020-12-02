from strategy.IMovingStrategy import MovingStrategy
from Position import Position
from MVCGameConfig import MISSILE_STEP
import math


class SimpleMovingStrategy(MovingStrategy):
    def updatePosition(self, missile):
        x = math.cos(math.radians(missile.angle)) * MISSILE_STEP
        y = math.sin(math.radians(missile.angle)) * MISSILE_STEP
        missile.move(Position(x, y))
