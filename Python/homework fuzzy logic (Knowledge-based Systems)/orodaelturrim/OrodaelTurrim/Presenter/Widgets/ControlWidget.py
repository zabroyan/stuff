import typing

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Dialogs.GameOverDialog import GameOverDialog
from OrodaelTurrim.Presenter.Widgets.GameControlWidget import GameControlWidget
from OrodaelTurrim.Presenter.Widgets.LogWidget import LogWidget
from OrodaelTurrim.Presenter.Widgets.MapInfoWidget import MapInfoWidget
from OrodaelTurrim.Presenter.Widgets.RoundControlWidget import RoundControlWidget
from OrodaelTurrim.Presenter.Widgets.SpawnInfoWidget import SpawnInfoWidget
from OrodaelTurrim.Structure.Enums import GameOverStates


class ControlWidget(QWidget):
    """ Main tab widget for all control panels. """


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        Connector().subscribe('game_over', self.game_over_slot)

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'controlWidget.ui')) as f:
            uic.loadUi(f, self)

        # Tab for map information
        map_tab = typing.cast(QWidget, self.findChild(QWidget, 'mapTab'))
        map_tab_layout = QVBoxLayout(map_tab)

        map_info_widget = MapInfoWidget(map_tab, self.__game_engine)
        map_tab_layout.addWidget(map_info_widget)

        # Tab for log information
        log_tab = typing.cast(QWidget, self.findChild(QWidget, 'logTab'))
        log_tab_layout = QVBoxLayout(log_tab)

        log_widget = LogWidget(log_tab, self.__game_engine)
        log_tab_layout.addWidget(log_widget)

        # Tab for round control
        round_tab = typing.cast(QWidget, self.findChild(QWidget, 'roundTab'))
        round_tab_layout = QVBoxLayout(round_tab)

        round_widget = RoundControlWidget(round_tab, self.__game_engine)
        round_tab_layout.addWidget(round_widget)

        # Tab for game control
        game_tab = typing.cast(QWidget, self.findChild(QWidget, 'gameTab'))
        game_tab_layout = QVBoxLayout(game_tab)

        game_tab_widget = GameControlWidget(game_tab, self.__game_engine)
        game_tab_layout.addWidget(game_tab_widget)

        # Tab for spawn info
        game_tab = typing.cast(QWidget, self.findChild(QWidget, 'spawnInfoTab'))
        game_tab_layout = QVBoxLayout(game_tab)

        game_tab_widget = SpawnInfoWidget(game_tab, self.__game_engine)
        game_tab_layout.addWidget(game_tab_widget)


    @pyqtSlot()
    def game_over_slot(self) -> None:
        """ Raise game over on game over signal"""
        result = GameOverDialog.execute_()

        if result == GameOverStates.LET_HIM_DIE.value:
            exit(0)

        if result == GameOverStates.FIND_REASON.value:
            Connector().set_variable('find_reason', True)
