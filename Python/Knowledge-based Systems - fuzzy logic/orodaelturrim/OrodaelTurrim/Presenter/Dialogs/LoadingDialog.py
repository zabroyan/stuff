from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QDialog

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Presenter.Connector import Connector


class LoadingDialog(QDialog):
    """
     Simple window with info text
     Window could be closed only with signal, not from UI
    """


    def __init__(self):
        super().__init__()
        self.init_ui()

        Connector().subscribe('game_over', self.accept)
        Connector().subscribe('game_thread_finished', self.accept)


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'loadingDialog.ui')) as f:
            uic.loadUi(f, self)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)


    @staticmethod
    def execute_():
        dialog = LoadingDialog()
        result = dialog.exec_()

        return result
