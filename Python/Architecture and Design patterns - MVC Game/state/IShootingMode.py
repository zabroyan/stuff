from abc import abstractmethod


class ShootingMode:
    def __init__(self, damage):
        self.damage = damage

    @abstractmethod
    def shoot(self, cannon, damage):
        pass

    @abstractmethod
    def name(self):
        pass

