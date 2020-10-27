import copy
from typing import List, Dict, Set, Optional, Union

from OrodaelTurrim.Business.Factory import EffectFactory
from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Business.History import GameHistory
from OrodaelTurrim.Business.Interface.Player import IPlayer, PlayerTag
from OrodaelTurrim.Business.Uncertainty import SpawnUncertainty
from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Structure.Actions.Abstract import GameAction
from OrodaelTurrim.Structure.Actions.Combat import MoveAction, AttackAction
from OrodaelTurrim.Structure.Actions.Effect import EffectRefreshAction, EffectApplyAction, EffectTickAction, \
    EffectDamageAction, EffectExpireAction
from OrodaelTurrim.Structure.Actions.Log import LogAction
from OrodaelTurrim.Structure.Actions.Placement import DieAction, SpawnAction
from OrodaelTurrim.Structure.Actions.Resources import EarnResourcesAction, SpendResourcesAction, IncomeResourcesIncrease
from OrodaelTurrim.Structure.Actions.Terrain import TerrainDamageAction
from OrodaelTurrim.Structure.Enums import AttributeType, GameObjectType, TerrainType, EffectType, GameRole
from OrodaelTurrim.Structure.Exceptions import IllegalActionException
from OrodaelTurrim.Structure.GameObjects.Effect import Effect
from OrodaelTurrim.Structure.GameObjects.GameObject import GameObject, SpawnInformation, UncertaintySpawn
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototypePool
from OrodaelTurrim.Structure.Map import VisibilityMap
from OrodaelTurrim.Structure.Position import Position
from OrodaelTurrim.Structure.Resources import PlayerResources


