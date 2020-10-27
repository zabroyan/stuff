from enum import Enum
from typing import Optional

from OrodaelTurrim.Structure.Enums import AutoNumber


class LogicalOperator(AutoNumber):
    """ Enu, """
    AND = ()
    OR = ()


    def __str__(self):
        return self.name


class Operator(Enum):
    """ Enum for language operators """
    EQUAL = '=='
    LESS_THEN = '<'
    MORE_THEN = '>'
    NOT_EQUAL = '!='
    LESS_EQUAL = '<='
    MORE_EQUAL = '>='
    ASSIGN = ':='


    @staticmethod
    def from_string(comparator_str: str) -> Optional["Operator"]:
        for cmp in Operator:
            if cmp.value == comparator_str:
                return cmp

        return None
