from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Any, Set, Union, Dict, Callable, Tuple
from collections import deque

from ExpertSystem.Structure.Enums import LogicalOperator
from ExpertSystem.Structure.RuleBase import Rule, Expression, Fact, DataHolderFact
from OrodaelTurrim.Business.Interface.Player import IPlayer, PlayerTag
from OrodaelTurrim.Business.Proxy import MapProxy, GameObjectProxy, GameControlProxy, GameUncertaintyProxy
import inspect

from OrodaelTurrim.Structure.Exceptions import BadActionBaseParameters, BadFactDataValue
from OrodaelTurrim.Structure.Position import OffsetPosition, CubicPosition, AxialPosition

if TYPE_CHECKING:
    from User.ActionBase import ActionBase


class IKnowledgeBase(ABC):
    """ Abstract class for User knowledge base definition """


    def __init__(self, map_proxy: MapProxy, game_object_proxy: GameObjectProxy,
                 game_uncertainty_proxy: GameUncertaintyProxy, player: PlayerTag):
        self.map_proxy = map_proxy
        self.game_object_proxy = game_object_proxy
        self.game_uncertainty_proxy = game_uncertainty_proxy
        self.player = player


    @abstractmethod
    def create_knowledge_base(self) -> List[Fact]:
        """
        This method will be called every time before inference. This method should return List of created Facts
        """
        pass


class IInference(ABC):
    """ Abstract class for inference """


    @abstractmethod
    def infere(self, knowledge_base: Set[Any], rules: List[Rule], action_base: "ActionBase") -> None:
        """
        Inference method

        :param knowledge_base: - knowledge base created in the KnowledgeBase class by user
        :param rules: - parsed rules from rules file
        :param action_base: - instance of User defined action base
        """
        pass


class IActionBase(ABC):
    """
    Abstract method for user defined action base

    You can use `in` operator to check if method is in base (str or Expression)

    You can use ``[]`` operator to call function from ActionBase (with str without argument or Expresion with arguments)
    """


    def __init__(self, game_control_proxy: GameControlProxy, map_proxy: MapProxy, player: Union[IPlayer, PlayerTag]):
        """
        Constructor of Action base

        :param game_control_proxy: proxy for user operations
        :param player: Instance of your player
        """
        self.game_control_proxy = game_control_proxy
        self.map_proxy = map_proxy
        self.player = player


def check_method_parameters(method_parameters: inspect.FullArgSpec, parameters_injection: List[str],
                            function_name: str) -> bool:
    """
    Check, if data parameters could be injected without conflict

    :param method_parameters: Full argument specification of method
    :param parameters_injection: List of names of parameters, that should be injected
    :param function_name: Name of the function
    :return: True if parameters could be injected, raise Exception otherwise
    """
    if method_parameters.varkw is not None:
        return True

    for parameter in parameters_injection:
        if parameter in method_parameters.args:
            for i in range(method_parameters.args.index(parameter) + 1, len(method_parameters.args)):
                if method_parameters.args[i] not in parameters_injection:
                    raise BadActionBaseParameters(
                        f'ActionBase method "{function_name}" has position argument "{method_parameters.args[i]}" after injected argument "{parameter}"')
        elif parameter in method_parameters.kwonlyargs:
            pass
        else:
            raise BadActionBaseParameters(f'ActionBase method "{function_name}" has no "{parameter}" argument')

    return True


def check_return_values(injections: Dict) -> bool:
    """
    Check return values of data facts. Supported is only Position or iterable of Position
    :param injections: injected parameters
    :return: True if everything is fine, Raise exception otherwise
    """
    for name, argument in injections.items():
        if isinstance(argument, (OffsetPosition, CubicPosition, AxialPosition)):
            return True
        elif type(argument) in (list, tuple, set) and all(
                [isinstance(item, (OffsetPosition, CubicPosition, AxialPosition)) for item in argument]):
            return True
        elif argument is None:
            return True
        else:
            raise BadFactDataValue(f'Fact {name} returns unsupported data type')


