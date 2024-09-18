### jak zrobic wyswietlanie caly czas stanu jak i zmian
### w konstruktorze figury dodać boarda, po to, żeby init zrobić



class Figure:
    def __init__(self,color, positionX, positionY, image,canvas_image):
        self.color = color
        self.positionX = positionX
        self.positionY = positionY
        self.image = image
        self.canvas_image= canvas_image
    def canMove(self, toPosition):
        #if isEmpty(BOARD)
        pass

class Knight (Figure):
    def __init__(self, color, positionX, positionY, image, canvas_image):
        super().__init__(color, positionX, positionY, image, canvas_image)
    def canMove(self, toPosition):
        pass

class Pawn (Figure):
    def __init__(self,color, positionX, positionY, image, canvas_image):
        super().__init__(color, positionX, positionY, image, canvas_image)
    def canMove(self, toPosition):
        pass

class Bishop(Figure):
    def __init__(self, color, positionX, positionY, image, canvas_image):
        super().__init__(color, positionX, positionY, image, canvas_image)
    def canMove(self, toPosition):
        pass

class Queen (Figure):
    def __init__(self, color, positionX, positionY, image, canvas_image):
        super().__init__(color, positionX, positionY, image, canvas_image)
    def canMove(self, toPosition):
        pass

class King (Figure):
    def __init__(self, color, positionX, positionY, image, canvas_image):
        super().__init__(color, positionX, positionY, image, canvas_image)
    def canMove(self, toPosition):
        pass

class Rook (Figure):
    def __init__(self, color, positionX, positionY, image, canvas_image):
        super().__init__(color, positionX, positionY, image, canvas_image)
    def canMove(self, toPosition):
        pass