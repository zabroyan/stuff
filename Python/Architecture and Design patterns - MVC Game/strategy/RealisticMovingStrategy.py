from strategy.IMovingStrategy import MovingStrategy
from Position import Position
from MVCGameConfig import GRAVITY, MISSILE_STEP
import math


class RealisticMovingStrategy(MovingStrategy):
    def updatePosition(self, missile):
        angle = math.radians(-missile.angle)
        time = missile.time
        x = (MISSILE_STEP * math.cos(angle) * time)
        y = (MISSILE_STEP * math.sin(angle) * time) - (GRAVITY * (time ** 2)) / 2
        missile.move(Position(x, -y))
        missile.time += 0.1
