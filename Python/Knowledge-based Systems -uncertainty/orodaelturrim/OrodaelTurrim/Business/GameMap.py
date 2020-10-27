import copy
from collections import deque
from typing import List, TYPE_CHECKING, Dict, Union, Set, Tuple, Optional

from OrodaelTurrim.Structure.Exceptions import IllegalArgumentException
from OrodaelTurrim.Structure.Position import Position, OffsetPosition
from OrodaelTurrim.Structure.TypeStrucutre import DoubleLinkedList
from OrodaelTurrim.Structure.Utils import Singleton
from OrodaelTurrim.Structure.Enums import Nudge, TerrainType

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Enums import Nudge, TerrainType
    from OrodaelTurrim.Structure.Terrain import Terrain


class GameMap:
    """ Object representing rectangular game map """


    def __init__(self, width: int, height: int, tiles: List[List[Union['TerrainType', str]]] = None):
        self.__size = (width, height)
        if width % 2 == 0 or height % 2 == 0:
            raise IllegalArgumentException('Map size must be odd numbers')

        if width < 3:
            raise IllegalArgumentException('Map width must be greater than 2')

        if height < 3:
            raise IllegalArgumentException('Map height must be greater than 2')

        self.__width = width
        self.__height = height

        self.__vertical_radius = (height - 1) // 2
        self.__horizontal_radius = (width - 1) // 2

        self.__visible_tiles_cache = {}

        self.__tiles = []  # type: List[List[Union[Terrain,None]]]
        for i in range(height):
            self.__tiles.append([])
            for j in range(width):
                self.__tiles[i].append(None)

        if tiles:
            for y, terrain_list in enumerate(tiles):
                for x, terrain_type in enumerate(terrain_list):
                    position = OffsetPosition(x - self.__horizontal_radius, y - self.__vertical_radius)
                    if type(terrain_type) is TerrainType:
                        self.set_tile(position, terrain_type.value)
                    elif type(terrain_type) is str:
                        _terrain_type = TerrainType.from_char(terrain_type).value
                        if _terrain_type is None:
                            raise IllegalArgumentException('Invalid tile character {}'.format(terrain_type))
                        self.set_tile(position, TerrainType.from_char(terrain_type).value)
                    else:
                        raise IllegalArgumentException('Map tiles could be TerrainType enum or string representation!')


    def __sizeof__(self):
        return self.__size


    def __getitem__(self, position: Position) -> Union['Terrain', None]:
        position_offset = position.offset
        return self.__tiles[position_offset.q + self.__horizontal_radius][position_offset.r + self.__vertical_radius]


    def set_tile(self, position: Position, terrain: 'Terrain') -> None:
        """
        Set target position tile

        :param position: position which should be set
        :param terrain: terrain object for position
        """
        offset = self.__size[0] // 2, self.__size[1] // 2
        column = position.offset.q + offset[0]
        row = position.offset.r + offset[1]

        self.__tiles[column][row] = terrain


    @property
    def tiles(self):
        """ Iterator for all map tiles """
        for y in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
            for x in range(-self.__vertical_radius, self.__vertical_radius + 1):
                yield OffsetPosition(y, x)


    @property
    def size(self) -> Tuple[int, int]:
        """
        Get size of the map

        :return: Tuple of width and height
        """
        return self.__width, self.__height


    @property
    def width(self) -> int:
        """ Get width of the map """
        return self.__width


    @property
    def height(self) -> int:
        """ Get height of the map """
        return self.__height


    @property
    def vertical_radius(self) -> int:
        """ Vertical radius of map in tiles """
        return self.__vertical_radius


    @property
    def horizontal_radius(self) -> int:
        """ Horizontal radius of map in tiles """
        return self.__horizontal_radius


    def position_on_map(self, position: Position) -> bool:
        """
        Check if position is on map

        :param position: target position
        :return: True if position is on map, False otherwise
        """
        x = position.offset.r
        y = position.offset.q

        vertical = - self.__vertical_radius <= x <= self.__vertical_radius
        horizontal = - self.__horizontal_radius <= y <= self.__horizontal_radius

        return vertical and horizontal


    def filter_positions_on_map(self, positions: List[Position]) -> List[Position]:
        """
        Filter list of positions, left only on map positions

        :param positions: target positions
        :return: List of positions at map
        """
        on_map_positions = []
        for position in positions:
            if self.position_on_map(position):
                on_map_positions.append(position)

        return on_map_positions


    def position_on_edge(self, position: Position) -> bool:
        """
        Determinate, if positions is on the edge of the map
        :param position: target position
        :return: True if position is on the edge, False otherwise
        """
        x = position.offset.r
        y = position.offset.q

        vertical = self.__vertical_radius == x or -self.__vertical_radius == x
        horizontal = self.__horizontal_radius == y or -self.__horizontal_radius == y

        return vertical or horizontal


    def can_been_seen(self, start: Position, end: Position, sight: int, nudge: 'Nudge') -> bool:
        """
         Check whether the line from start to end exhausts given sight with given nudge correction

        :param start: Starting position of line
        :param end: Ending position of line
        :param sight: Given sight point to be checked upon
        :param nudge: Correcting nudge
        :return: True in case sight has NOT been exhausted, false otherwise
        """
        if start == end:
            return True
        line = start.plot_line(end, nudge)

        for tile in line[1:-1]:
            int_tile = tile.int_coord.offset
            if not self.position_on_map(int_tile):
                return False
            sight = self[int_tile].get_remaining_sigh(sight)

        return sight > 0


    def get_visible_tiles(self, position: Position, sight: int) -> Set[Position]:
        """
        Computes set of visible tiles from specified tile with given sight

        :param position: Starting position of computation
        :param sight: Current level of sight
        :return: Set of visible tiles from specified tile with given sight
        """
        if not self.position_on_map(position):
            return set()

        # Check the cache information
        if position in self.__visible_tiles_cache and sight in self.__visible_tiles_cache[position]:
            return copy.deepcopy(self.__visible_tiles_cache[position][sight])

        visited = set()
        visible = set()
        pool = set()
        pool.add(position)

        while len(pool) > 0:
            current = pool.pop()

            if current not in visited:
                visited.add(current)
            else:
                continue

            if current not in visible and (
                    self.can_been_seen(position, current, sight, Nudge.NEGATIVE) or self.can_been_seen(position,
                                                                                                       current, sight,
                                                                                                       Nudge.POSITIVE)):
                visible.add(current)

            for tile in current.get_all_neighbours():
                if self.position_on_map(tile) and tile not in visited:
                    pool.add(tile)

        # Save computed value to cache
        if position not in self.__visible_tiles_cache:
            self.__visible_tiles_cache[position] = {}
        if sight not in self.__visible_tiles_cache[position]:
            self.__visible_tiles_cache[position][sight] = copy.deepcopy(visible)

        return visible


    def get_accessible_tiles(self, position: Position, actions: int) -> Dict[Position, int]:
        """
        Computes map with accessible tiles as keys and remaining action points as values from specified tile
        with given action points

        :param position: Starting position of computation
        :param actions: Current action points
        :return: Dict with accessible tiles as keys and remaining action points as values
        """
        if not self.position_on_map(position):
            return {}

        pool = deque()
        pool.append(position)

        result_map = {position: actions}

        while len(pool) != 0:
            current = pool.popleft()
            current_actions = result_map[current]

            for neighbour in current.get_all_neighbours():
                if self.position_on_map(neighbour):
                    move_cost = self[current].get_move_cost(self[neighbour].terrain_type)
                    remaining = current_actions - move_cost

                    if remaining >= 0 and (neighbour not in result_map or result_map[neighbour] < remaining):
                        result_map[neighbour] = remaining
                        pool.append(neighbour)

        return result_map


    @property
    def border_tiles(self) -> Set[Position]:
        """
        Retrieves set of tiles on the edge of game map

        :return: Set of border tiles
        """
        border_tiles = set()
        for x in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
            border_tiles.add(OffsetPosition(x, -self.__vertical_radius))
            border_tiles.add(OffsetPosition(x, self.__vertical_radius))

        for y in range(-self.__vertical_radius, self.__vertical_radius + 1):
            border_tiles.add(OffsetPosition(-self.__horizontal_radius, y))
            border_tiles.add(OffsetPosition(self.__horizontal_radius, y))

        return border_tiles


    @property
    def inner_tiles(self) -> Set[Position]:
        inner_tiles = set()
        for x in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
            for y in range(-self.__vertical_radius, self.__vertical_radius + 1):
                inner_tiles.add(OffsetPosition(x, y))

        return inner_tiles


    def __repr__(self):
        map_repr = ''
        for i, row in enumerate(self.__tiles):
            if i % 2 == 1:
                map_repr += ' '
            for column in row:
                map_repr += column.char()
                map_repr += ' '

            map_repr += '\n'

        return map_repr


