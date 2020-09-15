import random
from abc import ABC, abstractmethod
from typing import List, Union

from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy
from OrodaelTurrim.Structure.Position import Position
from OrodaelTurrim.Structure.Exceptions import IllegalActionException


class TileFilter(ABC):
    """
    Abstract class that represent Tile filter. Purpose of class is get List of positions and return filtered positions
    """


    @abstractmethod
    def filter(self, positions: Position, tiles: List[Position]):
        """
        Filter given positions

        :param positions: Current positions of game object
        :param tiles: List of possible positions
        :return: List of filtered positions
        """
        pass


    @staticmethod
    def use_filter(position: Position, filters: List["TileFilter"], tiles: List[Position]) -> Union[Position, None]:
        """
        Use list of filters to get on final positions.
        Method use all filter one by one. If filter return zero positions, this filter will be skipped,
        if filter return exact one position, other filters will be skipped. If we have more then one position
        at the end, chose one position randomly

        :param position: Position of the game object
        :param filters: List of filters
        :param tiles: list of possible positions
        :return: On target position or None if list of initial positions was empty
        """

        if not tiles:
            return None

        for _filter in filters:
            # Use current filter
            filtered = _filter.filter(position, tiles)

            if not set(filtered) <= set(tiles):
                raise IllegalActionException('Filter did not return subset of original positions!')

            # If we have at least one positions use this filter
            if len(filtered) >= 1:
                tiles = filtered
                # IF we have only one position we dont need to use other filters
                if len(filtered) == 1:
                    break

        return TileFilter.filter_random(tiles)


    @staticmethod
    def filter_random(tiles: List[Position]) -> Position:
        """ Return random position from the list """
        return random.choice(tiles)


class MoveFilter(TileFilter):
    """ Specialization for move filters """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy):
        self.map_proxy = map_proxy  # type: MapProxy
        self.game_object_proxy = game_object_proxy  # type: GameObjectProxy


    @abstractmethod
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        pass


class AttackFilter(TileFilter):
    """ Specialization for attack filter """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy):
        self.map_proxy = map_proxy
        self.game_object_proxy = game_object_proxy


    @abstractmethod
    def filter(self, position: Position, tiles: List[Position]) -> List[Position]:
        pass


class FilterReference:
    """ Class wrapper for handle information about filter reference """


    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
