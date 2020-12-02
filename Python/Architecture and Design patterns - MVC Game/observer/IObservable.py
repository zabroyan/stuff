from abc import abstractmethod

from observer.IObserver import Observer


class Observable:

    @abstractmethod
    def registerObserver(self, obs: Observer):
        pass

    @abstractmethod
    def unregisterObserver(self, obs: Observer):
        pass

    @abstractmethod
    def notifyObservers(self):
        pass