class BorderTiles(metaclass=Singleton):
    """
    This class provides functionality for iterating over neighbour border tiles.
    Class is singleton cause of speedup
    """


    def __init__(self, game_map: GameMap = None):
        self.__game_map = game_map

        self.__border_tiles = DoubleLinkedList()
        self.__create_linked_list()


    def get_position(self, starting_position: Position, shift: int) -> Optional[Position]:
        """
        with this method you can iterate over border tiles in clockwise or counterclockwise order

        :param starting_position: Starting on edge position
        :param shift: number of positions positive for clockwise, negative for counterclockwise
        :return: target position or None if starting position is not on the edge
        """

        if not self.__game_map.position_on_edge(starting_position):
            return None

        self.__border_tiles.pointer = self.__border_tiles.head

        while self.__border_tiles.value != starting_position:
            self.__border_tiles.next()

        for i in range(abs(shift)):
            if shift < 0:
                self.__border_tiles.previous()
            else:
                self.__border_tiles.next()

        return self.__border_tiles.value


    def get_position_list(self, starting_position: Position, length: int) -> List[Position]:
        """
        Get list of positions on the edge. List will have clockwise order

        :param starting_position: starting position of the list
        :param length:  number of positions in return list
        :return: List of length Positions (with starting_position)
        """
        self.__border_tiles.pointer = self.__border_tiles.head

        while self.__border_tiles.value != starting_position:
            self.__border_tiles.next()

        result_list = []
        for i in range(length):
            result_list.append(self.__border_tiles.value)
            self.__border_tiles.next()

        return result_list


    def __create_linked_list(self):
        """ Create linked list for iterating over edge tiles """

        # In the corners, there are more than one neighbor. Precedence list will chose correct one
        precedence = {OffsetPosition(self.__game_map.horizontal_radius, self.__game_map.vertical_radius),
                      OffsetPosition(-self.__game_map.horizontal_radius, self.__game_map.vertical_radius),
                      OffsetPosition(self.__game_map.horizontal_radius, -self.__game_map.vertical_radius),
                      OffsetPosition(-self.__game_map.horizontal_radius, -self.__game_map.vertical_radius),
                      OffsetPosition(-self.__game_map.horizontal_radius + 2, -self.__game_map.vertical_radius)}

        first = OffsetPosition(-self.__game_map.horizontal_radius, -self.__game_map.vertical_radius)
        second = OffsetPosition(-self.__game_map.horizontal_radius + 1, -self.__game_map.vertical_radius)
        self.__border_tiles.push_back(first)
        self.__border_tiles.push_back(second)

        tiles = self.__game_map.border_tiles
        tiles.remove(first)
        tiles.remove(second)

        current = self.__border_tiles.head.value
        while tiles:
            _next_set = set(current.get_all_neighbours()).intersection(tiles)
            if len(_next_set) > 1:
                _next_set = _next_set.intersection(precedence)

            _next = _next_set.pop()

            current = _next
            self.__border_tiles.push_back(_next)
            tiles.remove(_next)

        self.__border_tiles.head.next = self.__border_tiles.tail
        self.__border_tiles.tail.previous = self.__border_tiles.head
