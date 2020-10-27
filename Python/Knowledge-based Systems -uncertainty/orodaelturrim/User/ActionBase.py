from OrodaelTurrim.Business.Interface.Player import PlayerTag
from OrodaelTurrim.Business.Proxy import GameControlProxy
from ExpertSystem.Business.UserFramework import IActionBase
from OrodaelTurrim.Business.Logger import Logger
from OrodaelTurrim.Structure.Enums import GameObjectType
from OrodaelTurrim.Structure.Filter.AttackFilter import AttackStrongestFilter
from OrodaelTurrim.Structure.Filter.Factory import FilterFactory
from OrodaelTurrim.Structure.GameObjects.GameObject import SpawnInformation
from OrodaelTurrim.Structure.Position import OffsetPosition

from User.AttackFilter import DummyAttackFilter, EmptyAttackFilter


class ActionBase(IActionBase):
    """
    You can define here your custom actions. Methods must be public (not starting with __ or _) and must have unique
    names. Methods could have as many arguments as you want. Instance of this class will be available in
    Inference class.

    **This class provides:**

    * self.game_control_proxy [GameControlProxy] for doing actions in game
    * self.player [PlayerTag] instance of your player for identification yourself in proxy

    Usage of ActionBase is described in documentation.


    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!               TODO: Write implementation of your actions HERE                !!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    game_control_proxy: GameControlProxy
    player: PlayerTag

    def build_base(self, free_tile):
        # Custom log messages
        Logger.log('Building base')

        # Create instance of custom filter
        empty_filter = FilterFactory().attack_filter(EmptyAttackFilter)
        dummy_filter = FilterFactory().attack_filter(DummyAttackFilter, 'Base attacking')

        # Create instance of default filter
        strongest_filter = FilterFactory().attack_filter(AttackStrongestFilter)

        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             free_tile,
                             [strongest_filter], []))

    def build_base_random(self, random_tile):
        Logger.log('Building base')
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             GameObjectType.BASE,
                             random_tile,
                             [FilterFactory().attack_filter(AttackStrongestFilter)], []))

    def spawn(self, gameObjectType, tile):
      #  print(tile)
        self.game_control_proxy.spawn_unit(
            SpawnInformation(self.player,
                             gameObjectType,
                             tile,
                             [FilterFactory().attack_filter(AttackStrongestFilter)], []))

    def spawn_knight_around_king (self, free_tile_around_king):
        cnt = 1
        for x in free_tile_around_king:
            if cnt % 3 != 0:
                self.spawn(GameObjectType.KNIGHT, x)
            else:
                self.spawn(GameObjectType.DRUID, x)
            cnt += 1

    def spawn_archer(self, tile):
        self.spawn(GameObjectType.ARCHER, tile)

    def spawn_knight(self, tile):
        self.spawn(GameObjectType.KNIGHT, tile)

    def spawn_druid(self, tile_close_to_king):
        self.spawn(GameObjectType.DRUID, tile_close_to_king)

    def spawn_magician(self, tile):
        self.spawn(GameObjectType.MAGICIAN, tile)

    def spawn_ent(self, tile):
        self.spawn(GameObjectType.ENT, tile)

    def spawn_up(self, type, tile_up):
        if type == 'ARCHER':
            type = GameObjectType.ARCHER
        elif type == 'KNIGHT':
            type = GameObjectType.KNIGHT
        elif type == 'DRUID':
            type = GameObjectType.DRUID
        self.spawn(type, tile_up)

    def spawn_down(self, type, tile_down):
        if type == 'ARCHER':
            type = GameObjectType.ARCHER
        elif type == 'KNIGHT':
            type = GameObjectType.KNIGHT
        elif type == 'DRUID':
            type = GameObjectType.DRUID
        self.spawn(type, tile_down)

    def spawn_left(self, type, tile_left):
        if type == 'ARCHER':
            type = GameObjectType.ARCHER
        elif type == 'KNIGHT':
            type = GameObjectType.KNIGHT
        elif type == 'DRUID':
            type = GameObjectType.DRUID
        self.spawn(type, tile_left)

    def spawn_right(self, type, tile_right):
        if type == 'ARCHER':
            type = GameObjectType.ARCHER
        elif type == 'KNIGHT':
            type = GameObjectType.KNIGHT
        elif type == 'DRUID':
            type = GameObjectType.DRUID
        self.spawn(type, tile_right)

    def surround_base(self, baseIsNotSurrounded):
        for i in baseIsNotSurrounded:
            self.spawn(GameObjectType.KNIGHT, i)