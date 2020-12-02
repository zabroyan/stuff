from model.gameObjects.AbsGameInfo import AbsGameInfo


class GameInfo_B(AbsGameInfo):
    def getNames(self):
        return ['Režim střelby', 'Poškození', 'Úhel', 'Gravitace', 'Skóre', 'Úroveň']
