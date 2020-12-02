from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPaintEvent, QKeyEvent
from PyQt5.QtWidgets import QWidget
from observer.IObserver import Observer


class Canvas(QWidget, Observer):
    def __init__(self, controller, view):
        super().__init__()
        self._controller = controller
        self._view = view
        self.setFocusPolicy(Qt.ClickFocus)
        self._view.model.registerObserver(self)

    def paintEvent(self, event):
        self._view.render()

    def keyPressEvent(self, event):
        self._controller.keyPressEvent(event)
