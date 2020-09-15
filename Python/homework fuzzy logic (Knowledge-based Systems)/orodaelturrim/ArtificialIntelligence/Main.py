from typing import List, Dict, Tuple, Optional

from OrodaelTurrim import AI_CONSOLE_OUTPUT
from OrodaelTurrim.Business.Interface.Player import IAttacker
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Structure.Enums import GameRole, GameObjectType
from OrodaelTurrim.Structure.Exceptions import IllegalActionException
from OrodaelTurrim.Structure.Filter.AttackFilter import AttackBaseFilter, AttackMostVulnerableFilter, \
    AttackNearestFilter, AttackNoResistantFilter, AttackStrongestFilter
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter, MoveFilter
from OrodaelTurrim.Structure.Filter.MoveFilter import MoveToNearestEnemyFilter, MoveToRangeFilter, MoveToBaseFilter, \
    MoveToSafeDistanceFilter
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation

BOSS_ROUNDS = 5
BOSS_UNITS = lambda turn: max(1, turn // 20)
BOSS_UNIT = GameObjectType.NECROMANCER


class AIPlayer(IAttacker):
    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, game_control_proxy: GameControlProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy):
        super().__init__(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)

        self.__spawn_information = None  # type : List[List[SpawnInformation]
        self.__resources_left = None
        self.__attackers = None
        self.__most_expensive_unit = None
        self.__cheapest_unit = None
        self.__border_tiles = None


    def act(self) -> None:

        self.__printer('Rigor Mortis doing his stuff')

        for spawn in self.spawn_information_list[0]:
            try:
                self.game_control_proxy.spawn_unit(spawn)
            except IllegalActionException:
                pass

        self.__update_spawn_list()


    @property
    def spawn_information_list(self) -> List[List[SpawnInformation]]:
        """
        Get information about spawns
        """
        return self.__spawn_information


    @property
    def name(self) -> str:
        return 'Rigor Mortis'


    def initialize(self):
        self.__spawn_information = [[] for _ in range(3)]  # type : List[List[SpawnInformation]

        # List of GameObject for attackers
        self.__attackers = GameObjectType.attackers()

        # Most expensive unit
        max_price = max([x.price for x in self.__attackers])
        self.__most_expensive_unit = [x for x in self.__attackers if x.price == max_price][0]

        # Cheapest unit
        min_price = min([x.price for x in self.__attackers if x.price != 0])
        self.__cheapest_unit = [x for x in self.__attackers if x.price == min_price][0]

        # Border tiles
        self.__border_tiles = self.map_proxy.get_border_tiles()

        self.__prepare_units_filters()

        self.__initialize_spawn_list()


    def __printer(self, text):
        if AI_CONSOLE_OUTPUT:
            print(text)


    def __prepare_units_filters(self):
        nearest_enemy = FilterFactory().move_filter(MoveToNearestEnemyFilter)
        to_range = FilterFactory().move_filter(MoveToRangeFilter)
        to_base = FilterFactory().move_filter(MoveToBaseFilter)
        safe_dist = FilterFactory().move_filter(MoveToSafeDistanceFilter)

        base = FilterFactory().attack_filter(AttackBaseFilter)
        vulnerable = FilterFactory().attack_filter(AttackMostVulnerableFilter)
        nearest = FilterFactory().attack_filter(AttackNearestFilter)
        no_resistance = FilterFactory().attack_filter(AttackNoResistantFilter)
        strongest = FilterFactory().attack_filter(AttackStrongestFilter)

        self.unit_filters = {
            GameObjectType.CYCLOPS: ([vulnerable], [nearest_enemy, to_base]),
            GameObjectType.DEMON: ([no_resistance, strongest], [to_range]),
            GameObjectType.ELEMENTAL: ([strongest, vulnerable], [safe_dist]),
            GameObjectType.GARGOYLE: ([base], [to_base]),
            GameObjectType.MINOTAUR: ([vulnerable], [nearest_enemy, to_base]),
            GameObjectType.NECROMANCER: ([], [safe_dist]),
            GameObjectType.ORC: ([nearest, base], [nearest_enemy, to_base]),
            GameObjectType.SKELETON: ([nearest, base], [nearest_enemy, to_base]),
        }  # type: Dict[GameObjectType,Tuple[List[AttackFilter], List[MoveFilter]]]


    def __initialize_spawn_list(self):
        resources = self.game_object_proxy.get_resources(self)
        income = self.game_object_proxy.get_income(self)

        for i, round_list in enumerate(self.spawn_information_list):
            # Generate list of spawn info for one round
            round_spawn, spend = self.__create_round_list(resources, i + 1)

            # Set list to the spawn info
            round_list.extend(round_spawn)

            # Update resources_left
            resources = resources - spend + income

        self.__resources_left = resources


    def __update_spawn_list(self):
        self.spawn_information_list.pop(0)
        current_round = self.game_object_proxy.get_current_round()

        _round, spend = self.__create_round_list(self.__resources_left,
                                                 len(self.spawn_information_list) + current_round + 2)

        self.spawn_information_list.append(_round)
        self.__resources_left = self.__resources_left + self.game_object_proxy.get_income(self) - spend


    def __create_round_list(self, resources: int, _round: int) -> Tuple[List[SpawnInformation], int]:
        result = []
        spend = 0
        current_resources = resources

        if _round % BOSS_ROUNDS == 0:
            for i in range(BOSS_UNITS(_round)):
                spawn_info = self.__create_spawn_info_boos()

                if spawn_info:
                    current_resources -= spawn_info.object_type.price
                    spend += spawn_info.object_type.price
                    result.append(spawn_info)

        else:
            while self.__spawn_unit(resources, current_resources):
                spawn_info = self.__create_spawn_info(current_resources, result)
                if spawn_info is None:
                    break
                current_resources -= spawn_info.object_type.price
                spend += spawn_info.object_type.price
                result.append(spawn_info)

        return result, spend


    def __create_spawn_info_boos(self):
        free_border_tiles = [tile for tile in self.__border_tiles if
                             self.game_object_proxy.get_object_type(tile) == GameObjectType.NONE]

        if not free_border_tiles:
            return None

        position = self.spawn_random.choice(tuple(free_border_tiles))
        return SpawnInformation(self, BOSS_UNIT, position, self.unit_filters[BOSS_UNIT][0],
                                self.unit_filters[BOSS_UNIT][1])


    def __create_spawn_info(self, resources: int, planned: List[SpawnInformation]) -> Optional[SpawnInformation]:
        attackers = [attacker for attacker in self.__attackers if attacker.price <= resources and attacker != BOSS_UNIT]
        game_object = self.spawn_random.choice(attackers)

        planned_positions = [x.position for x in planned]

        free_border_tiles = [tile for tile in self.__border_tiles if
                             self.game_object_proxy.get_object_type(
                                 tile) == GameObjectType.NONE and tile not in planned_positions]

        if not free_border_tiles:
            return None

        position = self.spawn_random.choice(tuple(free_border_tiles))
        return SpawnInformation(self, game_object, position, self.unit_filters[game_object][0],
                                self.unit_filters[game_object][1])


    def __spawn_unit(self, maximum_resources: int, remaining_resources: int) -> bool:
        """ Determinate if spawn new unit or not """

        if remaining_resources > self.__most_expensive_unit.price:
            return True

        if remaining_resources < self.__cheapest_unit.price:
            return False

        bound = maximum_resources / remaining_resources
        if bound > self.spawn_random.random():
            return True
        else:
            return False
