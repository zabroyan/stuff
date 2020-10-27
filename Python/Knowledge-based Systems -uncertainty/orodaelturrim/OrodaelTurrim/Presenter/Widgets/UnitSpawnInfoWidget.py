import typing

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton

from OrodaelTurrim import UI_ROOT, ICONS_ROOT
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Utils import AssetsEncoder
from OrodaelTurrim.Structure.GameObjects.GameObject import UncertaintySpawn
from OrodaelTurrim.Structure.Map import Border


class UnitSpawnInfoWidget(QWidget):
    """ One box for Unit spawn uncertainty info """


    def __init__(self, parent: QWidget = None, uncertainty_spawn: UncertaintySpawn = None):
        super().__init__(parent)

        self.uncertainty_spawn = uncertainty_spawn
        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'unitSpawnInfoWidget.ui')) as f:
            uic.loadUi(f, self)

        img = AssetsEncoder[self.uncertainty_spawn.game_object_type]

        img_label = typing.cast(QLabel, self.findChild(QLabel, 'imageLabel'))
        unit_label = typing.cast(QLabel, self.findChild(QLabel, 'unitLabel'))
        position_label = typing.cast(QLabel, self.findChild(QLabel, 'positionLabel'))

        # Display button for display possible positions on map
        display_button = typing.cast(QPushButton, self.findChild(QPushButton, 'displayButton'))
        display_button.setIcon(QIcon(str(ICONS_ROOT / 'eye.png')))
        display_button.clicked.connect(self.display_spawn_slot)

        # Display image of unit
        img_label.setScaledContents(True)
        img_label.setPixmap(QPixmap(str(img)))

        # Set text about uncertainty
        unit_label.setText(self.uncertainty_spawn.game_object_type.name.capitalize())
        text = 'Position from {} to {} uniform uncertainty {:.2f}%'.format(self.uncertainty_spawn.positions[0].position,
                                                                           self.uncertainty_spawn.positions[
                                                                               -1].position,
                                                                           self.uncertainty_spawn.positions[
                                                                               0].uncertainty * 100)
        position_label.setText(text)


    @pyqtSlot()
    def display_spawn_slot(self) -> None:
        """ Handle display spawn tiles on map"""

        border_dict = {}
        for position in self.uncertainty_spawn.positions:
            border_dict[position.position] = Border.full(3, QColor(255, 21, 221))

        Connector().emit('display_border', border_dict, [QColor(255, 21, 221)])
