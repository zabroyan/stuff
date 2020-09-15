from typing import TYPE_CHECKING, Optional, Set, Dict, List

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Position import Position
    from OrodaelTurrim.Structure.Enums import TerrainType, AttributeType, EffectType, GameObjectType, GameRole
    from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation, UncertaintySpawn
    from OrodaelTurrim.Business.GameEngine import GameEngine
    from OrodaelTurrim.Business.Interface.Player import IPlayer, PlayerTag


class MapProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.__get_map_height = game_engine.get_map_height
        self.__get_map_width = game_engine.get_map_width
        self.__get_terrain_type = game_engine.get_terrain_type
        self.__is_position_on_map = game_engine.is_position_on_map
        self.__is_position_occupied = game_engine.is_position_occupied
        self.__get_bases_positions = game_engine.get_bases_positions
        self.__get_border_tiles = game_engine.get_border_tiles
        self.__get_inner_tiles = game_engine.get_inner_tiles
        self.__get_player_visible_tiles = game_engine.get_current_player_visible_tiles
        self.__compute_visible_tiles = game_engine.compute_visible_tiles
        self.__compute_accessible_tiles = game_engine.compute_accessible_tiles
        self.__player_have_base = game_engine.player_have_base
        del game_engine


    def get_map_height(self) -> int:
        """ Retrieves number of tiles in each column of game map """
        return self.__get_map_height()


    def get_map_width(self) -> int:
        """ Retrieves number of tiles in each row of game map """
        return self.__get_map_width()


    def get_terrain_type(self, position: "Position") -> Optional["TerrainType"]:
        """
        Retrieves terrain type of given position
        Return None if Positions is not on map

        :param position: Position to get terrain type for
        :return: Terrain type of given position
        """
        return self.__get_terrain_type(position)


    def is_position_on_map(self, position: "Position") -> bool:
        """
        Checks whether given position is on map or not

        :param position: Position to be checked
        :return: True in case position is within map bounds, False otherwise
        """
        return self.__is_position_on_map(position)


    def is_position_occupied(self, position: "Position") -> bool:
        """
        Checks whether given position is occupied or not. You can check only visible positions

        :param position: Position to be checked
        :return: True in case there is game object on given position, False otherwise,
                 None if user did not see the position
        """
        return self.__is_position_occupied(position)


    def get_bases_positions(self) -> Set["Position"]:
        """
        Retrieves positions of defenders' bases

        :return: Positions of defenders' bases
        """
        return self.__get_bases_positions()


    def get_border_tiles(self) -> Set["Position"]:
        """ Retrieves set of tiles on the edge of game map """
        return self.__get_border_tiles()


    def get_inner_tiles(self) -> Set['Position']:
        """ Retrieves set of tiles which are not on the map edge """
        return self.__get_inner_tiles()


    def get_player_visible_tiles(self) -> Set["Position"]:
        """
        Retrieves set of visible tiles for player.

        :return:  Set of visible tiles
        """
        return self.__get_player_visible_tiles()


    def compute_visible_tiles(self, position: "Position", sight: int) -> Optional[Set["Position"]]:
        """
        Computes set of visible tiles in sight radius from given position.

        :param position: Position to use as base point of computation
        :param sight: Value of sight to consider for computation
        :return: Set of visible tiles of specified game object.
                 None if positions is not on map
        """
        return self.__compute_visible_tiles(position, sight)


    def compute_accessible_tiles(self, position: "Position", actions: int) -> Optional[Dict["Position", int]]:
        """
        Computes map with accessible tiles as keys and remaining action points as values from specified position
        and number of remaining action points

        :param position: Position to use as base point of computation
        :param actions: Number of action points to consider for computation
        :return: Dict with accessible tiles as keys and remaining action points as values
                 None if positions is not on map
        """
        return self.__compute_accessible_tiles(position, actions)


    def player_have_base(self, player: "PlayerTag") -> bool:
        """
        Check if player already have a base

        :param player: Target player to be checked
        :return: True if player have base, False otherwise
        """
        return self.__player_have_base(player)


class GameObjectProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.__get_attribute = game_engine.get_attribute
        self.__get_current_hit_points = game_engine.get_current_hit_points
        self.__get_attack_effects = game_engine.get_attack_effect
        self.__get_resistances = game_engine.get_resistances
        self.__get_active_effects = game_engine.get_active_effects
        self.__get_object_type = game_engine.get_object_type
        self.__get_role = game_engine.get_role
        self.__get_visible_tiles = game_engine.get_visible_tiles
        self.__get_visible_enemies = game_engine.get_visible_enemies

        self.__get_income = game_engine.get_income
        self.__get_resources = game_engine.get_resources

        self.__get_current_round = game_engine.get_current_round
        del game_engine


    def get_attribute(self, position: "Position", attribute_type: "AttributeType") -> Optional[float]:
        """
        Retrieves value of specified attribute of game object on specified position

        :param position: Position of queried game object
        :param attribute_type: Type of attribute to be retrieved
        :return: Value of specified attribute
                 None if there is no unit at the position
        """
        return self.__get_attribute(position, attribute_type)


    def get_current_hit_points(self, position: "Position") -> Optional[float]:
        """
        Retrieves amount of currently remaining hit points of game object on specified position

        :param position: Position of queried game object
        :return: Amount of currently remaining hit points
                 None if there is no unit at the position or you don't see that position
        """
        return self.__get_current_hit_points(position)


    def get_attack_effects(self, position: "Position") -> Optional[Set["EffectType"]]:
        """
        Retrieves the types of effect to be applied to the target of attack of game object on specified position

        :param position: Position of queried game object
        :return: Set of types of effect to be applied upon attacking
                 None if there is no unit at the position or you don't see that position
        """
        return self.__get_attack_effects(position)


    def get_resistances(self, position: "Position") -> Optional[Set["EffectType"]]:
        """
        Retrieves the types of effect which will NOT affect game object on specified position

        :param position: Position of queried game object
        :return: Set of resistances of game object on specified position
                 None if there is no unit at the position or player don't see that position
        """
        return self.__get_resistances(position)


    def get_active_effects(self, position: "Position") -> Optional[Dict["EffectType", int]]:
        """
        Retrieves types of currently active effects and their durations on game object on specified position

        :param position: Position of queried game object
        :return: Dict of types of active effects and associated remaining durations
                 None if there is no unit at the position or you don''t see that position
        """
        return self.__get_active_effects(position)


    def get_object_type(self, position: "Position") -> Optional["GameObjectType"]:
        """
        Retrieves the type of game object on the specified position. The player must see that position.
        This function could be used to get enemy types.

        :param position: Position of queried game object
        :return: Type of game object on specified position
                 GameObjectType.NONE if there is no unit at the position
                 None if player don't see that position
        """
        return self.__get_object_type(position)


    def get_role(self, position: "Position") -> "GameRole":
        """
        Retrieves the role of game object on specified position

        :param position: Position of queried game object
        :return: Role of game object on specified position
                 GameRole.NEUTRAL if there is no unit at the position,
                 None if you don't see that position
        """
        return self.__get_role(position)


    def get_visible_tiles(self, position: "Position") -> Optional[Set["Position"]]:
        """
        Retrieves set of currently visible tiles of game object on specified position

        :param position: Position of queried game object
        :return: Set of currently visible tiles
                 None if there is no unit at the position,
                 None if you don't see target position
        """
        return self.__get_visible_tiles(position)


    def get_visible_enemies(self, position: "Position") -> Optional[Dict["Position", int]]:
        """
        Retrieves map of distances to currently visible enemies by game object on specified position

        :param position: Position of queried game object
        :return: Dictionary of visible position with enemy as a Kye and distance as a value
                 Return None if there is no unit at the position,
                 None if you don't see target position
        """
        return self.__get_visible_enemies(position)


    def get_income(self, player: "PlayerTag") -> int:
        """
        Retrieves income of given player

        :param player: Player whose income should be obtained
        :return: Current income of given player
                 None if player not registered
        """
        return self.__get_income(player)


    def get_resources(self, player: "PlayerTag") -> int:
        """
        Retrieves current resources of given player

        :param player: Player whose resources should be obtained
        :return: Current resources of given player
                 None if player not registered
        """
        return self.__get_resources(player)


    def get_current_round(self) -> int:
        """

        :return:
        """
        return self.__get_current_round()


class GameControlProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.__spawn_unit = game_engine.spawn_unit
        del game_engine


    def spawn_unit(self, information: "SpawnInformation") -> None:
        """
        Attempts to spawn unit based on given spawn information

        :param information: Information bundle describing spawned unit
        :raise: IllegalActionException if invalid spawn attempt
        """
        return self.__spawn_unit(information)


class GameUncertaintyProxy:
    def __init__(self, game_engine: "GameEngine"):
        self.__spawn_information = game_engine.spawn_information
        del game_engine


    def spawn_information(self) -> List[List["UncertaintySpawn"]]:
        """
        | Get spawn information from uncertainty module.
        | First level is rounds, where 0 is the nearest round
        | Second level is list of UncertaintySpawn classes

        :return: Spawn information from Uncertainty module
        """
        return self.__spawn_information()
