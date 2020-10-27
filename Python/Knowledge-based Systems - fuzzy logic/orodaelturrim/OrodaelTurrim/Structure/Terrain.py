from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from OrodaelTurrim.Structure.Enums import TerrainType, AttributeType


class Terrain(ABC):
    """ Abstract class for terrain types."""


    def compute_damage(self, hit_points: float) -> float:
        """
        Computes, how much damage will this terrain inflict on start of each turn

        :param hit_points: Previous value of hit points of game object
        :return: Amount of damage to be inflicted to game object
        """
        return 0


    def affect_actions(self, original_value: float) -> float:
        return original_value


    def affect_max_hit_points(self, original_value: int) -> int:
        return original_value


    def affect_range(self, original_value: int) -> int:
        return original_value


    def affect_sight(self, original_value: int) -> int:
        return original_value


    def affect_attack(self, original_value: float) -> float:
        return original_value


    def affect_defense(self, original_value: float) -> float:
        return original_value


    def affect_attribute(self, attribute: "AttributeType", original_value: Union[int, float]) -> Union[float, int]:
        """
        Provides affected value of specified attribute by this terrain

        :param attribute: Type of attribute, which should be affected
        :param original_value: Original value of affected attribute
        :return: Affected value of specified attribute by this terrain
        """
        from OrodaelTurrim.Structure.Enums import AttributeType

        if attribute == AttributeType.ACTIONS:
            return self.affect_actions(original_value)

        elif attribute == AttributeType.HIT_POINTS:
            return self.affect_max_hit_points(original_value)

        elif attribute == AttributeType.ATTACK_RANGE:
            return self.affect_range(original_value)

        elif attribute == AttributeType.SIGHT:
            return self.affect_sight(original_value)

        elif attribute == AttributeType.ATTACK:
            return self.affect_attack(original_value)

        elif attribute == AttributeType.DEFENSE:
            return self.affect_defense(original_value)


    @abstractmethod
    def get_move_cost(self, target: 'TerrainType') -> int:
        """
        Get move cost of the terrain based current terrain type and target terrain type.
        Move cost have value based on target and source terrain type

        :param target:  target terrain type
        :return: action cost
        """
        pass


    @abstractmethod
    def get_remaining_sigh(self, current_sight: int) -> int:
        """
        Get remaining sight after current terrain type

        :param current_sight: current sight number
        :return: remaining sight
        """
        pass


    @property
    @abstractmethod
    def terrain_type(self) -> 'TerrainType':
        pass


    def info_text(self) -> str:
        """ Return text information of the terrain"""
        return ""


    @abstractmethod
    def char(self) -> str:
        """ Return character that represent this terrain type for string map definition """
        pass


class Field(Terrain):
    """
    Class representing field on map. This to horizon stretching plane of yellow crop provides neither bonuses
    nor penalties. Just an opportunity to ruin another harvest.
    """


    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.HILL, TerrainType.FOREST, TerrainType.RIVER):
            return 2
        else:
            return 1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 1


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.FIELD


    def char(self) -> str:
        return 'I'


    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: 1</p>        
        """.format()


class Forest(Terrain):
    """
    Class representing ever green forest. The shadows of the trees provide shelter from enemy arrows
    and the bushes make excellent place for an ambush. However, entering the forest might prove bit exhausting.
    """


    def get_move_cost(self, target: 'Terrain') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.HILL, TerrainType.RIVER):
            return 2
        else:
            return 1


    def affect_defense(self, original_value: float):
        return original_value * 1.2


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 3


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.FOREST


    def char(self) -> str:
        return 'F'


    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: 3</p>        
        <p>Attack bonus: 0.2</p>        
        <p>Defence bonus: 0.1</p>        
        """.format()


class Hill(Terrain):
    """
    Class representing little hill. Someone kept on throwing piles of dirt here and now look, there is a hill.
    """


    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.HILL:
            return 1
        else:
            return 2


    def affect_attack(self, original_value: float):
        return original_value * 1.1


    def affect_defense(self, original_value: float):
        return original_value * 1.1


    def affect_sight(self, original_value: int) -> int:
        return original_value + 1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight // 2


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.HILL


    def char(self) -> str:
        return 'H'


    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: half</p>        
        <p>Attack bonus: 0.1</p>        
        <p>Defence bonus: 0.1</p>        
        """.format()


class Mountain(Terrain):
    """
    Class representing pointy rock giants. Everyone who tried climbing those knows, it is not a piece of cake.
    On the other hand, they provide great place to stay safe, since nobody wants to climb them either.
    """


    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 2
        else:
            return 3


    def affect_attack(self, original_value: float):
        return original_value * 0.8


    def affect_defense(self, original_value: float):
        return original_value * 1.5


    def affect_sight(self, original_value: int):
        return original_value + 3


    def get_remaining_sigh(self, current_sight: int) -> int:
        return 0


    def compute_damage(self, hit_points: float):
        return hit_points * 0.05


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.MOUNTAIN


    def char(self) -> str:
        return 'M'


    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: all</p>        
        <p>Attack bonus: -0.2</p>        
        <p>Defence bonus: 0.5</p>        
        <p>Damage: 0.05</p>        
        """.format()


class River(Terrain):
    """
    Class representing mass of water. Does not matter if it´s river, lake or pond, nobody wants to get wet.
    Especially not Larry (he cannot swim).
    """


    def get_move_cost(self, target: 'TerrainType') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 4
        elif target in (TerrainType.FOREST, TerrainType.HILL):
            return 3
        elif target == TerrainType.RIVER:
            return 1
        else:
            return 2


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 1


    def affect_attack(self, original_value: float):
        return original_value * 0.8


    def affect_defense(self, original_value: float):
        return original_value * 0.8


    def affect_actions(self, original_value: float):
        return original_value - 1


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.RIVER


    def char(self) -> str:
        return 'R'


    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: 1</p>        
        <p>Attack bonus: -0.2</p>        
        <p>Action reduction: 1</p>        
        <p>Defence bonus: -0.2</p>        
        """.format()


class Village(Terrain):
    """
    Class representing little village in the countryside. Few huts, church and pub - everything a simple
    adventurer would need and even more!
    """


    def get_move_cost(self, target: 'Terrain') -> int:
        from OrodaelTurrim.Structure.Enums import TerrainType
        if target == TerrainType.MOUNTAIN:
            return 3
        elif target in (TerrainType.FOREST, TerrainType.HILL, TerrainType.RIVER):
            return 2
        else:
            return 1


    def affect_attack(self, original_value: float):
        return original_value * 1


    def affect_defense(self, original_value: float):
        return original_value * 1.3


    def affect_actions(self, original_value: float):
        return original_value + 1


    def get_remaining_sigh(self, current_sight: int) -> int:
        return current_sight - 1


    @property
    def terrain_type(self) -> 'TerrainType':
        from OrodaelTurrim.Structure.Enums import TerrainType
        return TerrainType.VILLAGE


    def char(self) -> str:
        return 'V'


    def info_text(self):
        return """    
        <br>            
        <p>Sight cost: 1</p>        
        <p>Attack bonus: 0</p>        
        <p>Defence bonus: 0.3</p>        
        <p>Actions bonus: 1</p>        
        """.format()
