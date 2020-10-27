import typing

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLayout

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Widgets.UnitSpawnInfoWidget import UnitSpawnInfoWidget


class SpawnInfoWidget(QWidget):
    """ Widget for display spawn info of Artificial Intelligence based on Uncertainty module"""

    round_1_layout: QVBoxLayout
    round_2_layout: QVBoxLayout
    round_3_layout: QVBoxLayout

    round_1_box: QWidget
    round_2_box: QWidget
    round_3_box: QWidget


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        Connector().subscribe('redraw_ui', self.redraw_ui)
        Connector().subscribe('game_thread_finished', self.redraw_ui)

        self.init_ui()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'spawnInfoWidget.ui')) as f:
            uic.loadUi(f, self)

        self.round_1_box = typing.cast(QWidget, self.findChild(QWidget, 'round1BoxWidget'))
        self.round_2_box = typing.cast(QWidget, self.findChild(QWidget, 'round2BoxWidget'))
        self.round_3_box = typing.cast(QWidget, self.findChild(QWidget, 'round3BoxWidget'))

        self.round_1_layout = QVBoxLayout(self.round_1_box)
        self.round_1_box.setLayout(self.round_1_layout)

        self.round_2_layout = QVBoxLayout(self.round_2_box)
        self.round_2_box.setLayout(self.round_2_layout)

        self.round_3_layout = QVBoxLayout(self.round_3_box)
        self.round_3_box.setLayout(self.round_3_layout)


    def redraw_ui(self) -> None:
        """ Redraw whole UI based on current information from Uncertainty module"""
        current_turn = self.__game_engine.get_game_history().current_turn
        self.findChild(QLabel, 'round1Label').setText('Round {}'.format(current_turn + 1))
        self.findChild(QLabel, 'round2Label').setText('Round {}'.format(current_turn + 2))
        self.findChild(QLabel, 'round3Label').setText('Round {}'.format(current_turn + 3))

        spawn_info = self.__game_engine.spawn_information()

        # Create widget for each round prediction
        for i, _round in enumerate(spawn_info):
            layout = getattr(self, 'round_{}_layout'.format(i + 1))  # type: QVBoxLayout
            box = getattr(self, 'round_{}_box'.format(i + 1))  # type: QWidget
            self.clear_layout(layout)

            # Create unit spawn widget for each unit spawn info
            for spawn in _round:
                layout.addWidget(UnitSpawnInfoWidget(box, spawn))


    @staticmethod
    def clear_layout(layout: QLayout) -> None:
        """ Clear all UnitSpawnInfoWidget in given layout"""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
