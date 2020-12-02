from controller.GameController import GameController
from model.GameModel import GameModel
from visitor.GameObjectRender import GameObjectRender
from proxy.GameModelProxy import GameModelProxy


class GameView:
    def __init__(self, model: GameModel):
        self.model = model
        self.renderer = GameObjectRender()

    def setGameGraphics(self, graphics):
        self.graphics = graphics
        self.renderer.setGameGraphics(self.graphics)

    def render(self):
        self.model.getGameInfo().acceptVisitor(self.renderer)
        for go in self.model.getGameObjects():
            go.acceptVisitor(self.renderer)

    def makeController(self):
        return GameController(GameModelProxy(self.model))

    def paintEvent(self):
        self.render()
