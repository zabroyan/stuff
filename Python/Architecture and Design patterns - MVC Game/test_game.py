from abstractfactory.GameObjectFactory_A import GameObjectFactory_A
from command.AbsCommand import CannonMoveUp, CannonAimUp, CannonShoot, ToggleShootingMode
from MVCGameConfig import MAX_X, MAX_Y
from model.GameModel import GameModel
from Position import Position, Rectangle
import pytest
from unittest.mock import MagicMock


def test_toggle():
    goFact = GameObjectFactory_A()
    cannon = goFact.createCannon(Position(100, 100))
    ogSM = cannon.shootingMode
    cannon.toggleShootingMode()
    assert cannon.shootingMode != ogSM
    cannon.toggleShootingMode()
    assert cannon.shootingMode == ogSM


def test_observer():
    model = GameModel()
    model.setGameArea(Rectangle(0, 0, MAX_X, MAX_Y))
    observer = MagicMock()
    model.registerObserver(observer)
    model.notifyObservers()
    assert observer.update.called == 1

    model.unregisterObserver(observer)
    model.notifyObservers()
    assert observer.update.called == 1


def test_shooting():
    goFact = GameObjectFactory_A()
    cannon = goFact.createCannon(Position(MAX_X, MAX_Y))
    missile = cannon.shoot(10)
    assert len(missile) == 1


def test_undo():
    model = GameModel()
    model.setGameArea(Rectangle(0, 0, MAX_X, MAX_Y))
    ogPos = model.cannon.getPosition()
    model.registerCommand(CannonMoveUp(model))
    model.timeTick()
    assert ogPos != model.cannon.getPosition()
    model.undoLastCommand()
    assert ogPos == model.cannon.getPosition()


def test_process():
    model = GameModel()
    model.setGameArea(Rectangle(0, 0, MAX_X, MAX_Y))
    ogAngle = model.cannon.angle

    model.registerCommand(CannonAimUp(model))
    model.registerCommand(CannonShoot(model))
    model.registerCommand(ToggleShootingMode(model))

    assert len(model.unprocessedCommands) == 3
    assert ogAngle == model.cannon.angle
    assert len(model.missiles) == 0
    assert model.cannon.shootingMode.name() == 'Single'
    assert model.cannon.shootingMode.damage == 10
    model.timeTick()
    assert len(model.unprocessedCommands) == 0
    assert ogAngle != model.cannon.angle
    assert len(model.missiles) > 0
    assert model.cannon.shootingMode.name() == 'Double'
    assert model.cannon.shootingMode.damage == 5
    assert len(model.processedCommands) == 3

