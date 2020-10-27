from random import randrange
from typing import List

from ExpertSystem.Business.UserFramework import IKnowledgeBase
from ExpertSystem.Structure.RuleBase import Fact
from OrodaelTurrim.Business.Interface.Player import PlayerTag
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameUncertaintyProxy
from OrodaelTurrim.Structure.Enums import TerrainType, GameObjectType, GameRole
from OrodaelTurrim.Structure.Position import OffsetPosition


class KnowledgeBase(IKnowledgeBase):
    """
    Class for defining known facts based on Proxy information. You can transform here any information from
    proxy to better format of Facts. Important is method `create_knowledge_base()`. Return value of this method
    will be passed to `Inference.interfere`. It is recommended to use Fact class but you can use another type.

    |
    |
    | Class provides attributes:

    - **map_proxy [MapProxy]** - Proxy for access to map information
    - **game_object_proxy [GameObjectProxy]** - Proxy for access to all game object information
    - **uncertainty_proxy [UncertaintyProxy]** - Proxy for access to all uncertainty information in game
    - **player [PlayerTag]** - class that serve as instance of user player for identification in proxy methods

    """
    map_proxy: MapProxy
    game_object_proxy: GameObjectProxy
    game_uncertainty_proxy: GameUncertaintyProxy
    player: PlayerTag
    no_knight = True
    lives = {
        "little": {'a': 0, 'b': 0, 'c': 75, 'd': 100},
        "enough": {'a': 75, 'b': 120, 'c':  200, 'd': 250},
        "alot": {'a': 250, 'b': 300, 'c':  500, 'd': 500}
    }

    enemy_distance = {
        "closest": {'a': 0, 'b': 0, 'c': 3.5, 'd': 4},
        "close": {'a': 3, 'b': 4, 'c': 5, 'd': 6},
        "medium": {'a': 5, 'b':  6, 'c': 7, 'd': 8},
        "far": {'a': 7, 'b':  8, 'c':  16, 'd':  16}
    }

    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy, player: PlayerTag):
        """
        You can add some code to __init__ function, but don't change the signature. You cannot initialize
        KnowledgeBase class manually so, it is make no sense to change signature.
        """
        super().__init__(map_proxy, game_object_proxy, game_uncertainty_proxy, player)

    def create_knowledge_base(self) -> List[Fact]:
        """
        Method for create user knowledge base. You can also have other class methods, but entry point must be this
        function. Don't change the signature of the method, you can change return value, but it is not recommended.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!  TODO: Write implementation of your knowledge base definition HERE   !!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """

        facts = []

        # Add bool fact
        if not self.map_proxy.player_have_base(self.player):
            facts.append(Fact('player_dont_have_base'))

        if self.no_knight:
            self.no_knight = False
            facts.append(Fact('no_knight'))

        # Add fact with data holder
        # We can use there eval function same as data function
        # because if first_free_tile return None, bool value of None is False, otherwise bool value is True
        # You can use different functions for eval and data

        facts.append(Fact('free_tile', eval_function=self.first_free_tile, data=self.first_free_tile))
        facts.append(
            Fact('free_tile_around_king', eval_function=self.free_tile_around_king, data=self.free_tile_around_king))
        facts.append(
            Fact('baseIsNotSurrounded', eval_function=self.baseIsNotSurrounded, data=self.baseIsNotSurrounded))
        facts.append(Fact('tile', eval_function=self.free_tiles, data=self.free_tiles))

        # Add numerical fact
        facts.append(Fact("money", lambda: self.game_object_proxy.get_resources(self.player)))

        facts.append(Fact("lives", lambda x: self.lives_count(x)))
        facts.append(Fact("enemy_distance", lambda x: self.enemy_distance_count(x)))

        return facts

    def get_f (self, fuzzy, number):
        results = dict()
        for x in fuzzy:
            a = fuzzy[x]['a']
            b = fuzzy[x]['b']
            c = fuzzy[x]['c']
            d = fuzzy[x]['d']
            if c == d:
                if number <= a:
                    results.update({x: 0})
                elif number >= b:
                    results.update({x: 1})
                else:
                    results.update({x: (number - a) / (b - a)})
            elif a == b:
                if number <= c:
                    results.update({x: 1})
                elif number >= d:
                    results.update({x: 0})
                else:
                    results.update({x: (d - number) / (d - c)})
            else:
                results.update({x: max(min((number - a) / (b - a), 1, (d - number) / (d - c)), 0)})
        return results

    def lives_count(self, faze):
        hp = self.game_object_proxy.get_current_hit_points(self.map_proxy.get_bases_positions().pop())
        result = self.get_f(self.lives, hp)
        # print("hp = ", hp, ", result = ", result)
        return result[faze]

    def enemy_distance_count (self, faze):
        pos = self.map_proxy.get_inner_tiles()
        enemies = list()
        for p in pos:
            if self.game_object_proxy.get_role(p) == GameRole.ATTACKER:
                enemies.append(p)
        if len(enemies) == 0:
            dist = 16
        else:
            dist = self.map_proxy.get_bases_positions().pop().distance_to_nearest(enemies)
        result = self.get_f(self.enemy_distance, dist)
        # print("distance = ", dist, ', result = ', result)
        return result[faze]

    def first_free_tile(self, terrain_type: str):
        """ Find random tile with given terrain type """
        tiles = self.map_proxy.get_inner_tiles()
        border_tiles = self.map_proxy.get_border_tiles()

        for position in tiles:
            terrain = self.map_proxy.get_terrain_type(position) == TerrainType.from_string(terrain_type)
            if terrain and position not in border_tiles:
                pos = position
                if (2 >= position.offset.q >= -2) and (-2 <= position.offset.r <= 2):
                    return position
        return pos

    def free_tile_around_king(self):
        """ Find random tile with given terrain type """
        pos = self.map_proxy.get_bases_positions()
        n = pos.pop().get_all_neighbours()
        for i in n:
            if self.map_proxy.is_position_occupied(i):
                return None
        return n

    def baseIsNotSurrounded(self):
        """ Find random tile with given terrain type """
        pos = self.map_proxy.get_bases_positions()
        n = pos.pop().get_all_neighbours()
        res = list()
        for i in n:
            if not self.map_proxy.is_position_occupied(i):
                res.append(i)
        money = self.game_object_proxy.get_resources(self.player)
        cnt = money // 12
        while len(res) > cnt:
            res.pop()
        if len(res) > 0:
            return res
        return None

    def free_tiles(self):
        """ Find random free tile with given terrain type """
        tiles = self.map_proxy.get_player_visible_tiles()
        border_tiles = self.map_proxy.get_border_tiles()
        pos = []
        for position in tiles:
            occupied = self.map_proxy.is_position_occupied(position)
            if not occupied and position not in border_tiles:
                pos.append(position)
        if len(pos) == 0:
            return None
        return pos

    def visible_free_tile(self):
        """ Find random free tile with given terrain type """
        tiles = self.map_proxy.get_player_visible_tiles()
        border_tiles = self.map_proxy.get_border_tiles()
        for position in tiles:
            occupied = self.map_proxy.is_position_occupied(position)
            if not occupied and position not in border_tiles:
                return position
        return None

    def object_count(self, type):
        if type == 'archer':
            type = GameObjectType.ARCHER
        elif type == 'knight':
            type = GameObjectType.KNIGHT
        elif type == 'druid':
            type = GameObjectType.DRUID
        elif type == 'magician':
            type = GameObjectType.MAGICIAN
        elif type == 'ent':
            type = GameObjectType.ENT
        pos = self.map_proxy.get_player_visible_tiles();
        cnt = 0
        for p in pos:
            if type == self.game_object_proxy.get_object_type(p):
                cnt += 1
        return cnt
