from abstractfactory.GameObjectFactory_A import GameObjectFactory_A
from abstractfactory.GameObjectFactory_B import GameObjectFactory_B
from observer.IObservable import Observable
from observer.IObserver import Observer
from Position import Position
from MVCGameConfig import CANNON_POS_X, CANNON_POS_Y, GRAVITY, ENEMIES_CNT, TIME_TICK_PERIOD, MAX_X, MAX_Y
from model.IGameModel import IGameModel
from collections import deque
from random import randint
from command.AbsCommand import AbsCommand
from model.gameObjects.family_A.GameInfo_A import GameInfo_A
from model.gameObjects.family_B.GameInfo_B import GameInfo_B


class GameModel(Observable, IGameModel):
    def __init__(self):
        self.enemies = []
        self.missiles = []
        self.collisions = []
        self.observers = []
        self.goFact = GameObjectFactory_A()
        self.gofact_A = GameObjectFactory_A()
        self.goFact_B = GameObjectFactory_B()
        self.cannon = self.goFact.createCannon(Position(CANNON_POS_X, CANNON_POS_Y))
        self.unprocessedCommands = deque()
        self.processedCommands = deque()
        self.gravity = GRAVITY
        self.gameInfo = GameInfo_A(self.cannon.shootingMode.damage, self.cannon.angle, 'None', 0,
                                   self.cannon.shootingMode.name())
        self.gameInfo_A = self.gameInfo
        self.gameInfo_B = GameInfo_B(self.cannon.shootingMode.damage, self.cannon.angle, 'None', 0,
                                     self.cannon.shootingMode.name())
        self.enemiesCnt = ENEMIES_CNT
        self.generateEnemies(self.enemiesCnt)

    def getCannonPosition(self):
        return self.cannon.getPosition()

    def getCannon(self):
        return self.cannon

    def moveCannonUp(self):
        self.cannon.moveUp(self.isInside)
        self.notifyObservers()

    def moveCannonDown(self):
        self.cannon.moveDown(self.isInside)
        self.notifyObservers()

    def aimCannonUp(self):
        self.cannon.aimUp()
        self.gameInfo.setAngle(self.cannon.angle)
        self.notifyObservers()

    def aimCannonDown(self):
        self.cannon.aimDown()
        self.gameInfo.setAngle(self.cannon.angle)
        self.notifyObservers()

    def cannonShoot(self):
        missileBatch = self.cannon.shoot(self.gameInfo.getDamage())
        self.missiles.extend(missileBatch)
        self.notifyObservers()

    def increaseDamage(self):
        damage = self.gameInfo.getDamage()
        if self.gameInfo.getShootingMode() == 'Double':
            damage *= 2
        self.cannon.increaseDamage(damage + 5)
        self.gameInfo.setDamage(self.cannon.shootingMode.damage)

    def getGameObjects(self):
        return [self.cannon, *self.enemies, *self.missiles, *self.collisions]

    def toggleShootingMode(self):
        self.cannon.toggleShootingMode()
        self.gameInfo.setShootingMode(self.cannon.shootingMode.name())
        self.gameInfo.setDamage(self.cannon.shootingMode.damage)
        self.notifyObservers()

    def changeLanguage(self):
        if self.gameInfo == self.gameInfo_A:
            self.gameInfo_B.setAll(self.gameInfo.getAll())
            self.gameInfo = self.gameInfo_B
        else:
            self.gameInfo_A.setAll(self.gameInfo.getAll())
            self.gameInfo = self.gameInfo_A

    def timeTick(self):
        self.processCommands()
        self.moveMissiles()
        self.removeCollisions()
        self.checkCollisions()
        self.destroyMissiles()

        if not len(self.enemies):
            self.nextLevel()

        self.notifyObservers()

    def removeCollisions(self):
        for coll in self.collisions:
            if coll.getAge() > TIME_TICK_PERIOD * 3 / 1000:
                self.collisions.remove(coll)

    def checkCollisions(self):
        for m in self.missiles:
            self.checkEnemies(m)

    def checkEnemies(self, missile):
        for e in self.enemies:
            if e.getRect().intersects(missile.getRect()):
                self.missiles.remove(missile)
                self.collisions.append(self.goFact.createCollision(e.getPosition()))
                e.hitBy(missile)
                if e.isDead():
                    self.enemies.remove(e)
                    self.gameInfo.addScore(e.points)

    def destroyMissiles(self):
        for m in self.missiles:
            if not self.isInside(m):
                self.missiles.remove(m)

    def generateEnemies(self, enemiesCnt):
        offset = 100
        for _ in range(1, enemiesCnt + 1):
            x = randint(0 + offset, MAX_X - 3 * offset)
            y = randint(0 + offset, MAX_Y - offset)
            self.enemies.append(self.goFact.createEnemy(Position(x, y)))

    def moveMissiles(self):
        for m in self.missiles:
            m.moveMissile()

    def getGameInfo(self):
        return self.gameInfo

    def isInside(self, obj):
        return self.gameArea.contains(obj.getRect())

    def nextLevel(self):
        self.missiles.clear()
        self.collisions.clear()
        self.unprocessedCommands.clear()
        self.processedCommands.clear()
        self.enemiesCnt += 1
        level = self.gameInfo.getLevel()
        self.gameInfo.setLevel(level + 1)
        if not level % 2:
            self.goFact = self.gofact_A
            self.gameInfo.setGravity('None')
        else:
            self.goFact = self.goFact_B
            self.gameInfo.setGravity(self.gravity)
        self.cannon = self.goFact.createCannon(Position(CANNON_POS_X, CANNON_POS_Y))
        self.increaseDamage()
        self.gameInfo.setShootingMode(self.cannon.shootingMode.name())
        self.gameInfo.setDamage(self.cannon.shootingMode.damage)
        self.gameInfo.setAngle(0)
        self.generateEnemies(self.enemiesCnt)

    def registerObserver(self, obs: Observer):
        self.observers.append(obs)

    def unregisterObserver(self, obs: Observer):
        self.observers.remove(obs)

    def notifyObservers(self):
        for obs in self.observers:
            obs.update()

    def registerCommand(self, command: AbsCommand):
        self.unprocessedCommands.append(command)

    def processCommands(self):
        while self.unprocessedCommands:
            cmd = self.unprocessedCommands.popleft()
            memento = self.createMemento()
            cmd.doExecute()
            self.processedCommands.appendleft((cmd, memento))

    def undoLastCommand(self):
        if self.processedCommands:
            cmd, memento = self.processedCommands.popleft()
            cmd.doUnexecute(memento)
            self.notifyObservers()

    def createMemento(self):
        return self.Memento(self.cannon, self.gameInfo.getScore(), self.cannon.angle, self.enemies,
                            self.cannon.shootingMode,
                            self.gameInfo.getDamage(), self.gravity, self.gameInfo)

    def restoreMemento(self, memento):
        self.gameInfo = memento.gameInfo
        self.cannon.position = Position(memento.posx, memento.posy)
        self.gameInfo.setScore(memento.score)
        self.cannon.angle = memento.angle
        self.enemies = memento.enemies.copy()
        self.cannon.shootingMode = memento.shootingMode
        self.gameInfo.setShootingMode(self.cannon.shootingMode.name())
        self.gameInfo.setDamage(memento.damage)
        self.gravity = memento.gravity
        self.gameInfo.setGravity(self.gravity)
        self.gameInfo.setAngle(memento.angle)

    class Memento:
        def __init__(self, cannon, score, angle, enemies, sm, damage, gravity, gi):
            self.posx = cannon.position.x
            self.posy = cannon.position.y
            self.score = score
            self.angle = angle
            self.enemies = enemies.copy()
            self.shootingMode = sm
            self.damage = damage
            self.gravity = gravity
            self.gameInfo = gi
