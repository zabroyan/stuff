import sys
from typing import Callable, Any

from PyQt5.QtCore import pyqtSignal, QObject
from OrodaelTurrim.Structure.Utils import QtSingleton

from OrodaelTurrim.Structure.Position import Position
import threading


class Connector(QObject, metaclass=QtSingleton):
    """
    Class for connection signals and slot across the application and threads

    Signals:
     - **redraw_ui** - Signal to redraw UI
     - **redraw_map** - Signal to redraw map
     - **display_border[dict,list]** - Signal to display border on map
          dict - Dict[Position, Border] - dict of border

          list - List[QColor] - colors for delete
     - **game_over** - Signal that base died
     - **map_position_change[Position]** - Selected position on map changed
     - **map_position_clear** - No position on map is selected
     - **status_message[str]** - Display message on status bar
     - **log_message[str]** - Add message to game log
     - **error_message[str][str]** - Display error dialog -  title, message
     - **game_thread_finished** - Inform that thread computation is done (From other thread!)
    """
    _lock = threading.Lock()  # Lock for thread save variable access

    redraw_ui = pyqtSignal()
    redraw_map = pyqtSignal()
    display_border = pyqtSignal(dict, list)
    game_over = pyqtSignal()
    map_position_change = pyqtSignal(Position)
    map_position_clear = pyqtSignal()
    status_message = pyqtSignal(str)
    log_message = pyqtSignal(str)
    error_message = pyqtSignal(str, str)

    game_thread_finished = pyqtSignal()


    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._variables = {}


    def subscribe(self, name: str, target: Callable) -> None:
        """ Connect target function to global signal. Signal must be defined as static """

        try:
            getattr(self, name).connect(target)
        except AttributeError:
            sys.stderr.write('Signal {} not defined, signal not subscribed!\n'.format(name))


    def emit(self, name: str, *args, **kwargs) -> None:
        """ Emit signal `name` with giver parameters. Signal must be defined as static """

        try:
            getattr(self, name).emit(*args, **kwargs)
        except AttributeError:
            sys.stderr.write('Signal {} not defined, signal not emitted!\n'.format(name))


    def functor(self, name) -> "Caller":
        """ Return pointer to function. Could be emitted later"""

        return Caller(name)


    def set_variable(self, name: str, value: Any) -> None:
        """ Set global variable. Thread safe"""

        with self._lock:
            self._variables[name] = value


    def get_variable(self, name: str) -> Any:
        """ Get global variable. Thread safe"""

        with self._lock:
            return self._variables.get(name, None)


class Caller:
    """ Class wrapper for function pointer """


    def __init__(self, name: str):
        self.__name = name


    def __call__(self, *args, **kwargs):
        Connector().emit(self.__name, *args, **kwargs)
