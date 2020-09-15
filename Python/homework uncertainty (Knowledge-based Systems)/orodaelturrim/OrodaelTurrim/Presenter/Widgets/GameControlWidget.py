import typing

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Widgets.UnitWidget import UnitWidget
from OrodaelTurrim.Structure.Enums import GameObjectType


class GameControlWidget(QWidget):
    """ Widget for manual unit spawn """

    scroll_area_layout: QVBoxLayout
    scroll_area: QWidget


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        Connector().subscribe('redraw_ui', self.redraw_available_money_slot)
        Connector().subscribe('game_thread_finished', self.redraw_available_money_slot)

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'gameControlWidget.ui')) as f:
            uic.loadUi(f, self)

        self.scroll_area = typing.cast(QWidget, self.findChild(QWidget, 'unitsArea'))
        self.scroll_area_layout = QVBoxLayout(self)

        self.scroll_area.setLayout(self.scroll_area_layout)

        # Insert widget for each Defender unit
        for game_object in GameObjectType.defenders():
            self.scroll_area_layout.addWidget(UnitWidget(self.scroll_area, self.__game_engine, game_object))

        self.redraw_available_money_slot()


    @pyqtSlot()
    def redraw_available_money_slot(self) -> None:
        """ Redraw label for available money"""

        resources = self.__game_engine.get_resources(self.__game_engine.get_game_history().active_player)
        income = self.__game_engine.get_income(self.__game_engine.get_game_history().active_player)
        self.findChild(QLabel, 'moneyLabel').setText('Available money: {} ( {} income )'.format(resources, income))
