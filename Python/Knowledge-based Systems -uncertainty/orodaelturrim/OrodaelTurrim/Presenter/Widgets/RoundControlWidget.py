import typing

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QSpinBox, QCheckBox, QDoubleSpinBox

from OrodaelTurrim import UI_ROOT
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.Thread import ThreadWorker
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Presenter.Dialogs.LoadingDialog import LoadingDialog


class RoundControlWidget(QWidget):
    """ Widget for control rounds, inference and game history"""


    def __init__(self, parent: QWidget = None, game_engine: GameEngine = None):
        super().__init__(parent)

        self.__game_engine = game_engine

        Connector().subscribe('redraw_ui', self.redraw_ui)
        Connector().subscribe('game_thread_finished', self.redraw_ui)

        self.init_ui()
        self.thread_pool = QThreadPool()


    def init_ui(self) -> None:
        with open(str(UI_ROOT / 'roundControlWidget.ui')) as f:
            uic.loadUi(f, self)

        self.findChild(QPushButton, 'endOfRoundButton').clicked.connect(self.end_of_round_slot)
        self.findChild(QPushButton, 'runInferenceButton').clicked.connect(self.run_inference_slot)

        self.findChild(QPushButton, 'playButton').clicked.connect(self.simulate_game_slot)

        self.findChild(QPushButton, 'previousTurnButton').clicked.connect(self.previous_turn_slot)
        self.findChild(QPushButton, 'nextTurnButton').clicked.connect(self.next_turn_slot)
        self.findChild(QPushButton, 'lastTurnButton').clicked.connect(self.last_turn_slot)

        self.findChild(QPushButton, 'nextTurnButton').setDisabled(True)
        self.findChild(QPushButton, 'lastTurnButton').setDisabled(True)

        self.redraw_ui()


    @pyqtSlot()
    def end_of_round_slot(self) -> None:
        """ Slot for button `End of round` """

        game_history = self.__game_engine.get_game_history()
        current_player = self.__game_engine.get_player(game_history.current_player)

        self.__game_engine.simulate_rest_of_player_turn(current_player)

        while not game_history.on_first_player and not Connector().get_variable('game_over'):
            game_history.active_player.act()
            self.__game_engine.simulate_rest_of_player_turn(game_history.active_player)

        Connector().emit('redraw_map')
        Connector().emit('redraw_ui')


    @pyqtSlot()
    def run_inference_slot(self) -> None:
        """ Run current player turn (act method)"""

        if self.__game_engine.get_game_history().on_first_player:
            self.__game_engine.get_game_history().active_player.act()

        Connector().emit('redraw_ui')
        Connector().emit('redraw_map')


    @pyqtSlot()
    def redraw_ui(self) -> None:
        """ Redraw whole tab UI """

        game_history = self.__game_engine.get_game_history()
        if game_history:

            # Current round and player labels
            self.findChild(QLabel, 'currentRoundLabel').setText(str(game_history.current_turn))
            self.findChild(QLabel, 'currentPlayerLabel').setText(game_history.active_player.name)

            inference_button = typing.cast(QPushButton, self.findChild(QPushButton, 'runInferenceButton'))
            end_of_round_button = typing.cast(QPushButton, self.findChild(QPushButton, 'endOfRoundButton'))
            play_button = typing.cast(QPushButton, self.findChild(QPushButton, 'playButton'))

            # If not in present disable round control buttons
            if not game_history.in_preset:
                end_of_round_button.setDisabled(True)
                play_button.setDisabled(True)
            else:
                end_of_round_button.setDisabled(False)
                play_button.setDisabled(False)

            # If not in present disable inference button
            if game_history.on_first_player and game_history.in_preset:
                inference_button.setDisabled(False)
            else:
                inference_button.setDisabled(True)

            # If game is over, disable play buttons
            if Connector().get_variable('game_over'):
                play_button.setDisabled(True)
                end_of_round_button.setDisabled(True)
                inference_button.setDisabled(True)


    @pyqtSlot()
    def simulate_game_slot(self) -> None:
        """ Simulate N rounds of the game"""

        rounds_box = typing.cast(QSpinBox, self.findChild(QSpinBox, 'roundsBox'))
        rounds = rounds_box.value()

        check_box = typing.cast(QCheckBox, self.findChild(QCheckBox, 'displayProcessCheck'))
        display = check_box.isChecked()

        delay_box = typing.cast(QDoubleSpinBox, self.findChild(QDoubleSpinBox, 'delayBox'))
        delay = delay_box.value()

        # If display is selected, I need to display result after each round
        # Create thread work for each round with argument 1 to simulate one round
        # Threads have locks, so thread will be processed sequentially
        # Between each thread there is space, where GIL is unlocked, so PyQT loop could redraw UI
        if display:
            for i in range(rounds):
                worker = ThreadWorker(self.__game_engine, 'run_game_rounds', delay, 1)
                self.thread_pool.start(worker)
        # If display is not selected, spawn one worker with N rounds and display window with info text
        else:
            worker = ThreadWorker(self.__game_engine, 'run_game_rounds', 0, rounds)
            self.thread_pool.start(worker)

            LoadingDialog.execute_()


    @pyqtSlot()
    def previous_turn_slot(self) -> None:
        """ Move history to previous turn"""
        self.__game_engine.get_game_history().move_turn_back()

        # Enable `Next turn` and `Last turn` buttons
        self.findChild(QPushButton, 'nextTurnButton').setDisabled(False)
        self.findChild(QPushButton, 'lastTurnButton').setDisabled(False)

        if self.__game_engine.get_game_history().at_start:
            self.findChild(QPushButton, 'previousTurnButton').setDisabled(True)

        Connector().emit('redraw_ui')
        Connector().emit('redraw_map')


    @pyqtSlot()
    def next_turn_slot(self) -> None:
        """ Move history one turn forward"""
        self.__game_engine.get_game_history().move_turn_forth()

        # If game is in present, disable `Next turns and `Last turn` buttons
        if self.__game_engine.get_game_history().in_preset:
            self.findChild(QPushButton, 'nextTurnButton').setDisabled(True)
            self.findChild(QPushButton, 'lastTurnButton').setDisabled(True)

        # Enable `Previous turn` button
        self.findChild(QPushButton, 'previousTurnButton').setDisabled(False)

        Connector().emit('redraw_ui')
        Connector().emit('redraw_map')


    @pyqtSlot()
    def last_turn_slot(self) -> None:
        """ Move history to present """
        self.__game_engine.get_game_history().move_to_present()

        # If game is in present, disable `Next turns and `Last turn` buttons
        if self.__game_engine.get_game_history().in_preset:
            self.findChild(QPushButton, 'nextTurnButton').setDisabled(True)
            self.findChild(QPushButton, 'lastTurnButton').setDisabled(True)

        # Enable `Previous turn` button
        self.findChild(QPushButton, 'previousTurnButton').setDisabled(False)

        Connector().emit('redraw_ui')
        Connector().emit('redraw_map')
