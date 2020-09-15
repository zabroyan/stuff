from typing import Union, List, Callable, Optional

from ExpertSystem.Structure.Enums import Operator, LogicalOperator
from OrodaelTurrim.Structure.Position import Position


class Expression:
    """
    Class that represent one expression in the tree

    **Example:**

    UNIT_ARMOR 2 5 >= 25 [0.25]

    - name -> UNIT_ARMOR
    - args -> [2,5]
    - comparator -> >=
    - value -> 25
    - uncertainty -> 0.25
    """


    def __init__(self):
        self.__name = None
        self.__args = []
        self.__comparator = None
        self.__value = None
        self.__uncertainty = None
        self.__data_holder_mark = None


    @property
    def name(self) -> str:
        """ Name of the expression """
        return self.__name


    @name.setter
    def name(self, value: str):
        self.__name = value


    @property
    def args(self) -> List[str]:
        """ List of expression arguments """
        return self.__args


    @args.setter
    def args(self, value: List[str]):
        self.__args = value


    @property
    def comparator(self) -> Operator:
        """ Comparator between expression and value (<, >, <=, >=, ==, !=) """
        return self.__comparator


    @comparator.setter
    def comparator(self, value: Union[Operator, str]):
        if type(value) is str:
            self.__comparator = Operator.from_string(value)
        else:
            self.__comparator = value


    @property
    def value(self) -> Union[str, int, float, bool]:
        """ Value of constant """
        return self.__value


    @value.setter
    def value(self, value: Union[str, int, float, bool]):
        self.__value = value


    @property
    def uncertainty(self) -> float:
        """ Get uncertainty of the expression """
        return self.__uncertainty


    @uncertainty.setter
    def uncertainty(self, value: float):
        self.__uncertainty = value


    @property
    def data_holder_mark(self) -> bool:
        return self.__data_holder_mark


    @data_holder_mark.setter
    def data_holder_mark(self, value: bool):
        self.__data_holder_mark = value


    def evaluate(self):  # TODO: What to do whit this
        pass


    def __repr__(self):
        text = ''
        text += '{} {}'.format(self.name, ' '.join(self.args))
        if self.comparator:
            text += ' {} {}'.format(self.comparator.value, self.value)

        if self.uncertainty:
            text += '[{}]'.format(self.uncertainty)
        return text


class ExpressionNode:
    """ One node in the tree representing representation """


    def __init__(self):
        self.__left = None
        self.__right = None
        self.__operator = None
        self.__value = None
        self.__parent = None
        self.__parentheses = False


    @property
    def left(self) -> Optional["ExpressionNode"]:
        """ Left child of the Node """
        return self.__left


    @left.setter
    def left(self, value: "ExpressionNode"):
        self.__left = value


    @property
    def right(self) -> Optional["ExpressionNode"]:
        """ Right child of the Node """
        return self.__right


    @right.setter
    def right(self, value: "ExpressionNode"):
        self.__right = value


    @property
    def value(self) -> Optional[Expression]:
        """
        If node has not left and right child, value is Expression, otherwise value is None
        """
        return self.__value


    @value.setter
    def value(self, value: Optional[Expression]):
        self.__value = value


    @property
    def operator(self) -> Optional[LogicalOperator]:
        """ Return logical operator between left and right child. If Node don't have child, operator is None"""
        return self.__operator


    @operator.setter
    def operator(self, value: Optional[LogicalOperator]):
        self.__operator = value


    @property
    def parent(self) -> Union["ExpressionNode", None]:
        """ Parent of the node """
        return self.__parent


    @parent.setter
    def parent(self, value: "ExpressionNode"):
        self.__parent = value


    @property
    def parentheses(self) -> bool:
        """ True if current level of expression have parentheses """
        return self.__parentheses


    @parentheses.setter
    def parentheses(self, value: bool):
        self.__parentheses = value


    def __repr__(self):
        if self.left:
            if self.parentheses:
                return '({} {} {})'.format(self.left.__repr__(), self.operator, self.right.__repr__())
            else:
                return '{} {} {}'.format(self.left.__repr__(), self.operator, self.right.__repr__())
        else:
            return self.value.__repr__()


class Rule:
    """ Class for store one rule """


    def __init__(self):
        self.__condition = None
        self.__conclusion = None
        self.__uncertainty = None


    @property
    def condition(self) -> ExpressionNode:
        """ Condition of the rule (left side of the expression) """
        return self.__condition


    @condition.setter
    def condition(self, value):
        self.__condition = value


    @property
    def conclusion(self) -> ExpressionNode:
        """ Conclusion of the rule (right side of the expression) """
        return self.__conclusion


    @conclusion.setter
    def conclusion(self, value):
        self.__conclusion = value


    @property
    def uncertainty(self) -> float:
        """ Get uncertainty of the whole rule """
        return self.__uncertainty


    @uncertainty.setter
    def uncertainty(self, value):
        self.__uncertainty = value


    def __repr__(self):
        if self.uncertainty:
            return 'IF {} THEN {} WITH {}'.format(self.condition.__repr__(), self.conclusion.__repr__(),
                                                  self.uncertainty)
        else:
            return 'IF {} THEN {}'.format(self.condition.__repr__(), self.conclusion.__repr__())


class Fact:
    """
    Class Fact should store information about one Fact in Knowledge base.
    Fact is defined with name (name must be unique). Also Fact could hold information about probability.

    User must define evaluate functions which get parameters and must return some value:
    * bool - True / False simple way to verify fact  (by default Fact return True)
    * int / float - for purpose to use comp operator ( >, >=, <, <=, ==, != )
    * str - for Fuzzy

    You can use () operator to call evaluate the fact
    """


    def __init__(self, name: str, eval_function: Callable = None, probability: float = 1,
                 data: Callable = None):
        self.name = name
        self.probability = probability
        if self.data:
            self.data = data

        if eval_function:
            self.evaluate = eval_function


    def evaluate(self, *args, **kwargs) -> Union[str, int, float, bool]:
        """ Evaluate method -> for advance purpose overload this method """
        return True


    def data(self, *args, **kwargs) -> Union[Position, List[Position], None]:
        return None


    def __call__(self, *args, **kwargs):
        return self.evaluate(*args, **kwargs)


    def __hash__(self):
        return hash(self.name)


    def __deepcopy__(self, memodict={}):
        return Fact(self.name, self.evaluate, self.probability, self.data)


    def __eq__(self, other):
        return self.name == other


class DataHolderFact:
    def __init__(self, fact, arguments):
        self.fact = fact
        self.arguments = arguments
