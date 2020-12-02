from model.gameObjects.AbsGameInfo import AbsGameInfo


class GameInfo_A(AbsGameInfo):
    def getNames(self):
        return ['Shooting mode', 'Damage', 'Angle', 'Gravity', 'Score', 'Level']
