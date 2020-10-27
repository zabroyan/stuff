from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Dict, Set, Union

from OrodaelTurrim.Structure.Enums import AttributeType, GameObjectType, EffectType, GameRole
from OrodaelTurrim.Structure.Filter.FilterPattern import TileFilter, MoveFilter, AttackFilter
from OrodaelTurrim.Structure.GameObjects.Effect import Effect
from OrodaelTurrim.Structure.GameObjects.Prototypes.Prototype import GameObjectPrototypePool, GameObjectPrototype
from OrodaelTurrim.Structure.Position import Position

if TYPE_CHECKING:
    from OrodaelTurrim.Business.Interface.Player import IPlayer, PlayerTag
    from OrodaelTurrim.Business.GameEngine import GameEngine


class GameObject:
    """ Interface defining common behavior of game objects (attackers and defenders) """


    def __init__(self, owner: "IPlayer", position: Position, object_type: GameObjectType, game_engine: "GameEngine"):
        self.__owner = owner
        self.__game_engine = game_engine

        self.__object_type = object_type

        self.__prototype = GameObjectPrototypePool.prototypes[object_type]  # type: GameObjectPrototype
        self.__accessible_tiles = []  # type: List[Position]

        self.__move_filters = []  # type: List[MoveFilter]
        self.__attack_filters = []  # type: List[AttackFilter]

        self.__active_effects = set()  # type: Set[Effect]

        self.__visible_enemies = {}  # type: Dict[Position, int]
        self.__current_hit_points = self.__prototype.get_attribute_value(AttributeType.HIT_POINTS)

        self.__visible_tiles = set()  # type: Set[Position]
        self.__accessible_tiles = set()  # type: Set[Position]

        self.__position = None
        self.position = position


    def move(self) -> None:
        """
        Moves this game object based on its filter strategy
        """
        if self.get_attribute(AttributeType.ACTIONS) == 0 or self.__prototype.get_attribute_value(
                AttributeType.ACTIONS) == 0:
            return

        free_accessible_tiles = [x for x in self.__accessible_tiles if
                                 self.__game_engine.is_position_occupied(x) is False]

        if free_accessible_tiles:
            self.__game_engine.create_move_action(self, TileFilter.use_filter(self.position, self.__move_filters,
                                                                              free_accessible_tiles))


    def attack(self) -> None:
        """
        Attacks nearby game object based on its filter strategy
        """
        if self.enemies_in_range:
            self.__game_engine.create_attack_action(self, TileFilter.use_filter(self.position, self.__attack_filters,
                                                                                self.enemies_in_range))


    def recalculate_cache(self) -> None:
        """
        Recalculates cached values of visible and accessible tiles
        """
        self.__visible_tiles = self.__game_engine.compute_visible_tiles(self.position,
                                                                        int(self.get_attribute(AttributeType.SIGHT)))

        self.__accessible_tiles = set(self.__game_engine.compute_accessible_tiles(self.position, int(
            self.get_attribute(AttributeType.ACTIONS))).keys())


    @property
    def enemies_in_range(self) -> List[Position]:
        """
        Retrieves tiles with enemies in range of this game object

        :return: Tiles with enemies in range of this game object
        """
        attack_range = int(self.get_attribute(AttributeType.ATTACK_RANGE))
        return [position for position, distance in self.__visible_enemies.items() if distance <= attack_range]


    def act(self):
        """ Commands this game object to perform its actions """
        self.move()
        self.attack()


    def take_damage(self, damage: float) -> None:
        """
        Subtracts given amount of hit points from current hit points of this game object

        :param damage: Final amount of damage to receive
        """
        self.__current_hit_points -= damage


    def receive_healing(self, healing: float) -> None:
        """
        Adds given amount of hit points to current hit points of this game object

        :param healing: Final amount of healing to receive
        """
        self.__current_hit_points = min(self.__current_hit_points + healing,
                                        self.__prototype.get_attribute_value(AttributeType.HIT_POINTS))


    def apply_effect(self, effect: Effect) -> None:
        """
        Attempts to apply given effect onto this game object

        :param effect: Effect to be applied (unless resistance is active)
        """
        previous_sight = self.get_attribute(AttributeType.SIGHT)
        self.__active_effects.add(effect)

        if previous_sight != self.get_attribute(AttributeType.SIGHT):
            self.recalculate_cache()


    def remove_effect(self, effect_type: EffectType) -> None:
        """
        Removes currently active effect of given type

        :param effect_type: Type of effect to be removed
        """
        previous_sight = self.get_attribute(AttributeType.SIGHT)
        self.__active_effects = set([x for x in self.__active_effects if x.effect_type != effect_type])

        if previous_sight != self.get_attribute(AttributeType.SIGHT):
            self.recalculate_cache()


    def on_enemy_appear(self, position: Position) -> None:
        """
        Callback function which should be called when enemy appears in vision of this game object

        :param position: Position which enemy disappeared
        """
        self.__visible_enemies[position] = self.position.distance_from(position)


    def on_enemy_disappear(self, position: Position) -> None:
        """
        Callback function which should be called when enemy leaves the vision of this game object

        :param position: Position which enemy disappeared
        """
        try:
            self.__visible_enemies.pop(position)
        except KeyError:
            pass


    def register_attack_filter(self, attack_filter: AttackFilter) -> None:
        """
         Registers specified attack filter (as least significant)

        :param attack_filter: Filter to be registered
        """
        self.__attack_filters.append(attack_filter)


    def register_move_filter(self, move_filter: MoveFilter) -> None:
        """
        Registers specified move filter (as least significant)

        :param move_filter: Filter to be registered
        """
        self.__move_filters.append(move_filter)


    def is_dead(self) -> bool:
        """
        Checks whether this game object perished or not

        :return: True in case the game object is dead, false otherwise
        """
        return self.__current_hit_points <= 0


    def get_attribute(self, attribute_type: AttributeType) -> Union[int, float]:
        """
        Retrieves value of specified attribute

        :param attribute_type: Type of attribute to be retrieved
        :return: Value of specified attribute
        """
        return self.__game_engine.compute_attribute(self, attribute_type,
                                                    self.__prototype.get_attribute_value(attribute_type))


    @property
    def current_hit_points(self) -> float:
        """
        Retrieves amount of currently remaining hit points of this game object

        :return: Amount of currently remaining hit points
        """
        return self.__current_hit_points


    @property
    def object_type(self):
        """
        Retrieves the type of this game object

        :return: Type of this game object
        """
        return self.__object_type


    @property
    def role(self) -> GameRole:
        """
        Retrieves the role of this game object

        :return: Role of this game object
        """
        return self.__prototype.role


    @property
    def owner(self) -> "IPlayer":
        """
        Retrieves reference to player, who owns this game object

        :return: Reference to owner player
        """
        return self.__owner


    @property
    def position(self):
        """
        Retrieves current position of this game object

        :return: Current position of this game object
        """
        return self.__position


    @position.setter
    def position(self, value: Position):
        self.__position = value
        self.recalculate_cache()


    @property
    def attack_effects(self) -> Set[EffectType]:
        """
        Retrieves the types of effect to be applied to the target of attack of this object

        :return: Set of types of effect to be applied upon attacking
        """
        return self.__prototype.attack_effects


    @property
    def resistances(self) -> Set[EffectType]:
        """
        Retrieves the types of effect which will NOT affect this game object

        :return: Set of resistances
        """
        return self.__prototype.resistances


    @property
    def active_effects(self) -> Set[Effect]:
        """
        Retrieves currently active effects on this game object

        :return: Set of currently active effects
        """
        return self.__active_effects


    @property
    def visible_tiles(self) -> Set[Position]:
        """
        Retrieves set of currently visible tiles of this game object

        :return: Set of currently visible tiles
        """
        return self.__visible_tiles


    @property
    def accessible_tiles(self) -> Set[Position]:
        """ Get set of accessible tiles """
        return self.__accessible_tiles


    @property
    def visible_enemies(self) -> Dict[Position, int]:
        """
        Retrieves map of distances to currently visible enemies by this game object

        :return: Map of distances to currently visible enemies
        """
        return self.__visible_enemies


    @property
    def description(self) -> str:
        """ Return text attributes information """
        return self.__prototype.description.format(self.__current_hit_points)


    @property
    def move_filters(self) -> List[MoveFilter]:
        """ Get Set of the active MoveFilters """
        return self.__move_filters


    @property
    def attack_filters(self) -> List[AttackFilter]:
        """ Get Set of the active MoveFilters """
        return self.__attack_filters


class SpawnInformation:
    """ Holds all necessary information for spawning unit """


    def __init__(self, owner: Union["IPlayer", "PlayerTag"], object_type: GameObjectType, position: Position,
                 attack_filters: List[TileFilter], move_filters: List[TileFilter]):
        """
        :param owner: Owning player of spawned object
        :param object_type: Type of spawned object
        :param position: Initial position of spawned object
        :param attack_filters: List of attack filters to be applied ot spawned game object
        :param move_filters: List of move filters to be applied ot spawned game object
        """
        self.owner = owner
        self.object_type = object_type
        self.position = position
        self.attack_filters = attack_filters
        self.move_filters = move_filters


@dataclass(frozen=True)
class UncertaintyPosition(object):
    """ Information about position with uncertainty """
    position: Position
    uncertainty: float


class UncertaintySpawn:
    def __init__(self, game_object_type: GameObjectType, positions: List[UncertaintyPosition]):
        self.positions = positions
        self.game_object_type = game_object_type
