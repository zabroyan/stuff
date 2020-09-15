import os
import random
from typing import List, Set, Union

from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Structure.Enums import TerrainType
from OrodaelTurrim.Structure.Exceptions import IllegalArgumentException
from OrodaelTurrim.Structure.Position import OffsetPosition, Position
from OrodaelTurrim.Structure.Terrain import River, Field, Terrain
from OrodaelTurrim.config import Config

# Precision of terrain types (how many items will be in random list
PRECISION = 100


class MapGenerator:
    """ Class for generating map for the game """


    def __init__(self, width: int, height: int, seed: int = None):
        """
        :param width: - width of the map (must be ood number)
        :param height: - height of the map (must be odd number)
        :param seed: - random seed for generating map
        """
        self.__width = width
        self.__height = height

        self.__vertical_radius = (height - 1) // 2
        self.__horizontal_radius = (width - 1) // 2

        self.__game_map = GameMap(width, height)

        self.__border_tiles = self.__game_map.border_tiles

        self.__initialize_generator_config()

        if not seed:
            seed = Config.MAP_RANDOM_SEED

        if not seed:
            seed = int.from_bytes(os.urandom(50), 'big')
            Config.MAP_RANDOM_SEED = seed

        random.seed(seed)

        self.__base_random_list = self.create_base_random_list()

        for i in range(-self.__vertical_radius, self.__vertical_radius + 1):
            for j in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
                self.__game_map.set_tile(OffsetPosition(i, j), Field())


    def create_base_random_list(self) -> List[TerrainType]:
        """
        Create random list of terrains based on probability constants

        :return: List of terrain types
        """
        random_list = []

        for i in range(int(self.mountain_frq * PRECISION)):
            random_list.append(TerrainType.MOUNTAIN)

        for i in range(int(self.field_frq * PRECISION)):
            random_list.append(TerrainType.FIELD)

        for i in range(int(self.hill_frq * PRECISION)):
            random_list.append(TerrainType.HILL)

        for i in range(int(self.forest_frq * PRECISION)):
            random_list.append(TerrainType.FOREST)

        for i in range(int(self.village_frq * PRECISION)):
            random_list.append(TerrainType.VILLAGE)

        return random_list


    def get_random_terrain_type(self, position: Position) -> Terrain:
        """
        Get random terrain type for target position. Based on neighbours
        """

        neigbours = self.__game_map.filter_positions_on_map(position.get_all_neighbours())

        for neigbour in neigbours:
            if self.__game_map[neigbour].terrain_type not in (TerrainType.FIELD, TerrainType.RIVER):
                for i in range(int(self.neighbour_add * PRECISION)):
                    self.__base_random_list.append(self.__game_map[neigbour].terrain_type)

        terrain_type = random.choice(self.__base_random_list)

        return terrain_type.value


    def generate(self, game_map: List[List[Union[str, TerrainType]]] = None) -> GameMap:
        """ Generate map method """
        if game_map:
            if len(game_map) != self.__height:
                raise IllegalArgumentException('Map configuration did not correspond with map height!')
            if max([len(x) for x in game_map]) != min([len(x) for x in game_map]):
                raise IllegalArgumentException('Size mismatch in map config!')
            if len(game_map[0]) != self.__width:
                raise IllegalArgumentException('Map configuration did not correspond with map with!')
            self.__game_map = GameMap(self.__width, self.__height, game_map)
        else:
            self.__generate_river()
            self.__generate_tiles()

        return self.__game_map


    def __initialize_generator_config(self):

        self.field_frq = Config.FIELD_FREQUENCY if Config.FIELD_FREQUENCY is not None else 0.5
        self.mountain_frq = Config.MOUNTAIN_FREQUENCY if Config.MOUNTAIN_FREQUENCY is not None else 0.1
        self.hill_frq = Config.HILL_FREQUENCY if Config.HILL_FREQUENCY is not None else 0.1
        self.forest_frq = Config.FOREST_FREQUENCY if Config.FOREST_FREQUENCY is not None else 0.2
        self.village_frq = Config.VILLAGE_FREQUENCY if Config.VILLAGE_FREQUENCY is not None else 0.01

        self.river_prob = Config.RIVER_ON_MAP_PROBABILITY if Config.RIVER_ON_MAP_PROBABILITY is not None else 0.9

        self.neighbour_add = Config.NEIGHBOUR_ADD if Config.NEIGHBOUR_ADD is not None else 0.01


    def __generate_tiles(self):
        """ Generate all tiles (without water) """
        for i in range(-self.__vertical_radius, self.__vertical_radius + 1):
            for j in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
                position = OffsetPosition(i, j)
                if self.__game_map[position].terrain_type != TerrainType.RIVER:
                    self.__game_map.set_tile(position, self.get_random_terrain_type(position))


    def __generate_river(self):
        """ Generate rivver tiles. There will be only one river with starting and ending at the map edge"""


        def filter_river_neighbour(position, ancestor):
            _neighbours = [self.__game_map[x].terrain_type for x in
                           self.__game_map.filter_positions_on_map(position.get_all_neighbours()) if ancestor != x]

            if TerrainType.RIVER in _neighbours:
                return False

            return True


        if random.random() < self.river_prob:
            current = self.__river_start_position()
            river_length = 1
            self.__game_map.set_tile(current, River())

            while True:
                # Filter neighbours on map
                neighbours = self.__game_map.filter_positions_on_map(current.get_all_neighbours())
                # Filter neighbours which are not RIVER
                neighbours = [x for x in neighbours if self.__game_map[x].terrain_type != TerrainType.RIVER]
                # Filter neighbours which are have not river as neighbour
                neighbours = [x for x in neighbours if filter_river_neighbour(x, current)]
                # Filter border tiles under size factor
                if river_length < 3:
                    neighbours = [x for x in neighbours if not self.__game_map.position_on_edge(x)]

                neighbours.sort(key=lambda x: (x.length() + 1 if self.__game_map.position_on_edge(x) else 0))
                if neighbours:
                    for i in range(6):
                        neighbours.append(neighbours[0])

                # If cannot continue generate new river
                if not neighbours:
                    for i in range(-self.__vertical_radius, self.__vertical_radius + 1):
                        for j in range(-self.__horizontal_radius, self.__horizontal_radius + 1):
                            self.__game_map.set_tile(OffsetPosition(i, j), Field())
                    self.__generate_river()
                    break

                neighbour = random.choice(neighbours)
                self.__game_map.set_tile(neighbour, River())
                if self.__game_map.position_on_edge(neighbour):
                    break
                else:
                    current = neighbour
                    river_length += 1


    def __river_start_position(self) -> Position:
        """ Get river start position """
        left_bottom_corner = OffsetPosition(-self.__horizontal_radius, self.__vertical_radius)
        right_bottom_corner = OffsetPosition(self.__horizontal_radius, self.__vertical_radius)

        while True:
            starting_position = self.__pick_random_position(self.__border_tiles)

            if starting_position != left_bottom_corner and starting_position != right_bottom_corner:
                break

        return starting_position


    def __pick_random_position(self, positions: Set[Position]) -> Position:
        """ Pick random position from the set of positions """
        return random.choice(tuple(positions))
