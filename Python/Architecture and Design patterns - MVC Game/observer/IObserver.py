from abc import abstractmethod


class Observer:

    @abstractmethod
    def update(self):
        pass
