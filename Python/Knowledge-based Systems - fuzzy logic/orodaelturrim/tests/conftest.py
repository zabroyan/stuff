from typing import List
from flexmock import flexmock
import pytest
from antlr4 import InputStream

from ExpertSystem.Business.Parser.KnowledgeBase.RulesLexer import RulesLexer, CommonTokenStream, ParseTreeWalker
from ExpertSystem.Business.Parser.KnowledgeBase.RulesListenerImplementation import RulesListenerImplementation
from ExpertSystem.Business.Parser.KnowledgeBase.RulesParser import RulesParser
from OrodaelTurrim.Business.GameMap import GameMap
from OrodaelTurrim.Business.Uncertainty import SpawnUncertainty
from OrodaelTurrim.Structure.Map import VisibilityMap
from OrodaelTurrim.Structure.Position import Position
from ArtificialIntelligence.Main import AIPlayer
from ExpertSystem.Business.Player import Player
from OrodaelTurrim.Business.GameEngine import GameEngine
from OrodaelTurrim.Business.MapGenerator import MapGenerator
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
from OrodaelTurrim.Structure.Enums import TerrainType, GameObjectType
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition
from OrodaelTurrim.Structure.Resources import PlayerResources
from OrodaelTurrim.config import Config


@pytest.fixture
def game_map() -> GameMap:
    tiles = [
        [TerrainType.RIVER, TerrainType.FIELD, TerrainType.FIELD, TerrainType.FOREST, TerrainType.VILLAGE],
        [TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN],
        [TerrainType.FOREST, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.FIELD, TerrainType.RIVER],
        [TerrainType.VILLAGE, TerrainType.MOUNTAIN, TerrainType.HILL, TerrainType.HILL, TerrainType.HILL],
        [TerrainType.RIVER, TerrainType.FIELD, TerrainType.FOREST, TerrainType.FIELD, TerrainType.FOREST],
    ]

    return GameMap(5, 5, tiles)


@pytest.fixture
def utils():
    return Utils()


class Utils:
    def compare_position_list(self, list1: List[Position], list2: List[Position]) -> bool:
        list1 = [x.offset for x in list1]
        list2 = [x.offset for x in list2]
        list1.sort()
        list2.sort()

        return len(set(list1) - set(list2)) == 0 and len(set(list2) - set(list1)) == 0


    def parse_antlr_grammar(self, rule: str):
        input_file = InputStream(rule)

        lexer = RulesLexer(input_file)
        stream = CommonTokenStream(lexer)
        parser = RulesParser(stream)
        tree = parser.rules_set()

        rules_listener = RulesListenerImplementation()
        walker = ParseTreeWalker()
        walker.walk(rules_listener, tree)

        return rules_listener.rules


GAME_MAP = [
    [TerrainType.FIELD, TerrainType.FIELD, TerrainType.FIELD, TerrainType.FOREST, TerrainType.VILLAGE],
    [TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.MOUNTAIN],
    [TerrainType.FOREST, TerrainType.MOUNTAIN, TerrainType.FIELD, TerrainType.RIVER, TerrainType.RIVER],
    [TerrainType.VILLAGE, TerrainType.MOUNTAIN, TerrainType.HILL, TerrainType.RIVER, TerrainType.HILL],
    [TerrainType.FIELD, TerrainType.FIELD, TerrainType.FOREST, TerrainType.RIVER, TerrainType.FOREST],
]


def fake_init(cls, game_map):
    cls.__game_map = game_map
    cls.__players = []
    cls.__player_resources = {}
    cls.__player_units = {}
    cls.__defender_bases = {}
    cls.__game_object_positions = {}
    cls.__initial_resources = {}
    cls.__visibility_map = VisibilityMap()
    cls.__spawn_uncertainty = SpawnUncertainty(cls)


@pytest.fixture(scope='package')
def game_instance():
    game_map = MapGenerator(5, 5).generate(GAME_MAP)

    # Initialize game engine
    game_engine = GameEngine(game_map)

    map_proxy = MapProxy(game_engine)
    game_object_proxy = GameObjectProxy(game_engine)
    game_control_proxy = GameControlProxy(game_engine)
    game_uncertainty_proxy = GameUncertaintyProxy(game_engine)

    # Register defender
    defender = Player(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)
    game_engine.register_player(defender, PlayerResources(1000, 10), [])

    # Register attacker
    attacker = AIPlayer(map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy)
    game_engine.register_player(attacker, PlayerResources(200, 0, 0), [])

    game_engine.start(500)

    game_engine.spawn_unit(SpawnInformation(defender, GameObjectType.BASE, OffsetPosition(0, 0), [], []))
    game_engine.spawn_unit(SpawnInformation(attacker, GameObjectType.DEMON, OffsetPosition(0, -2), [], []))
    game_engine.spawn_unit(SpawnInformation(attacker, GameObjectType.DEMON, OffsetPosition(-1, -1), [], []))

    attacker.initialize()

    return map_proxy, game_object_proxy, game_control_proxy, game_uncertainty_proxy, defender, attacker, game_engine


@pytest.fixture()
def defender(game_instance):
    return game_instance[4]


@pytest.fixture()
def attacker(game_instance):
    return game_instance[5]
