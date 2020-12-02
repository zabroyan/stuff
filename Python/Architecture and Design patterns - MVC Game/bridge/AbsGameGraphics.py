from abc import abstractmethod


class AbsGameGraphics:

    @abstractmethod
    def drawImage(self, image, position):
        pass

    @abstractmethod
    def drawText(self, text: str, position):
        pass

    @abstractmethod
    def drawLine(self, startPos, endPos):
        pass
