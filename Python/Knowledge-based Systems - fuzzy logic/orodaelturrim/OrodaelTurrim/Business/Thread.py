import time
from threading import Lock

from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject

from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Presenter.Connector import Connector


class WorkerSignals(QObject):
    """ Class wraper for signal communication between threads"""
    redraw_signal = pyqtSignal()


class ThreadWorker(QRunnable):
    """ Thread worker for calling GameEngine methods in other threads """
    _lock = Lock()


    def __init__(self, game_engine: GameEngine, function_name: str, delay: float, *args, **kwargs):
        """
        Definition of the work

        :param game_engine: instance of game engine
        :param function_name: dame of the function in game engine
        :param delay: delay between execute the action
        :param args: arguments to be passed to function
        :param kwargs: keyword arguments to be passed to function
        """
        super().__init__()
        self.game_engine = game_engine
        self.function_name = function_name
        self.delay = delay

        self.args = args
        self.kwargs = kwargs

        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        """ Execute job in other thread """
        # Lock is necessary because we are working with same game engine instance
        self._lock.acquire()

        # Minimum sleep time is here for PyQt loop need time to redraw dialogs
        time.sleep(max(self.delay, 0.1))

        getattr(self.game_engine, self.function_name)(*self.args, **self.kwargs)
        Connector().emit('game_thread_finished')

        self._lock.release()
