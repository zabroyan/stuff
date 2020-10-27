import os
from random import Random
from typing import TYPE_CHECKING, List, Dict

from OrodaelTurrim.Business.GameMap import BorderTiles, GameMap
from OrodaelTurrim.Business.Interface.Player import IAttacker
from OrodaelTurrim.Structure.GameObjects.GameObject import UncertaintySpawn, UncertaintyPosition
from OrodaelTurrim.config import Config

if TYPE_CHECKING:
    from OrodaelTurrim.Business.GameEngine import GameEngine


def scout_success_rate(number: float) -> int:
    """ Recompute success rate of scouts to positions range"""
    if number < 0 or number > 1:
        raise ValueError('Insert number between 0 and 1')

    if number <= 0.1:
        return 12
    elif number <= 0.3:
        return 10
    elif number <= 0.4:
        return 8
    elif number <= 0.5:
        return 7
    elif number <= 0.6:
        return 6
    elif number <= 0.7:
        return 5
    elif number <= 0.8:
        return 4
    elif number <= 0.95:
        return 2
    else:
        return 0


class SpawnUncertainty:
    """ Class that compute spawn uncertainty from spawn information provided by AI """


    def __init__(self, game_engine: "GameEngine"):
        self.__attackers = []  # type: List: IAttacker
        self.__spawn_uncertainty = {}  # type: Dict[int, List[UncertaintySpawn]]
        self.__game_engine = game_engine  # type: GameEngine
        self.__game_map = game_engine.get_game_map()  # type: GameMap
        self.__best_scout_uncertainty = {}  # type: Dict[int, float]
        self.__last_generated_turn = -1
        self.__scout_uncertainties = {}  # type: Dict[float]

        # Try to load SEED from config

        seed = Config.UNCERTAINTY_RANDOM_SEED
        if not seed:
            seed = int.from_bytes(os.urandom(50), 'big')
            Config.UNCERTAINTY_RANDOM_SEED = seed

        self.__random = Random(seed)


    def register_attacker(self, attacker: IAttacker) -> None:
        """ Register attacker to database """
        self.__attackers.append(attacker)


    def clear(self) -> None:
        """ Clear computed uncertainty """
        self.__spawn_uncertainty = {}
        self.__best_scout_uncertainty = {}
        self.__last_generated_turn = -1
        self.__scout_uncertainties = {}


    def __compute_uncertainty(self, _round: int) -> None:
        """ Compute uncertainty list for target round"""
        current_turn = self.__game_engine.get_game_history().current_turn

        for attacker in self.__attackers:
            spawns = attacker.spawn_information_list[_round - current_turn - 1]

            self.__spawn_uncertainty[_round] = []
            for spawn in spawns:
                scout_success = self.__scout_uncertainties[current_turn]
                scout_success_unit = self.__random.uniform(max(scout_success - 0.10, 0), min(scout_success + 0.10, 1))
                mistake_range = scout_success_rate(scout_success_unit)
                deviation = self.__random.randint(0, mistake_range)

                deviation_start = BorderTiles(self.__game_map).get_position(spawn.position, -deviation)
                positions_list = BorderTiles(self.__game_map).get_position_list(deviation_start, mistake_range + 1)

                # Uniform distribution
                uncertainty = 1 / (mistake_range + 1)  # Plus correct position
                spawn_list = [UncertaintyPosition(position, uncertainty) for position in positions_list]

                self.__spawn_uncertainty[_round].append(UncertaintySpawn(spawn.object_type, spawn_list))


    @property
    def spawn_information(self) -> List[List[UncertaintySpawn]]:
        """ Get spawn information with computed uncertainty """
        current_turn = self.__game_engine.get_game_history().current_turn

        if self.__last_generated_turn != current_turn:
            self.__scout_uncertainties[current_turn] = self.__random.uniform(0.0, 1.0)
            for _round in range(1, 4):
                if _round + current_turn not in self.__spawn_uncertainty:
                    self.__compute_uncertainty(current_turn + _round)
                    self.__best_scout_uncertainty[current_turn + _round] = self.__scout_uncertainties[current_turn]
                elif self.__scout_uncertainties[current_turn] > self.__best_scout_uncertainty[current_turn + _round]:
                    self.__compute_uncertainty(current_turn + _round)
                    self.__best_scout_uncertainty[current_turn + _round] = self.__scout_uncertainties[current_turn]

            self.__last_generated_turn = current_turn
        return [self.__spawn_uncertainty[x] for x in range(current_turn + 1, current_turn + 4)]
