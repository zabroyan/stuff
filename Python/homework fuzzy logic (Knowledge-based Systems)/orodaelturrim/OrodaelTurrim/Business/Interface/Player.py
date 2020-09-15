import os
from abc import ABC, abstractmethod
from random import Random
from typing import List, TYPE_CHECKING, Union

from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Structure.Enums import GameRole
from OrodaelTurrim.config import Config

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation


class PlayerTag:
    def __init__(self, player: "IPlayer"):
        self.hash = hash(player)
        self.name = player.name
        self.role = player.role
        del player


    def __hash__(self):
        return self.hash


class IPlayer(ABC):
    """
    Provides methods for accessing and/or notifying players
    """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, game_control_proxy: GameControlProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy):
        self.map_proxy = map_proxy
        self.game_object_proxy = game_object_proxy
        self.game_control_proxy = game_control_proxy
        self.game_uncertainty_proxy = game_uncertainty_proxy


    @abstractmethod
    def act(self) -> None:
        """
        Resolves a turn of player. This is the player's only opportunity to place units on map
        """
        pass


    @property
    @abstractmethod
    def role(self) -> GameRole:
        """
        Retrieves role of this player
        :return: Role of this player
        """
        pass


    @property
    @abstractmethod
    def name(self) -> str:
        """
        Retrieves name of this player, which should be displayed in UI
        """
        pass


    def __eq__(self, other: Union["IPlayer", "PlayerTag"]):
        return self.name == other.name and self.role == other.role


    def __hash__(self):
        return hash((self.name, self.role))


class IAttacker(IPlayer, ABC):
    """ Specialization Player for attacker. Attacker must provide list of spawn information and have own random seed """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy, game_control_proxy: GameControlProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy):
        super().__init__(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)

        # Load seed from config file
        seed = Config.AI_RANDOM_SEED
        if not seed:
            seed = int.from_bytes(os.urandom(50), 'big')
            Config.AI_RANDOM_SEED = seed

        self.spawn_random = Random(seed)


    @property
    def role(self) -> GameRole:
        return GameRole.ATTACKER


    @property
    @abstractmethod
    def spawn_information_list(self) -> List[List["SpawnInformation"]]:
        """
        Return list of of spawn information for next 3 rounds

        0 first round
            0 unit 1
            1 Unit 2
            ...

        1 second round
            0 unit 1
            1 Unit 2
            ...

        2 third round
            0 unit 1
            1 Unit 2
            ...

        """
        pass


    @abstractmethod
    def initialize(self):
        pass
