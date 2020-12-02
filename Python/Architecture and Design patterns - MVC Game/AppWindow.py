from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QApplication

from MVCGameConfig import APP_ROOT, TIME_TICK_PERIOD, MAX_X, MAX_Y
from model.GameModel import GameModel
from view.GameView import GameView
from view.Canvas import Canvas
from bridge.QtGameGraphics import QtGameGraphics
from Position import Rectangle

qt_creator_file = f'{APP_ROOT}\\ui\\mainWindow.ui'
UiMainWindow, _ = uic.loadUiType(qt_creator_file)


class AppWindow(QMainWindow, UiMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        UiMainWindow.__init__(self)
        self.setupUi(self)

        self.model = GameModel()
        view = GameView(self.model)
        controller = view.makeController()
        canvas = Canvas(controller, view)

        layout = self.findChild(QHBoxLayout, "metrics")
        labels = [layout.itemAt(i).widget() for i in range(0, layout.count())]
        view.setGameGraphics(QtGameGraphics(canvas, labels))

        self.model.setGameArea(Rectangle(0, 0, MAX_X, MAX_Y))

        canvas_holder = self.findChild(QScrollArea, 'canvasHolder')
        canvas_holder.setWidget(canvas)
        canvas_holder.setStyleSheet('background-color: white')
