from abc import abstractmethod


class IGameObjectVisitor:

    @abstractmethod
    def visitCannon(self, cannon):
        pass

    @abstractmethod
    def visitMissile(self, missile):
        pass

    @abstractmethod
    def visitEnemy(self, enemy):
        pass

    @abstractmethod
    def visitCollision(self, collision):
        pass

    @abstractmethod
    def visitGameInfo(self, gi):
        pass
