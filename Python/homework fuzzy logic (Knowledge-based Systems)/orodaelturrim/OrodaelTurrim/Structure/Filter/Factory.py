import inspect
import sys
from multi_key_dict import multi_key_dict
from typing import Dict, Union, List, Optional

from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy
from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter, MoveFilter
from OrodaelTurrim.Structure.Utils import Singleton


class FilterClassInfo:
    def __init__(self, name, cls, arguments):
        self.name = name
        self.cls = cls
        self.arguments = arguments


class FilterFactory(metaclass=Singleton):
    """ Factory for easy creating filters without need proxy instances """


    def __init__(self, map_proxy: MapProxy = None, game_object_proxy: GameObjectProxy = None):
        self.__map_proxy = map_proxy
        self.__game_object_proxy = game_object_proxy

        self.__attack_filters = multi_key_dict()
        self.__move_filters = multi_key_dict()

        self.__prepare_attack_filters()
        self.__prepare_move_filters()


    def __prepare_attack_filters(self):
        """ Find attack filters in each possible location, check if they are correct and register them """
        from OrodaelTurrim.Structure.Filter import AttackFilter as ODAttackFilter
        from OrodaelTurrim.Structure.Filter.FilterPattern import AttackFilter as AttackFilterPattern
        from ArtificialIntelligence import Filter as AIFilter
        from User import AttackFilter as UAttackFilter

        # Load Attack filter from OrodaelTurrim and User modules
        for module in (ODAttackFilter, UAttackFilter, AIFilter):
            for name, obj, in inspect.getmembers(module):
                # Check if it is class
                if not inspect.isclass(obj):
                    continue

                if name == 'MoveFilter' or name == 'AttackFilter':
                    continue

                # Check if it is subclass of AttackFilter
                if not issubclass(obj, AttackFilterPattern):
                    continue

                # Check if class is not abstract
                if inspect.isabstract(obj):
                    sys.stderr.write('Filter {} not loaded, class cannot be abstract\n'.format(name))
                    continue

                arguments = inspect.getfullargspec(obj.__init__).args
                if arguments[1] != 'map_proxy' or arguments[2] != 'game_object_proxy':
                    sys.stderr.write('Filter {} not loaded because bad __init__ signature\n'.format(name))
                    continue

                parameters = [parameter for parameter in inspect.getfullargspec(obj.__init__).args if
                              parameter not in ['self', 'map_proxy', 'game_object_proxy']]

                self.__attack_filters[name, obj] = FilterClassInfo(name, obj, parameters)


    def __prepare_move_filters(self):
        """ Find move filters in each possible location, check if they are correct and register them """
        from OrodaelTurrim.Structure.Filter import MoveFilter
        from OrodaelTurrim.Structure.Filter.FilterPattern import MoveFilter as MoveFilterPattern
        from ArtificialIntelligence import Filter as AIFilter

        for module in (MoveFilter, AIFilter):
            for name, obj, in inspect.getmembers(module):
                # Check if it is class
                if not inspect.isclass(obj):
                    continue

                if name == 'MoveFilter' or name == 'AttackFilter':
                    continue

                # Check if it is subclass of MoveFilterPattern
                if not issubclass(obj, MoveFilterPattern):
                    continue

                # Check if class is not abstract
                if inspect.isabstract(obj):
                    sys.stderr.write('Filter {} not loaded, class cannot be abstract\n'.format(name))
                    continue

                arguments = inspect.getfullargspec(obj.__init__).args
                if arguments[1] != 'map_proxy' or arguments[2] != 'game_object_proxy':
                    sys.stderr.write('Filter {} not loaded because bad __init__ signature\n'.format(name))
                    continue

                parameters = [parameter for parameter in inspect.getfullargspec(obj.__init__).args if
                              parameter not in ['self', 'map_proxy', 'game_object_proxy']]

                self.__move_filters[name, obj] = FilterClassInfo(name, obj, parameters)


    def attack_filter(self, name: Union[str, type], *args, **kwargs) -> Optional[AttackFilter]:
        """
        Get instance of attack filter by name or class

        :param name: str name of the class or Class type itself
        :param args: extra arguments that filter need (don't pass proxy arguments)
        :param kwargs: extra keyword arguments that filter need (don't pass proxy arguments)
        :return: None if filter doesn't exists,
                Raise exception if there is problem with creating Filter,
                Attack filter otherwise
        """
        if name not in self.__attack_filters:
            return None

        return self.__attack_filters[name].cls(self.__map_proxy, self.__game_object_proxy, *args, **kwargs)


    def move_filter(self, name: Union[str, type], *args, **kwargs) -> Optional[MoveFilter]:
        """
        Get instance of move filter by name or class

        :param name: str name of the class or Class type itself
        :param args: extra arguments that filter need (don't pass proxy arguments)
        :param kwargs: extra keyword arguments that filter need (don't pass proxy arguments)
        :return: None if filter doesn't exists,
                Raise exception if there is problem with creating Filter,
                Move filter otherwise
        """
        if name not in self.__move_filters:
            return None

        return self.__move_filters[name].cls(self.__map_proxy, self.__game_object_proxy, *args, **kwargs)


    @property
    def attack_filters(self) -> List[FilterClassInfo]:
        """ Get list of FilterClassInfo of all founded attack filters """
        return self.__attack_filters.values()


    @property
    def move_filters(self) -> List[FilterClassInfo]:
        """ Get list of FilterClassInfo of all founded move filters """
        return self.__move_filters.values()


    def get_attack_filter_by_name(self, name: str) -> FilterClassInfo:
        return self.__attack_filters.get(name)


    def get_move_filter_by_name(self, name: str) -> FilterClassInfo:
        return self.__move_filters.get(name)
