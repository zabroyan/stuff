class OrodaelTurrimException(Exception):
    """ Base framework exception. All framework exception inherit from this exception """
    pass


class IllegalArgumentException(OrodaelTurrimException):
    """ Illegal argument passed to object initialization """
    pass


class IllegalActionException(OrodaelTurrimException):
    """ You try to use illegal action on the game engine """
    pass


class IllegalHistoryOperation(OrodaelTurrimException):
    """ Trying to do illegal operation when in Browsing mode """
    pass


class IllegalLogMessage(OrodaelTurrimException):
    """ You are trying to log message which is not correct type """
    pass


class IllegalConfigState(OrodaelTurrimException):
    """ Something missing in game config file """
    pass


class IllegalRulesFormat(OrodaelTurrimException):
    """ Problem with parsing rules file """
    pass


class BadActionBaseParameters(OrodaelTurrimException):
    """ ActionBase method has bad parameters """
    pass


class BadFactDataValue(OrodaelTurrimException):
    """ Fact contain bad value type """
    pass