def create_virtual_function(target_method: Callable, injection: Dict[str, DataHolderFact]) -> Callable:
    """
    This function will create virtual function, that is used for call method from ActionBase.
    Virtual method evaluate inject parameters when it's executed.
    """


    def virtual_function(*args, **kwargs):
        parameter_to_inject = {}
        for key, value in injection.items():
            try:
                parameter_to_inject[key] = value.fact.data(*value.arguments)
            except TypeError:
                parameter_to_inject[key] = value.fact.data()

        check_method_parameters(inspect.getfullargspec(target_method), list(parameter_to_inject.keys()),
                                target_method.__name__)
        check_return_values(parameter_to_inject)
        target_method(*args, **dict(parameter_to_inject, **kwargs))


    return virtual_function


def create_data_holder_callable(rule: Rule, facts: List[Fact], action_base: IActionBase) -> Tuple[
    Dict[Expression, Callable], List[str]]:
    """
    This method will create dictionary, where keys are Expressions and values are methods with injected parameters.
    Method from action base and also injected parameters are executed with action call.

    :param rule: rule to parse
    :param facts: list of all facts
    :param action_base: user defined action base
    :return:
    """
    data_process = deque((rule.condition,))

    fact_dictionary = {}
    for fact in facts:
        fact_dictionary[fact.name] = fact

    # Find all fact with data holder mark
    data_holder_facts = {}
    while data_process:
        current = data_process.pop()
        if current.operator in (LogicalOperator.AND, LogicalOperator.OR):
            data_process.append(current.left)
            data_process.append(current.right)
        elif isinstance(current.value, Expression):
            # Marked as data holder and defined in facts
            if current.value.data_holder_mark and current.value.name in fact_dictionary:
                fact_object = fact_dictionary[current.value.name]
                arguments = current.value.args
                data_holder_facts[current.value.name] = DataHolderFact(fact_object, arguments)

    # Find all actions with data holder parameters
    virtual_functions = {}
    data_process = deque((rule.conclusion,))
    while data_process:
        current = data_process.pop()
        if current.operator == LogicalOperator.AND:
            data_process.append(current.left)
            data_process.append(current.right)
        elif isinstance(current.value, Expression):
            parameter_injection = {}
            # Check all parameters of action and prepare injection for data holder ones
            for parameter in current.value.args:
                if parameter in data_holder_facts:
                    parameter_injection[parameter] = data_holder_facts[parameter]

            try:
                original_method = getattr(action_base, current.value.name)
            except AttributeError:
                continue
            # Create virtual function defined by Expression object
            virtual_functions[current.value] = create_virtual_function(original_method, parameter_injection)

    return virtual_functions, list(data_holder_facts.keys())


class ActionBaseCaller:
    def __init__(self, facts: List[Fact], action_base: IActionBase, rules: List[Rule]):
        self.__data_holder_parameters = []
        self.__virtual_functions = {}
        self.__create_callable(facts, action_base, rules)
        del action_base
        del facts


    def __create_callable(self, facts: List[Fact], action_base: IActionBase, rules: List[Rule]) -> None:
        """
        Create same methods as ActionBase with injected parameters

        :param facts: List of Facts
        :param action_base: User ActionBase implementation object
        :param rules: list of rules
        """
        self.virtual_functions = {}

        for rule in rules:
            virtual_function, data_holder_parameters = create_data_holder_callable(rule, facts, action_base)
            self.__virtual_functions.update(virtual_function)
            self.__data_holder_parameters.extend(data_holder_parameters)


    def call(self, method: Union[Expression]) -> None:
        """
        Call method from action base. You can define method with string name or Expression object.
        With string name, you cannot pass the parameters.
        With Expression object, parameters are passed automatically.

        :param method: string name or expression node defining Action
        """
        if isinstance(method, Expression):
            parameters = [parameter for parameter in method.args if parameter not in self.__data_holder_parameters]
            if method in self.__virtual_functions:
                self.__virtual_functions[method](*parameters)
            else:
                raise ValueError('There is no function that is defined by this Expression')
        else:
            raise ValueError('Get functions only by Expression')


    def has_method(self, method: Expression) -> bool:
        """
        This method check, if ActionBase contains given method.
        You can define method with string name or Expression object.

        :param method: string name or expression node defining Action
        :return: True if method exists, False otherwise
        """
        return self.__contains__(method)


    def __contains__(self, item: Expression) -> bool:
        if isinstance(item, Expression):
            if item in self.__virtual_functions:
                return True
            return False

        raise ValueError('Test only with Expression')
