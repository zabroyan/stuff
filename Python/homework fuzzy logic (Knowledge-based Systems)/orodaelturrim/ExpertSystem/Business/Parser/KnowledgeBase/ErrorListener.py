import sys
import antlr4
from PyQt5.QtCore import QObject
from antlr4.error.ErrorListener import ErrorListener

from OrodaelTurrim.Presenter.Connector import Connector
from OrodaelTurrim.Structure.Exceptions import IllegalRulesFormat


class CustomErrorListener(ErrorListener, QObject):
    """ Custom error listener for Antlr4. Emiting signals for UI """


    def syntaxError(self, recognizer, offending_symbol, line: int, column: int, msg: str, e: Exception):
        """ Syntax error in the rules """

        error_msg = 'Error: Problem with parsing rules: {} at line {} column {}. Rules not parsed!\n'.format(msg, line,
                                                                                                             column)

        sys.stderr.write(error_msg)

        ui_error = 'Problem with parsing rules:\n\n{} at line {} column {}.\n\nRules not parsed!\n'.format(msg,
                                                                                                           line,
                                                                                                           column)
        Connector().emit('error_message', 'Rule parser', ui_error)

        raise IllegalRulesFormat


    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        sys.stderr.write('Problem with parsing rules!')
