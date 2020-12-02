import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from AppWindow import AppWindow
from MVCGameConfig import APP_ROOT, TIME_TICK_PERIOD

qt_creator_file = f'{APP_ROOT}\\ui\\mainWindow.ui'
UiMainWindow, _ = uic.loadUiType(qt_creator_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    timer = QTimer()
    timer.timeout.connect(window.model.timeTick)
    timer.start(TIME_TICK_PERIOD)

    # Wrapping the GUI execution into `sys.exit()` to ensure that proper result code
    # will be returned when the window closes (otherwise it's always 0)
    sys.exit(app.exec_())
