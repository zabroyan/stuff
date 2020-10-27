from typing import List, TYPE_CHECKING, Optional

from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Exceptions import IllegalHistoryOperation
import xml.etree.cElementTree as et

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Actions.Abstract import GameAction


class GameHistory:
    """
    | Class providing methods for access to and navigation in game history.
    |
    | Three dimensional array holding all the game history. The first level array represents turns, second
      level array holds players and the third one holds actions of those players.
    """


    def __init__(self, turn_limit: int, players: List[IPlayer]):
        self.__turn_limit = turn_limit
        self.__players = players

        self.__current_turn = -1
        self.__current_player = 0
        self.__current_action = -1

        self.__turns = []  # type: List[List[List["GameAction"]]]

        self.start_next_game_turn()


    def start_next_game_turn(self) -> None:
        """ Registers next game turn and moves indexes to it """
        self.__current_turn += 1
        self.__current_player = -1

        self.__turns.append([])
        self.start_next_player_turn()


    def start_next_player_turn(self) -> None:
        """ Registers turn of next player and moves indexes to it """
        self.__current_player += 1
        self.__current_action = -1

        self.__turns[self.__current_turn].append([])


    def delete_player_turn(self) -> None:
        """
        Removes current registered player turn

        Note that this will discard any remaining actions there, and should be therefore
        called only after all actions have been undone
        """
        self.__turns[self.__current_turn].pop(self.__current_player)


    def delete_game_turn(self) -> None:
        """ Removes current registered game turn """
        self.__turns.pop(self.__current_turn)


    def redo_player_actions(self) -> None:
        """
        Calls execute operation on all remaining actions in current player turn and sets the action index
        on the last player action
        """
        if self.before_first_action:
            self.move_to_next()

        player_actions = self.__turns[self.__current_turn][self.__current_player]

        while self.__current_action <= self.last_action_index:
            player_actions[self.__current_action].execute()

            self.__current_action += 1

        self.__current_action = self.last_action_index


    def undo_player_actions(self) -> None:
        """
        Calls undo operation on all remaining actions in current player turn and sets the action index
        before the first player action
        """
        player_actions = self.__turns[self.__current_turn][self.__current_player]
        while self.__current_action >= 0:
            player_actions[self.__current_action].undo()
            self.__current_action -= 1


    def clear_player_turn(self) -> None:
        """
        Removes all actions from player turn

        Note that this will **NOT undo the actions**, and should be therefore called only once all the actions
        have been undone
        :return:
        """
        self.__turns[self.__current_turn][self.__current_player].clear()


    def move_to_next(self) -> None:
        """ Moves the pointing indexes to next action """
        if self.in_preset:
            return

        if not self.on_last_action:
            self.__current_action += 1
            return
        else:
            self.__current_action = -1

        if not self.on_last_player:
            self.__current_player += 1
            return
        else:
            self.__current_player = 0

        self.__current_turn += 1


    def move_to_previous(self) -> None:
        """ Moves the pointing indexes to previous action """
        if self.at_start:
            return

        if not self.before_first_action:
            self.__current_action -= 1
            return

        if not self.on_first_player:
            self.__current_player -= 1
        else:
            self.__current_player = len(self.__players) - 1
            self.__current_turn -= 1

        self.__current_action = self.last_action_index


    @property
    def current_action(self) -> "GameAction":
        """
        Retrieves action which is being currently pointed at

        :return: Currently pointed action
        :raise: IllegalHistoryOperation in case action pointer is before first action
        """

        if self.before_first_action:
            raise IllegalHistoryOperation('Cannot access action - action pointer is before first action!')

        return self.__turns[self.__current_turn][self.__current_player][self.__current_action]


    @property
    def last_action_index(self) -> int:
        """
        Computes the index of last action for current turn and player
        :return: Index of last action
        """
        return len(self.__turns[self.__current_turn][self.__current_player]) - 1


    @property
    def on_present_turn(self) -> bool:
        """
        Checks, whether turn pointer is on the last played turn

        :return: True in case turn pointer is on the last played turn, false otherwise
        """
        return self.__current_turn == (len(self.__turns) - 1)


    @property
    def on_first_player(self) -> bool:
        """
        Checks, whether player pointer is on the first player

        :return: True in case player pointer is on the first player, false otherwise
        """
        return self.__current_player == 0


    @property
    def on_present_player(self) -> bool:
        """
        Checks, whether player pointer is on the last player who played this turn

        :return: True in case player pointer points to the one who played last, false otherwise
        """
        return self.__current_player == (len(self.__turns[self.__current_turn]) - 1)


    @property
    def on_last_player(self) -> bool:
        """
        Checks, whether player pointer is on the last player

        :return: True in case player pointer is on the last player, false otherwise
        """
        return self.__current_player == (len(self.__players) - 1)


    @property
    def before_first_action(self) -> bool:
        """
        Checks, whether action pointer is before first action in player turn

        :return: True in case action pointer is before first action, false otherwise
        """
        return self.__current_action == -1


    @property
    def on_last_action(self) -> bool:
        """
        Checks, whether action pointer is on last action for current turn and player

        :return: True in case this is last action, false otherwise
        """
        return self.__current_action == self.last_action_index


    def add_action(self, action: "GameAction") -> None:
        """
        Adds given game action to game history. Mote that added action **will NOT get executed** in process
        :param action: action Action to be added to history
        """
        if not self.in_preset:
            raise IllegalHistoryOperation("Control action invoked in browsing mode!")

        self.__turns[self.__current_turn][self.__current_player].append(action)
        self.__current_action += 1


    def end_turn(self) -> None:
        """ Ends current game turn """

        if not self.in_preset:
            raise IllegalHistoryOperation("Control action invoked in browsing mode")

        if self.on_last_player:
            self.start_next_game_turn()
        else:
            self.start_next_player_turn()


    def undo_player_turn(self) -> None:
        """
        Undoes every action, which has been done in last player's turn setting state to before
        the first action this player made (but still remaining in their turn)
        """
        if not self.in_preset:
            raise IllegalHistoryOperation("Control action invoked in browsing mode")

        if self.before_first_action:
            if self.at_start:
                return

            self.delete_player_turn()
            if self.on_first_player:
                self.delete_game_turn()

            self.move_to_previous()

        self.undo_player_actions()
        self.clear_player_turn()


    def move_action_back(self) -> None:
        """ Moves one action back in history """
        if not self.before_first_action:
            self.current_action.undo()

        self.move_to_previous()


    def move_action_forth(self) -> None:
        """ Moves one action forth towards present """
        self.move_to_next()
        if not self.before_first_action:
            self.current_action.execute()


    def move_turn_back(self) -> None:
        """ Moves to the start of previous turn """
        if self.before_first_action:
            if self.at_start:
                return
            self.move_to_previous()
        self.undo_player_actions()


    def move_turn_forth(self) -> None:
        """ Moves to the start of next turn """
        if self.on_last_action:
            if self.in_preset:
                return
            self.move_to_next()

        self.redo_player_actions()

        self.move_to_next()


    def move_to_present(self) -> None:
        """ Move to the present turn and action """
        while not self.in_preset:
            self.move_turn_forth()


    @property
    def active_player(self) -> IPlayer:
        """ Retrieves reference to currently active player """
        return self.__players[self.__current_player]


    @property
    def turns_count(self) -> int:
        """ Retrieves number of current turn """
        return len(self.__turns)


    @property
    def remaining_turn(self) -> int:
        """ Computes how many turns remain until game finishes """
        return self.__turn_limit - self.turns_count


    @property
    def in_preset(self) -> bool:
        """
        Checks, whether history is in the present
        :return: True in case history is in the present moment, false otherwise
        """
        return self.on_present_turn and self.on_present_player and self.on_last_action


    @property
    def at_start(self) -> bool:
        """
        Checks, whether history is in the very first moment
        :return: True in case there are no previous actions, false otherwise
        """
        return self.__current_turn == 0 and self.on_first_player and self.before_first_action


    @property
    def current_player(self) -> int:
        """ Return index of current player """
        return self.__current_player


    @property
    def current_turn(self) -> int:
        """ Return index of current turn """
        return self.__current_turn


    @property
    def current_action_index(self):
        """ Return index of current action """
        return self.__current_action


    def is_history_log(self, turn: int, player: int, action: int) -> bool:
        """
        Check if given history log is before current time or after

        :param turn: turn of log
        :param player: player of log
        :param action: action number of log
        :return: True if log is in history, False if log is in the future
        """

        if turn < self.current_turn:
            return True

        if turn == self.current_turn:
            if player < self.current_player:
                return True

            if player == self.current_player:
                if self.__current_action == -1:
                    return True
                elif action <= self.__current_action:
                    return True

        return False


    def to_history_point(self, turn: int, player: Optional[int], action: Optional[int]) -> None:
        """
        Move history to target point

        :param turn: target turn
        :param player: target player
        :param action:  target action
        """
        if action is None:
            action = 0

        if player is None:
            player = 0

        if self.current_turn < turn:
            direction = 1
        elif self.current_turn > turn:
            direction = -1
        else:
            if self.current_player < player:
                direction = 1
            elif self.current_player > player:
                direction = -1
            else:
                if self.current_action_index < action:
                    direction = 1
                else:
                    direction = -1

        while not (self.current_turn == turn and self.current_player == player and self.current_action_index == action):
            if direction == 1:
                self.move_action_forth()
            else:
                self.move_action_back()


    def to_html(self):
        """ Export log to HTML format """
        result = '<ul>'
        for turn in range(self.turns_count):
            player_turn = self.__turns[turn]
            for p_turn in range(len(player_turn)):
                actions = player_turn[p_turn]
                for i, action in enumerate(actions):
                    color = 'black' if self.is_history_log(turn, p_turn, i) else 'red'
                    result += '<li style="color: {}">Turn {} - Player {}- {}</li>'.format(color, turn, p_turn, action)
        result += '</ul>'

        return result


    def to_xml(self) -> str:
        """ Export log to XML format"""
        root = et.Element('GameHistory')

        for turn in range(self.turns_count):
            _turn = et.SubElement(root, 'Turn', index=str(turn))
            player_turn = self.__turns[turn]
            for p_turn in range(len(player_turn)):
                player = et.SubElement(_turn, 'Player', index=str(p_turn), name=self.__players[p_turn].name)
                actions = player_turn[p_turn]
                for i, action in enumerate(actions):
                    action.xml(player)

        tree = et.ElementTree(root)

        return et.tostring(tree.getroot(), 'utf-8', 'xml').decode('utf-8')


    def to_model(self):
        """ Convert history to Model vor QTreeView """
        from PyQt5.QtGui import QStandardItemModel, QStandardItem
        from PyQt5.QtGui import QColor, QBrush

        model = QStandardItemModel()
        root = model.invisibleRootItem()

        for turn in range(self.turns_count):
            color = QColor(0, 0, 0) if self.is_history_log(turn, 0, 0) else QColor(255, 0, 0)
            _round = QStandardItem('Round {}'.format(turn))
            _round.setForeground(color)
            _round.setData((turn, None, None))
            root.appendRow(_round)
            player_turn = self.__turns[turn]

            for p_turn in range(len(player_turn)):
                color = QColor(0, 0, 0) if self.is_history_log(turn, p_turn, 0) else QColor(255, 0, 0)
                player = QStandardItem('Player {} - {}'.format(p_turn, self.__players[p_turn].name))
                player.setForeground(color)
                player.setData((turn, p_turn, None))
                _round.appendRow(player)
                actions = player_turn[p_turn]

                for i, action in enumerate(actions):
                    color = QColor(0, 0, 0) if self.is_history_log(turn, p_turn, i) else QColor(255, 0, 0)
                    _action = QStandardItem(str(action))
                    _action.setForeground(QBrush(color))
                    _action.setToolTip(str(action))
                    _action.setData((turn, p_turn, i))

                    player.appendRow(_action)

        return model


    def __str__(self):
        return self.to_html()
