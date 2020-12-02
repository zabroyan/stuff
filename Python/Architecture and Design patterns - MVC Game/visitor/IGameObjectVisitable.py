from abc import abstractmethod
from visitor.IGameObjectVisitor import IGameObjectVisitor


class GameObjectVisitable:
    @abstractmethod
    def acceptVisitor(self, visitor: IGameObjectVisitor):
        pass
