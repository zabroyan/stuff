from abc import abstractmethod


class MovingStrategy:
    @abstractmethod
    def updatePosition(self, missile):
        pass
