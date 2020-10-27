from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from PyQt5 import QtCore
from typing import cast
from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.config import Config


class ConfigurationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'configurationDialog.ui')) as f:
            uic.loadUi(f, self)

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        config = dict([(key, value) for key, value in Config.__dict__.items() if key[:1] != '_'])

        table = cast(QTableWidget, self.findChild(QTableWidget, 'configTable'))

        for key, value in config.items():
            row_position = table.rowCount()
            table.insertRow(row_position)

            table.setItem(row_position, 0, QTableWidgetItem(key))
            table.setItem(row_position, 1, QTableWidgetItem(str(value)))

        table.resizeColumnToContents(0)


    @staticmethod
    def execute_():
        dialog = ConfigurationDialog()
        result = dialog.exec_()

        return result
