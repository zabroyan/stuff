from typing import List, Dict, Set

from PyQt5.QtGui import QColor

from OrodaelTurrim.Business.Interface.Player import IPlayer
from OrodaelTurrim.Structure.Enums import GameRole
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject
from OrodaelTurrim.Structure.Position import Position


class Border:
    """
    Class wrapper for border of tile. Store line thickness of each edge and color of the edges
    """


    def __init__(self, right_lower: int = 0, lower: int = 0, left_lower: int = 0, left_upper: int = 0, upper: int = 0,
                 right_upper: int = 0, color: [List[QColor], QColor] = QColor(0, 0, 0)):
        """
        :param right_lower: thick of right lower edge
        :param lower: thick of lower edge
        :param left_lower: thick of left lower edge
        :param left_upper: thick of left upper edge
        :param upper: thick of upper edge
        :param right_upper: thick of right upper edge
        :param color: list of colors for all edges
        """
        self.upper = upper
        self.right_upper = right_upper
        self.right_lower = right_lower
        self.lower = lower
        self.left_lower = left_lower
        self.left_upper = left_upper
        self.__color = color


    @staticmethod
    def full(weight: int, color: QColor) -> "Border":
        """ Create Border instance with all border with same width """
        return Border(weight, weight, weight, weight, weight, weight, color)


    @property
    def order(self) -> List[int]:
        """ Return edges thick in order of the borders same as directions of neighbours """
        return [self.right_upper, self.right_lower, self.lower, self.left_lower, self.left_upper, self.upper]


    @property
    def color(self) -> List[QColor]:
        """ Get list of colors of edges """
        if type(self.__color) is list:
            return self.__color
        else:
            return [self.__color for x in range(6)]


    @color.setter
    def color(self, value: [List[QColor], QColor]):
        """ Set color of the edges """
        self.__color = value


    def __str__(self):
        return '<BORDER> U: {}, RU: {}, RL: {}, L: {}, LL: {}, LU: {}'.format(self.upper, self.right_upper,
                                                                              self.right_lower,
                                                                              self.lower, self.left_lower,
                                                                              self.left_upper)


class VisibilityMap:
    """
    Map which holds visibility of tiles. The first level represents registered players for the game, second
    level holds map of positions, which keys are visible to that player. The third level is array of game
    objects, which contribute to the visibility of associated position.

    Once again this might seem confusing a lot, so for clarity, here is example:

    Here first player owns game object 0 and 1. Game object 0 can see positions [0,0], [0,1] and [1,0]. Game
    object 1 can see positions [0,1], [1,0] and [1,1].

     Player 1
        Position [0,0]
            GameObject 0
        Position [1,0]
            GameObject 0

            GameObject 1
        Position [1,1]
            GameObject 1
              ...
    """


    def __init__(self):
        self.__visibility_map = {}  # type: Dict[IPlayer, Dict[Position, Set[GameObject]]]


    def register_player(self, player: IPlayer) -> None:
        """ Register player to visibility map """
        self.__visibility_map[player] = {}


    def add_vision(self, game_object: GameObject, new_visible_positions: Set[Position]) -> None:
        """ Add visible tiles for target game object """
        for position in new_visible_positions:
            if position not in self.__visibility_map[game_object.owner]:
                self.__visibility_map[game_object.owner][position] = set()

            self.__visibility_map[game_object.owner][position].add(game_object)


    def remove_vision(self, game_object: GameObject, no_longer_visible: Set[Position]) -> None:
        """ Remove visible tiles for target game object """
        player_map = self.__visibility_map[game_object.owner]  # type: Dict[Position,Set[GameObject]]

        for position in no_longer_visible:
            if position not in player_map:
                continue

            watcher = player_map[position]
            try:
                watcher.remove(game_object)
            except KeyError:
                pass

            if len(watcher) == 0:
                player_map.pop(position)


    def get_visible_tiles(self, player: IPlayer) -> Set[Position]:
        """ Get all visible tiles for one player """
        return set(self.__visibility_map[player].keys())


    def get_watching_enemies(self, role: GameRole, position: Position) -> List[GameObject]:
        """ Get list of enemies watching target position """
        watching_enemies = set()
        for player in self.__visibility_map.keys():
            if role.is_enemy(player.role):
                player_visibility = self.__visibility_map[player]
                if position in player_visibility:
                    watching_enemies.update(player_visibility[position])

        return list(watching_enemies)


    def clear(self):
        """ Clear visibility map. Registered players stayed with empty visibility """
        for player in self.__visibility_map.keys():
            self.__visibility_map[player] = {}


    def player_registered(self, player: IPlayer) -> bool:
        """
        Check if given player is registered in VisibilityMap

        :param player: Target player to check
        :return: True if player is registered, False otherwise
        """
        return player in self.__visibility_map.keys()


    def text_format(self):
        """ Print visibility map to console """
        for player in self.__visibility_map.keys():
            print('** {} **'.format(player.name))
            for position in self.__visibility_map[player].keys():
                print('    - {}'.format(position))
                for game_object in self.__visibility_map[player][position]:
                    print('        - {} at {}'.format(game_object.object_type, game_object.position))
