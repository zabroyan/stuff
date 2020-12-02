from model.gameObjects.LifetimeLimitedGameObject import LifetimeLimitedGameObject
from visitor.IGameObjectVisitor import IGameObjectVisitor


class AbsCollision(LifetimeLimitedGameObject):
    def acceptVisitor(self, visitor: IGameObjectVisitor):
        visitor.visitCollision(self)
