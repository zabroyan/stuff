from random import randrange
from typing import List
from OrodaelTurrim.Business.Interface.Player import PlayerTag
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameUncertaintyProxy
from ExpertSystem.Business.UserFramework import IKnowledgeBase
from ExpertSystem.Structure.RuleBase import Fact
from OrodaelTurrim.Structure.Enums import TerrainType, AttributeType, EffectType, GameRole, GameObjectType
from OrodaelTurrim.Structure.Position import OffsetPosition, CubicPosition, AxialPosition


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
        unc_sp = self.game_uncertainty_proxy.spawn_information().pop()
        # for i in unc_sp:
        #     print("UNCERTAINTY: ", i.game_object_type, " at ")
        #     for p in i.positions:
        #         print(p.position, " with ", p.uncertainty)

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
        facts.append(Fact('random_tile', eval_function=self.first_random_tile, data=self.first_random_tile))
        facts.append(
            Fact('free_tile_around_king', eval_function=self.free_tile_around_king, data=self.free_tile_around_king))
        facts.append(Fact('tile', eval_function=self.visible_free_tile, data=self.visible_free_tile))
        facts.append(Fact('tile_up', eval_function=self.free_tile_up, data=self.free_tile_up))
        facts.append(Fact('tile_down', eval_function=self.free_tile_down, data=self.free_tile_down))
        facts.append(Fact('tile_left', eval_function=self.free_tile_left, data=self.free_tile_left))
        facts.append(Fact('tile_right', eval_function=self.free_tile_right, data=self.free_tile_right))
        facts.append(Fact('tile_close_to_king', eval_function=self.tile_close_to_king, data=self.tile_close_to_king))

        facts.append(Fact('archer_count', lambda: self.object_count('archer')))
        facts.append(Fact('knight_count', lambda: self.object_count('knight')))
        facts.append(Fact('magician_count', lambda: self.object_count('magician')))
        facts.append(Fact('druid_count', lambda: self.object_count('druid')))
        facts.append(Fact('ent_count', lambda: self.object_count('ent')))
        facts.append(Fact("knight_up", lambda: self.knight_up()))
        facts.append(Fact("knight_down", lambda: self.knight_down()))
        facts.append(Fact("knight_left", lambda: self.knight_left()))
        facts.append(Fact("knight_right", lambda: self.knight_left()))
        facts.append(Fact('enemy_up', lambda x: self.enemy_up(x)))
        facts.append(Fact('enemy_down', lambda x: self.enemy_down(x)))
        facts.append(Fact('enemy_left', lambda x: self.enemy_left(x)))
        facts.append(Fact('enemy_right', lambda x: self.enemy_right(x)))

        facts.append(Fact('spawn_enemy_up', lambda x: self.spawn_enemy_up(x)))
        facts.append(Fact('spawn_enemy_down', lambda x: self.spawn_enemy_down(x)))
        facts.append(Fact('spawn_enemy_left', lambda x: self.spawn_enemy_left(x)))
        facts.append(Fact('spawn_enemy_right', lambda x: self.spawn_enemy_right(x)))

        facts.append(
            Fact('baseIsNotSurrounded', eval_function=self.baseIsNotSurrounded, data=self.baseIsNotSurrounded))

        # Add numerical fact
        facts.append(Fact("money", lambda: self.game_object_proxy.get_resources(self.player)))

        return facts

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

    @staticmethod
    def first_random_tile():
        return OffsetPosition(randrange(-3, 3), randrange(-3, 3))

    def free_tile_around_king(self):
        """ Find random tile with given terrain type """
        pos = self.map_proxy.get_bases_positions()
        n = pos.pop().get_all_neighbours()
        for i in n:
            if self.map_proxy.is_position_occupied(i):
                return None
        return n

    def tile_close_to_king(self):
        pos = self.map_proxy.get_bases_positions().pop().get_all_neighbours()
        tiles = self.map_proxy.get_player_visible_tiles()
        res = set(pos)
        for i in pos:
            res.update(i.get_all_neighbours())
        pos = res.copy()
        for i in pos:
            res.update(i.get_all_neighbours())
        for i in res:
            if not self.map_proxy.is_position_occupied(i) and i in tiles:
                return i
        return None

    def free_tile_up(self):
        # x = {x-1, x, x+1}
        # y = {r...-6}
        """ Find random tile with given terrain type """
        pos = self.map_proxy.get_bases_positions().pop()
        x = pos.offset.q
        tiles = self.map_proxy.get_player_visible_tiles()
        while pos.offset.r > -6 and pos in tiles:
            if not self.map_proxy.is_position_occupied(pos):
                # print(pos)
                return pos
            elif not self.map_proxy.is_position_occupied(OffsetPosition(x-1, pos.offset.r)) and OffsetPosition(x-1, pos.offset.r) in tiles:
                # print(OffsetPosition(x-1, pos.offset.r))
                return OffsetPosition(x-1, pos.offset.r)
            elif not self.map_proxy.is_position_occupied(OffsetPosition(x+1, pos.offset.r)) and OffsetPosition(x+1, pos.offset.r) in tiles:
                # print(OffsetPosition(x-1, pos.offset.r))
                return OffsetPosition(x+1, pos.offset.r)
            pos = OffsetPosition(x, pos.offset.r - 1)
        return None

    def free_tile_down(self):
        # x = {x-1, x, x+1}
        # y = {r...6}
        """ Find random tile with given terrain type """
        pos = self.map_proxy.get_bases_positions().pop()
        x = pos.offset.q
        tiles = self.map_proxy.get_player_visible_tiles()
        while pos.offset.r < 6 and pos in tiles:
            if not self.map_proxy.is_position_occupied(pos):
                return pos
            elif not self.map_proxy.is_position_occupied(OffsetPosition(x-1, pos.offset.r)) and OffsetPosition(x-1, pos.offset.r) in tiles:
                return OffsetPosition(x-1, pos.offset.r)
            elif not self.map_proxy.is_position_occupied(OffsetPosition(x+1, pos.offset.r)) and OffsetPosition(x+1, pos.offset.r) in tiles:
                return OffsetPosition(x+1, pos.offset.r)
            pos = OffsetPosition(x, pos.offset.r + 1)
        return None

    def free_tile_left(self):
        # x = {q...6}
        # y = {y-1, y, y+1}
        """ Find random tile with given terrain type """
        pos = self.map_proxy.get_bases_positions().pop()
        y = pos.offset.r
        tiles = self.map_proxy.get_player_visible_tiles()
        while pos.offset.q < 6 and pos in tiles:
            if not self.map_proxy.is_position_occupied(pos):
                # print(pos)
                return pos
            elif not self.map_proxy.is_position_occupied(OffsetPosition(pos.offset.q, y-1)) and OffsetPosition(pos.offset.q, y-1) in tiles:
                # print(OffsetPosition(x-1, pos.offset.r))
                return OffsetPosition(pos.offset.q, y-1)
            elif not self.map_proxy.is_position_occupied(OffsetPosition(pos.offset.q, y+1)) and OffsetPosition(pos.offset.q, y+1) in tiles:
                # print(OffsetPosition(x-1, pos.offset.r))
                return OffsetPosition(pos.offset.q, y+1)
            pos = OffsetPosition(pos.offset.q+1, y)
        return None

    def free_tile_right(self):
        # x = {q...-6}
        # y = {y-1, y, y+1}
        """ Find random tile with given terrain type """
        pos = self.map_proxy.get_bases_positions().pop()
        y = pos.offset.r
        tiles = self.map_proxy.get_player_visible_tiles()
        while pos.offset.q > -6 and pos in tiles:
            if not self.map_proxy.is_position_occupied(pos):
                # print(pos)
                return pos
            elif not self.map_proxy.is_position_occupied(OffsetPosition(pos.offset.q, y-1)) and OffsetPosition(pos.offset.q, y-1) in tiles:
                # print(OffsetPosition(x-1, pos.offset.r))
                return OffsetPosition(pos.offset.q, y-1)
            elif not self.map_proxy.is_position_occupied(OffsetPosition(pos.offset.q, y+1)) and OffsetPosition(pos.offset.q, y+1) in tiles:
                # print(OffsetPosition(x-1, pos.offset.r))
                return OffsetPosition(pos.offset.q, y+1)
            pos = OffsetPosition(pos.offset.q-1, y)
        return None

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

    def spawn_enemy_up (self, range):
        # y = -6
        unc_sp = self.game_uncertainty_proxy.spawn_information()[int(range)]
        sum = 0;
        for i in unc_sp:
            for p in i.positions:
                if p.position.offset.r == -6:
                    sum += p.uncertainty
        # print("range = ", range, "; sum_up = ", sum)
        return sum

    def spawn_enemy_down (self, range):
        # y = -6
        unc_sp = self.game_uncertainty_proxy.spawn_information()[int(range)]
        sum = 0;
        for i in unc_sp:
            for p in i.positions:
                if p.position.offset.r == 6:
                    sum += p.uncertainty
      #  print("sum_down = ", sum)
        return sum

    def spawn_enemy_left (self, range):
        # y = -6
        unc_sp = self.game_uncertainty_proxy.spawn_information()[int(range)]
        sum = 0;
        for i in unc_sp:
            for p in i.positions:
                if p.position.offset.q == 6:
                    sum += p.uncertainty
        # print("sum_left = ", sum)
        return sum

    def spawn_enemy_right (self, range):
        # y = -6
        unc_sp = self.game_uncertainty_proxy.spawn_information()[int(range)]
        sum = 0;
        for i in unc_sp:
            for p in i.positions:
                if p.position.offset.q == -6:
                    sum += p.uncertainty

        # print("sum_right = ", sum)
        return sum

    def knight_up(self):
        cnt = 0
        pos = self.map_proxy.get_bases_positions().pop()
        x = pos.offset.q
        tiles = self.map_proxy.get_player_visible_tiles()
        while pos.offset.r > -6 and pos in tiles:
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(pos):
                cnt += 1
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(OffsetPosition(x - 1, pos.offset.r)):
                cnt += 1
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(OffsetPosition(x + 1, pos.offset.r)):
                cnt += 1
            pos = OffsetPosition(x, pos.offset.r - 1)
        # print("KNIGHT_Up = ", cnt)
        return cnt

    def knight_down(self):
        cnt = 0
        pos = self.map_proxy.get_bases_positions().pop()
        x = pos.offset.q
        tiles = self.map_proxy.get_player_visible_tiles()
        while pos.offset.r < 6 and pos in tiles:
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(pos):
                cnt += 1
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(OffsetPosition(x - 1, pos.offset.r)):
                cnt += 1
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(OffsetPosition(x + 1, pos.offset.r)):
                cnt += 1
            pos = OffsetPosition(x, pos.offset.r + 1)
        # print("KNIGHT_Do = ", cnt)
        return cnt

    def knight_left(self):
        cnt = 0
        pos = self.map_proxy.get_bases_positions().pop()
        y = pos.offset.r
        tiles = self.map_proxy.get_player_visible_tiles()
        while pos.offset.q < 6 and pos in tiles:
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(pos):
                cnt += 1
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(OffsetPosition(pos.offset.q, y-1)):
                cnt += 1
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(OffsetPosition(pos.offset.q, y+1)):
                cnt += 1
            pos = OffsetPosition(pos.offset.q+1, y)
        # print("KNIGHT_Le = ", cnt)
        return cnt

    def knight_right(self):
        cnt = 0
        pos = self.map_proxy.get_bases_positions().pop()
        y = pos.offset.r
        tiles = self.map_proxy.get_player_visible_tiles()
        while pos.offset.q > -6 and pos in tiles:
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(pos):
                cnt += 1
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(OffsetPosition(pos.offset.q, y - 1)):
                cnt += 1
            if GameObjectType.KNIGHT == self.game_object_proxy.get_object_type(OffsetPosition(pos.offset.q, y + 1)):
                cnt += 1
            pos = OffsetPosition(pos.offset.q - 1, y)
        # print("KNIGHT_Ri = ", cnt)
        return cnt

    def enemy_up (self, type):
        # y = -6
        if type == 'MINOTAUR':
            type = GameObjectType.MINOTAUR
        elif type == 'DEMON':
            type = GameObjectType.DEMON
        unc_sp = self.game_uncertainty_proxy.spawn_information().pop()
        for i in unc_sp:
            for p in i.positions:
                if p.position.offset.r == -6 and i.game_object_type == type:
                    # print(type, "up")
                    return True
        return False

    def enemy_down (self, type):
        # y = 6
        if type == 'MINOTAUR':
            type = GameObjectType.MINOTAUR
        elif type == 'DEMON':
            type = GameObjectType.DEMON
        unc_sp = self.game_uncertainty_proxy.spawn_information().pop()
        for i in unc_sp:
            for p in i.positions:
                if p.position.offset.r == 6 and i.game_object_type == type:
                    # print(type, "down")
                    return True
        return False

    def enemy_left (self, type):
        # x = -6
        if type == 'MINOTAUR':
            type = GameObjectType.MINOTAUR
        elif type == 'DEMON':
            type = GameObjectType.DEMON
        unc_sp = self.game_uncertainty_proxy.spawn_information().pop()
        for i in unc_sp:
            for p in i.positions:
                if p.position.offset.q == -6 and i.game_object_type == type:
                    # print(type, "left")
                    return True
        return False

    def enemy_right (self, type):
        # x = 6
        if type == 'MINOTAUR':
            type = GameObjectType.MINOTAUR
        elif type == 'DEMON':
            type = GameObjectType.DEMON
        unc_sp = self.game_uncertainty_proxy.spawn_information().pop()
        for i in unc_sp:
            for p in i.positions:
                if p.position.offset.q == 6 and i.game_object_type == type:
                    # print(type,"right")
                    return True
        return False