from abc import ABC, abstractmethod


class AbsCommand(ABC):

    def __init__(self, receiver):
        self.receiver = receiver

    def doExecute(self):
        self._execute()

    @abstractmethod
    def _execute(self):
        pass

    def doUnexecute(self, memento):
        if memento:
            self.receiver.restoreMemento(memento)

    @abstractmethod
    def name(self):
        pass


class CannonMoveUp(AbsCommand):

    def _execute(self):
        self.receiver.moveCannonUp()

    def name(self):
        return "CannonMoveUp"


class CannonMoveDown(AbsCommand):

    def _execute(self):
        self.receiver.moveCannonDown()

    def name(self):
        return "CannonMoveDown"


class CannonShoot(AbsCommand):

    def _execute(self):
        self.receiver.cannonShoot()

    def name(self):
        return "CannonShoot"


class CannonAimUp(AbsCommand):

    def _execute(self):
        self.receiver.aimCannonUp()

    def name(self):
        return "CannonAimUp"


class CannonAimDown(AbsCommand):

    def _execute(self):
        self.receiver.aimCannonDown()

    def name(self):
        return "CannonAimDown"


class ToggleShootingMode(AbsCommand):

    def _execute(self):
        self.receiver.toggleShootingMode()

    def name(self):
        return "ToggleShootingMode"


class ChangeLanguage(AbsCommand):

    def _execute(self):
        self.receiver.changeLanguage()

    def name(self):
        return "ChangeLanguage"
