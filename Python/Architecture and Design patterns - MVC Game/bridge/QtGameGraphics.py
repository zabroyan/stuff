from PyQt5.QtGui import QPixmap, QPainter, QPixmap, QPen
from PyQt5.QtCore import QPoint
from bridge.AbsGameGraphics import AbsGameGraphics


class QtGameGraphics(AbsGameGraphics):

    def __init__(self, canvas, labels):
        self.canvas = canvas
        self.labels = labels

    def drawImage(self, image, position):
        painter = QPainter(self.canvas)
        painter.drawPixmap(QPoint(position.x, position.y), QPixmap(image))

    def drawText(self, text: str, position):
        pen = QPen()
        painter = QPainter(self.canvas)
        painter.setPen(pen)
        painter.drawText(QPoint(position.x, position.y), text)

    def drawLine(self, startPos, endPos):
        pen = QPen()
        pen.setDashOffset(1)
        pen.setWidth(2)
        painter = QPainter(self.canvas)
        painter.setPen(pen)
        painter.drawLine(QPoint(startPos.x, startPos.y), QPoint(endPos.x, endPos.y))

    def drawGameInfo(self, gi):
        names = gi.getNames()
        self.labels[0].setText(f"{names[0]}: {gi.getShootingMode()}")
        self.labels[1].setText(f"{names[1]}: {gi.getDamage()}")
        self.labels[2].setText(f"{names[2]}: {- gi.getAngle()}")
        self.labels[3].setText(f"{names[3]}: {gi.getGravity()}")
        self.labels[4].setText(f"{names[4]}: {gi.getScore()}")
        self.labels[5].setText(f"{names[5]}: {gi.getLevel()}")