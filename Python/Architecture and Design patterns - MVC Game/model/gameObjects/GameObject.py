from abc import abstractmethod
# from PyQt5.QtGui import QPixmap
from Position import Rectangle
from visitor.IGameObjectVisitor import IGameObjectVisitor


class GameObject:
    def __init__(self, pos, icon):
        self.position = pos
        self.icon = icon
        # pixmap = QPixmap(icon) #tests crash with PyQt
        # self.width = pixmap.width()
        # self.height = pixmap.height()
        self.width = 30
        self.height = 30

    def move(self, pos):
        self.position += pos

    def getPosition(self):
        return self.position

    def getIcon(self):
        return self.icon

    def getRect(self):
        return Rectangle(self.position.x, self.position.y, self.width, self.height)

    @abstractmethod
    def acceptVisitor(self, visitor: IGameObjectVisitor):
        pass