class GameEngine:
    """
    Main class of game module. Holds all parts of the game and provides most of the communication
    means in between them. Also serves as gateway for players to interact with the game

    Attributes:
        __game_map: Instance of the game map
        __players: List of registered players
        __player_resources: Dictionary with resources for each player
        __player_units: Dict with List of GameObjects for each player
        __defender_bases: Dict with one GameObject representing defender players bases
        __game_object_positions: Dictionary of GameObject positions
        __game_history: Instance of GameHistory
        __turn_limit: Limit of the rounds
        __initial_resources: Copy of player_resources on the start of game for restart the game
        __visibility_map: Instance of visibility map
        __spawn_uncertainty Instance of SpawnUncertainty class
    """

    __game_map: GameMap
    __players: List[IPlayer]
    __player_resources: Dict[Union[IPlayer, PlayerTag], PlayerResources]
    __player_units: Dict[IPlayer, List[GameObject]]

    __defender_bases: Dict[IPlayer, GameObject]
    __game_object_positions: Dict[Position, GameObject]

    __game_history: GameHistory
    __turn_limit: int

    __initial_resources: Dict[IPlayer, PlayerResources]
    __visibility_map: VisibilityMap
    __spawn_uncertainty: SpawnUncertainty


    def __init__(self, game_map: GameMap):
        GameEngine.__new__ = lambda x: print('Cannot create GameEngine instance')

        self.__game_map = game_map
        self.__players = []
        self.__player_resources = {}
        self.__player_units = {}
        self.__defender_bases = {}
        self.__game_object_positions = {}
        self.__initial_resources = {}
        self.__visibility_map = VisibilityMap()
        self.__spawn_uncertainty = SpawnUncertainty(self)


    def start(self, turn_limit: int) -> None:
        """
        Switches to the game execution state

        :param turn_limit: Maximum game rounds
        """
        self.__turn_limit = turn_limit
        self.__game_history = GameHistory(turn_limit, self.__players)


    def restart(self):
        """
        Restart GameEngine to starting state
        """
        self.__game_history = GameHistory(self.__turn_limit + self.__game_history.turns_count, self.__players)
        self.__player_resources = {key: value for key, value in self.__initial_resources.items()}

        for player in self.__player_units.keys():
            self.__player_units[player] = []
        self.__defender_bases = {}
        self.__game_object_positions = {}

        self.__visibility_map.clear()

        self.__spawn_uncertainty.clear()


    def register_player(self, player: IPlayer, resources: PlayerResources,
                        unit_spawn_info: List[SpawnInformation]) -> None:
        """
        Registers player to the game

        Note that order which players are registered in determines the order which they will play

        :param player: Player to be registered
        :param resources: Resources associated with registered player
        :param unit_spawn_info: Units associated with registered player
        """
        self.__players.append(player)
        self.__player_resources[player] = resources
        self.__player_units[player] = []

        self.__initial_resources[player] = copy.deepcopy(resources)

        self.__visibility_map.register_player(player)

        if player.role == GameRole.ATTACKER:
            self.__spawn_uncertainty.register_attacker(player)

        for spawn_information in unit_spawn_info:
            game_object = GameObject(spawn_information.owner, spawn_information.position, spawn_information.object_type,
                                     self)
            self.register_game_object(game_object)


    def register_game_object(self, game_object: GameObject) -> None:
        """
        Ensures proper registration of given game object to all structures

        :param game_object: Game object to be registered
        """
        owner = game_object.owner
        if game_object.object_type == GameObjectType.BASE:
            if owner in self.__defender_bases:
                raise IllegalActionException('Players are not allowed to spawn multiple bases!')
            else:
                self.__defender_bases[owner] = game_object

        self.__player_units[owner].append(game_object)
        self.__game_object_positions[game_object.position] = game_object

        self.__visibility_map.add_vision(game_object, game_object.visible_tiles)

        self.handle_self_vision_gain(game_object, set(), game_object.visible_tiles)
        self.handle_enemy_vision_gain(game_object, game_object.position)


    def delete_game_object(self, game_object: GameObject) -> None:
        """
        Ensures proper deletion of all references to given game object

        :param game_object: Game object to be deleted
        """
        self.__player_units[game_object.owner].remove(game_object)
        self.__game_object_positions.pop(game_object.position)

        self.__visibility_map.remove_vision(game_object, game_object.visible_tiles)

        self.handle_self_vision_loss(game_object, game_object.visible_tiles, set())
        self.handle_enemy_vision_loss(game_object, game_object.position)


    def create_unit(self, spawn_information: SpawnInformation) -> GameObject:
        """
        Creates a unit of given type

        :param spawn_information: Information about created unit
        :return: Created unit of given type
        """
        unit = GameObject(spawn_information.owner, copy.deepcopy(spawn_information.position),
                          spawn_information.object_type, self)

        for attack_filter in spawn_information.attack_filters:
            unit.register_attack_filter(attack_filter)

        for move_filter in spawn_information.move_filters:
            unit.register_move_filter(move_filter)

        return unit


    def handle_enemy_vision_gain(self, game_object: GameObject, position: Position) -> None:
        """
        Handles gain of vision for the enemies given game object

        :param game_object: Game object which enemies should be alerted
        :param position: Position enemies can newly see given game object
        """
        new_watchers = self.__visibility_map.get_watching_enemies(game_object.role, position)
        for watcher in new_watchers:
            watcher.on_enemy_appear(position)


    def handle_enemy_vision_loss(self, game_object: GameObject, position: Position) -> None:
        """
        Handles loss of vision for the enemies given game object

        :param game_object: Game object which enemies should be alerted
        :param position: Position enemies can no longer see given game object
        """
        old_watchers = self.__visibility_map.get_watching_enemies(game_object.role, position)
        for watcher in old_watchers:
            watcher.on_enemy_disappear(position)


    def handle_self_vision_gain(self, game_object: GameObject, old_vision: Set[Position],
                                new_vision: Set[Position]) -> None:
        """
        Handles the gain of vision for given game object

        :param game_object: Game object which gained vision
        :param old_vision: Set of visible positions from position before action
        :param new_vision: Set of visible positions from position after action
        """

        gain_vision = copy.deepcopy(new_vision)
        gain_vision.difference_update(old_vision)

        for position in gain_vision:
            if self.is_position_occupied(position) and game_object.role.is_enemy(
                    self.__game_object_positions[position].role):
                game_object.on_enemy_appear(position)


    def handle_self_vision_loss(self, game_object: GameObject, old_vision: Set[Position],
                                new_vision: Set[Position]) -> None:
        """
        Handles the loss of vision for given game object

        :param game_object: Game object which lost vision
        :param old_vision: Set of visible positions from position before action
        :param new_vision: Set of visible positions from position after action
        """

        lost_vision = copy.deepcopy(old_vision)
        lost_vision.difference_update(new_vision)
        for position in lost_vision:
            game_object.on_enemy_disappear(position)


    def handle_effect_attack(self, game_object: GameObject, effect_type: EffectType) -> None:
        """
        Apply target effect type to to target game object. Affect unit with new or refresh duration

        :param game_object: instance of target game object
        :param effect_type:  effect type to be apply
        """
        effect = EffectFactory.create(effect_type)

        if effect is None:
            return

        for active_effect in game_object.active_effects:
            if active_effect.effect_type == effect.effect_type:
                self.execute_action(EffectRefreshAction(self, active_effect, game_object))
                break
        else:
            self.execute_action(EffectApplyAction(self, effect, game_object))


    def handle_sight_affection(self, game_object: GameObject, old_sight: float, old_visibility: Set[Position]) -> None:
        """
        Handle state when unit lose some vision or get new vision

        :param game_object: target game object
        :param old_sight: old visibility (sight_number)
        :param old_visibility: new visibility (sight number)
        """
        if old_sight == game_object.get_attribute(AttributeType.SIGHT):
            return

        new_visibility = game_object.visible_tiles

        # Update visibility map
        vision_lost = old_visibility - new_visibility
        vision_gain = new_visibility - old_visibility
        self.__visibility_map.remove_vision(game_object, vision_lost)
        self.__visibility_map.add_vision(game_object, vision_gain)

        self.handle_self_vision_loss(game_object, old_visibility, new_visibility)
        self.handle_self_vision_gain(game_object, old_visibility, new_visibility)


    def execute_action(self, action: GameAction) -> None:
        """
        Executes and saves given game action to history

        :param action: Action to be executed and registered
        """
        if self.__game_history.in_preset:
            self.__game_history.add_action(action)
        action.execute()


    def execute_terrain_turn(self, game_object: GameObject) -> None:
        """
        Executes the actions towards given game object from the tile it's standing on

        :param game_object: Game object which tile's actions should be executed
        """
        terrain = self.__game_map[game_object.position]
        potential_damage = terrain.compute_damage(game_object.current_hit_points)

        if potential_damage != 0:
            self.execute_action(TerrainDamageAction(self, game_object, terrain.terrain_type, potential_damage))


    def execute_effect_turn(self, effect: Effect, owner: GameObject) -> None:
        """
        Executes the actions given effect will make in one turn

        :param effect: Effect which turn should be executed
        :param owner: Game object given effect is attached to
        """
        self.execute_action(EffectTickAction(self, effect, owner))

        potential_damage = effect.compute_damage(owner.current_hit_points)
        if potential_damage != 0:
            self.execute_action(EffectDamageAction(self, effect, owner, potential_damage))

        if effect.hax_expired:
            self.execute_action(EffectExpireAction(self, effect, owner))


    def execute_unit_turn(self, unit: GameObject) -> None:
        """
        Executes the actions given unit would make in one turn

        :param unit: Unit which turn should be executed
        """
        self.execute_terrain_turn(unit)

        effects = unit.active_effects
        for effect in effects:
            self.execute_effect_turn(effect, unit)

        if not unit.is_dead():
            unit.act()


    def simulate_rest_of_player_turn(self, player) -> None:
        """
        Simulates rest of turn for given player

        :param player: Player to simulate rest of turn for
        """
        units = self.__player_units[player]

        for unit in units:
            if Connector().get_variable('game_over'):
                return
            self.execute_unit_turn(unit)

        income = self.__player_resources[player].income
        self.execute_action(EarnResourcesAction(self, player, income))

        income_increase = self.__player_resources[player].income_increase
        if income_increase > 0:
            self.execute_action(IncomeResourcesIncrease(self, player, income_increase))

        # Check base
        if player.role == GameRole.DEFENDER and self.__game_history.in_preset and not self.player_have_base(player):
            Connector().emit('game_over')
            Connector().set_variable('game_over', True)
            return

        self.__game_history.end_turn()


    def damage(self, game_object: GameObject, damage: float) -> None:
        """
        Applies specified amount of damage to given game object

        :param game_object: Game object to be damaged
        :param damage: Amount of damage to be applied
        """
        game_object.take_damage(damage)
        if game_object.is_dead() and self.get_game_history().in_preset:
            self.execute_action(DieAction(self, game_object))


    def heal(self, game_object: GameObject, amount: float) -> None:
        """
        Restores specified amount of hit points of given game object

        :param game_object: Game object to be healed
        :param amount: Amount of hit points to be restored
        """
        game_object.receive_healing(amount)


    def move(self, game_object: GameObject, to: Position) -> None:
        """
        Moves given game object to specified position

        :param game_object: Game object to be moved
        :param to: Position to move game object to
        """
        position_from = game_object.position

        del self.__game_object_positions[position_from]
        self.__game_object_positions[to] = game_object

        old_visibility = game_object.visible_tiles
        game_object.position = to
        new_visibility = game_object.visible_tiles

        # Update visibility map
        vision_lost = old_visibility - new_visibility
        vision_gain = new_visibility - old_visibility
        self.__visibility_map.remove_vision(game_object, vision_lost)
        self.__visibility_map.add_vision(game_object, vision_gain)

        self.handle_self_vision_loss(game_object, old_visibility, new_visibility)
        self.handle_self_vision_gain(game_object, old_visibility, new_visibility)

        self.handle_enemy_vision_loss(game_object, position_from)
        self.handle_enemy_vision_gain(game_object, to)


    def apply_effect(self, game_object: GameObject, effect: Effect) -> None:
        """
        Applies given effect to specified game object

        :param game_object: Game object to apply effect to
        :param effect: Effect to be applied
        """
        old_sight = game_object.get_attribute(AttributeType.SIGHT)
        old_visibility = game_object.visible_tiles

        game_object.apply_effect(effect)
        self.handle_sight_affection(game_object, old_sight, old_visibility)


    def remove_effect(self, game_object: GameObject, effect_type: EffectType) -> None:
        """
        Removes effect of given type from specified game object

        :param game_object: Game object to remove effect from
        :param effect_type: Type of effect to be removed
        """
        old_sight = game_object.get_attribute(AttributeType.SIGHT)
        old_visibility = game_object.visible_tiles

        game_object.remove_effect(effect_type)

        self.handle_sight_affection(game_object, old_sight, old_visibility)


    def remove(self, game_object: GameObject) -> None:
        """
        Removes given game object from the game

        :param game_object: Game object to be removed
        """
        if game_object.object_type == GameObjectType.BASE:
            for player, _game_object in self.__defender_bases.items():
                if game_object == _game_object:
                    del self.__defender_bases[player]

                    if self.__game_history.in_preset and not Connector().get_variable('game_over'):
                        Connector().set_variable('game_over', True)
                        Connector().emit('game_over')
                    break

        self.delete_game_object(game_object)


    def place(self, game_object: GameObject) -> None:
        """
        Places given game object into game under specified player's control

        :param game_object: Game object to be placed
        """
        self.register_game_object(game_object)


    def earn(self, player: IPlayer, amount: int) -> None:
        """
        Adds given amount of resources to specified player

        :param player: Player to give resources to
        :param amount: Amount of resources to give
        """
        self.__player_resources[player].add_resources(amount)


    def spend(self, player: IPlayer, amount: int) -> None:
        """
        Removes given amount of resources from specified player

        :param player:  Player to remove resources from
        :param amount: Amount of resources to remove
        :return:
        """
        self.__player_resources[player].remove_resources(amount)


    def create_move_action(self, game_object: GameObject, position: Position) -> None:
        """
        Create move action and execute it (Mmves specified game object to specified position)

        :param game_object: Game object to be moved
        :param position: Position to move game object to
        :return:
        """
        if game_object is not None and position is not None:
            self.execute_action(MoveAction(self, game_object, game_object.position, position))


    def create_attack_action(self, game_object: GameObject, position: Position) -> None:
        """
        Makes specified game object attack game object standing on given position

        :param game_object: Game object to perform the attack
        :param position: Position of game object which will be victim of the attack
        """
        if game_object is None or position is None or position not in self.__game_object_positions:
            return

        attacked = self.__game_object_positions[position]
        self.execute_action(AttackAction(self, game_object, attacked))

        attack_effects = copy.deepcopy(game_object.attack_effects)
        attack_effects.difference_update(attacked.resistances)

        for effect_type in attack_effects:
            self.handle_effect_attack(attacked, effect_type)


    def create_log_action(self, message: str) -> None:
        """
        Create user custom log action. Message appear in game history

        :param message: String message to log
        """
        if type(message) is not str:
            return

        self.execute_action(LogAction(self, message))


    def compute_attribute(self, game_object: GameObject, attribute_type: AttributeType, original_value: float) -> float:
        """
        Computes current influenced value of attribute of specified game object

        :param game_object: Game object which attribute's value should get computed
        :param attribute_type: Type of attribute which should get computed
        :param original_value: Original value of influenced attribute
        :return: Current influenced value of specified attribute
        """
        affected = self.__game_map[game_object.position].affect_attribute(attribute_type, original_value)

        for effect in game_object.active_effects:
            affected = effect.affect_attribute(attribute_type, affected)

        return affected


    def get_attribute(self, position: Position, attribute_type: AttributeType) -> Optional[float]:
        """
        Retrieves value of specified attribute of game object on specified position
        Returns None if there is no unit at the position

        :param position: Position of queried game object
        :param attribute_type: Type of attribute to be retrieved
        :return: Value of specified attribute
        """
        if position not in self.__game_object_positions:
            return None

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        return self.__game_object_positions[position].get_attribute(attribute_type)


    def get_current_hit_points(self, position: Position) -> Optional[float]:
        """
        Retrieves amount of currently remaining hit points of game object on specified position
        Returns None if there is no unit at the position or position is not visible

        :param position: Position of queried game object
        :return: Amount of currently remaining hit points
        """
        if position not in self.__game_object_positions:
            return None

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        return self.__game_object_positions[position].current_hit_points


    def get_attack_effect(self, position: Position) -> Optional[Set[EffectType]]:
        """
        Retrieves the types of effect to be applied to the target of attack of game object on specified position
        Returns None if there is no unit at the position

        :param position: Position of queried game object
        :return: Set of types of effect to be applied upon attacking
        """
        if position not in self.__game_object_positions:
            return None

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        return self.__game_object_positions[position].attack_effects


    def get_resistances(self, position: Position) -> Optional[Set[EffectType]]:
        """
        Retrieves the types of effect which will NOT affect game object on specified position
        Returns None if there is no unit at the position or player don't see that position

        :param position: Position of queried game object
        :return: Set of resistances of game object on specified position
        """
        if position not in self.__game_object_positions:
            return None

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        return self.__game_object_positions[position].resistances


    def get_active_effects(self, position: Position) -> Optional[Dict[EffectType, int]]:
        """
        Retrieves types of currently active effects and their durations on game object on specified position
        Returns None if there is no unit at the position or player don't see that position

        :param position: Position of queried game object
        :return: Dict of types of active effects and associated remaining durations
        """
        if position not in self.__game_object_positions:
            return None

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        active_effects = {}

        effects = self.__game_object_positions[position].active_effects
        for effect in effects:
            active_effects[effect.effect_type] = effect.remaining_duration

        return active_effects


    def get_object_type(self, position: Position) -> Optional[GameObjectType]:
        """
        Retrieves the type of game object on specified position
        Return GameObjectType.NONE if there is no unit at the position

        :param position: Position of queried game object
        :return: Type of game object on specified position,
                 GameObjectType.NONE if there is no unit at the position,
                 None if player don't see that position

        """
        if position not in self.__game_object_positions:
            return GameObjectType.NONE

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        return self.__game_object_positions[position].object_type


    def get_role(self, position: Position) -> Optional[GameRole]:
        """
        Retrieves the role of game object on specified position
        Return GameRole.NEUTRAL if there is no unit at the position


        :param position: Position of queried game object
        :return: Role of game object on specified position,
                 GameRole.NEUTRAL if there is no unit at the position,
                 None if player don't see that position
        """
        if position not in self.__game_object_positions:
            return GameRole.NEUTRAL

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        return self.__game_object_positions[position].role


    def get_visible_tiles(self, position: Position) -> Optional[Set[Position]]:
        """
        Retrieves set of currently visible tiles of game object on specified position
        Return None if there is no unit at the position

        :param position: Position of queried game object
        :return: Set of currently visible tiles
        """
        if position not in self.__game_object_positions:
            return None

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        return self.__game_object_positions[position].visible_tiles


    def get_visible_enemies(self, position: Position) -> Optional[Dict[Position, int]]:
        """
        Retrieves map of distances to currently visible enemies by game object on specified position
        Return None if there is no unit at the position
        Return None if player don't see target position

        :param position: Position of queried game object
        :return:
        """
        if position not in self.__game_object_positions:
            return None

        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None

        return self.__game_object_positions[position].visible_enemies


    def get_map_height(self) -> int:
        """ Retrieves number of tiles in each column of game map """
        return self.__game_map.size[1]


    def get_map_width(self) -> int:
        """ Retrieves number of tiles in each row of game map """
        return self.__game_map.size[0]


    def get_terrain_type(self, position: Position) -> Optional[TerrainType]:
        """
        Retrieves terrain type of given position
        Return None if Positions is not on map

        :param position: Position to get terrain type for
        :return: Terrain type of given position
        """
        if not self.is_position_on_map(position):
            return None

        return self.__game_map[position].terrain_type


    def is_position_on_map(self, position: Position) -> bool:
        """
        Checks whether given position is on map or not

        :param position: Position to be checked
        :return: True in case position is within map bounds, False otherwise
        """
        return self.__game_map.position_on_map(position)


    def is_position_occupied(self, position: Position) -> Optional[bool]:
        """
        Checks whether given position is occupied or not. You can check only visible positions

        :param position: Position to be checked
        :return: True in case there is game object on given position, False otherwise,
                 None if user did not see the position
        """
        if position not in self.__visibility_map.get_visible_tiles(self.__game_history.active_player):
            return None
        return position in self.__game_object_positions


    def get_bases_positions(self) -> Set[Position]:
        """
        Retrieves positions of defenders' bases

        :return: Positions of defenders' bases
        """
        return set([x.position for x in self.__defender_bases.values()])


    def get_border_tiles(self) -> Set[Position]:
        """ Retrieves set of tiles on the edge of game map """
        return self.__game_map.border_tiles


    def get_inner_tiles(self) -> Set[Position]:
        """ Retrieves set of tiles which are not on the map edge"""
        return self.__game_map.inner_tiles


    def get_player_visible_tiles(self, player: IPlayer) -> Optional[Set[Position]]:
        """
        Retrieves set of visible tiles for player.
        Return None if player is not registered in GameEngine

        :param player: Player to obtain vision for
        :return:  Set of visible tiles of specified player
        """
        if player not in self.__players:
            return None
        return self.__visibility_map.get_visible_tiles(player)


    def get_current_player_visible_tiles(self) -> Set[Position]:
        """
        Retrieves set of visible tiles for player.

        :return: Set of visible tiles of specified player
        """
        return self.get_player_visible_tiles(self.__game_history.active_player)


    def compute_visible_tiles(self, position: Position, sight: int) -> Optional[Set[Position]]:
        """
        Computes set of visible tiles in sight radius from given position.

        :param position: Position to use as base point of computation
        :param sight: Value of sight to consider for computation
        :return: Set of visible tiles of specified game object.
                 None if positions is not on map
        """
        if not self.is_position_on_map(position):
            return None
        return self.__game_map.get_visible_tiles(position, sight)


    def compute_accessible_tiles(self, position: Position, actions: int) -> Optional[Dict[Position, int]]:
        """
        Computes map with accessible tiles as keys and remaining action points as values from specified position
        and number of remaining action points

        :param position: Position to use as base point of computation
        :param actions: Number of action points to consider for computation
        :return: Dict with accessible tiles as keys and remaining action points as values
                 None if positions is not on map
        """
        if not self.is_position_on_map(position):
            return None
        return self.__game_map.get_accessible_tiles(position, actions)


    def spawn_unit(self, information: SpawnInformation) -> None:
        """
        Attempts to spawn unit based on given spawn information

        :param information: Information bundle describing spawned unit
        :raise: IllegalActionException
        """
        prototype = GameObjectPrototypePool[information.object_type]

        resources = self.__player_resources[information.owner].resources

        if information.object_type == GameObjectType.BASE and information.owner in self.__defender_bases:
            raise IllegalActionException('You cannot spawn additional base!')

        if resources < prototype.cost:
            raise IllegalActionException('Insufficient resources!')

        if not issubclass(type(information.position), Position):
            raise TypeError('Invalid parameter type information position!')

        if not self.is_position_on_map(information.position):
            raise IllegalActionException('Position is not on the map!')

        if information.owner.role == GameRole.DEFENDER:
            if information.position not in self.get_player_visible_tiles(
                    information.owner) and information.object_type != GameObjectType.BASE:
                raise IllegalActionException('Attempt to spawn unit at not visible tile!')

        if self.is_position_occupied(information.position):
            raise IllegalActionException('Tile is already occupied!')

        if self.__game_map.position_on_edge(information.position) and information.owner.role == GameRole.DEFENDER:
            raise IllegalActionException('Cannot spawn unit defender unit on the map edge.')

        if information.owner.role != prototype.role:
            raise IllegalActionException('Attempt to spawn unit of different role!')

        self.execute_action(SpendResourcesAction(self, information.owner, prototype.cost))
        self.execute_action(SpawnAction(self, self.create_unit(information)))


    def get_resources(self, player: Union[PlayerTag, IPlayer]) -> int:
        """
        Retrieves current resources of given player

        :param player: Player whose resources should be obtained
        :return: Current resources of given player
        """
        return self.__player_resources.get(player, None).resources


    def get_income(self, player: Union[IPlayer, PlayerTag]) -> int:
        """
        Retrieves income of given player

        :param player: Player whose income should be obtained
        :return: Current income of given player
        """
        return self.__player_resources.get(player, None).income


    def increase_income(self, player: IPlayer, amount: int):
        """
        Raise income of given player

        :param player: Player whose income should be increased
        :param amount:
        :return:
        """
        self.__player_resources[player].increase_income(amount)


    def get_current_round(self) -> int:
        """
        Get current round of the game
        """
        return self.get_game_history().current_turn


    def get_game_map(self) -> GameMap:
        """ Get game map instance """
        return self.__game_map


    def get_game_object(self, position: Position) -> Optional[GameObject]:
        """
        Get game object instance on target position

        :param position: Target position to check
        :return: Game object on target position
                 None if position not occupied or positions is not on map
        """
        if not self.is_position_on_map(position):
            return None
        if position not in self.__game_object_positions:
            return None
        return self.__game_object_positions[position]


    def get_player(self, player_index: int) -> IPlayer:
        """
        Get player by player index

        :param player_index: Target player index (from 0)
        :return: IPlayer instance
        """
        return self.__players[player_index]


    def get_game_history(self) -> GameHistory:
        """ Get instance of GameHistory """
        return self.__game_history


    def player_have_base(self, player: Union[PlayerTag, IPlayer]) -> bool:
        """
        Check if player already have a base

        :param player: Target player to be checked
        :return: True if player have base, False otherwise
        """
        return player in self.__defender_bases


    def spawn_information(self) -> List[List[UncertaintySpawn]]:
        """
        | Get spawn information from uncertainty module.
        | First level is rounds, where 0 is the nearest round
        | Second level is list of UncertaintySpawn classes

        :return: Spawn infromation from Uncertainty module
        """
        return self.__spawn_uncertainty.spawn_information


    def run_game_rounds(self, rounds: int) -> None:
        """
        Simulate N number of rounds in game engine

        :param rounds: Number of rounds to be simulated
        """
        game_history = self.get_game_history()
        while rounds > 0 and not Connector().get_variable('game_over'):
            game_history.active_player.act()
            self.simulate_rest_of_player_turn(game_history.active_player)

            if game_history.on_first_player:
                rounds -= 1
