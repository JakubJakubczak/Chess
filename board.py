from tkinter.constants import BOTTOM
from tkinter import *
from Const import *
from Const import *
###############
## NOTATION ##
## QUEEN - 9
## ROOK - 5
## BISHOP - 4
## KNIGHT - 3
## KING - 2
## PAWN - 1

class Board:
    def __init__(self, frame):
        self.frame = frame
        self.canvas_board = Canvas(self.frame, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.canvas_label1 = Canvas(self.frame, width=LABEL_VERTUCAL_WIDTH, height=LABEL_VERTICAL_HEIGHT)
        self.canvas_label2 = Canvas(self.frame, width=LABEL_VERTICAL_HEIGHT, height=LABEL_VERTUCAL_WIDTH)
        self.canvas_label1.create_text(20, 20, text="1", font=("Arial", 16), fill="black")
        self.canvas_label2.create_text(20, 20, text="1", font=("Arial", 16), fill="black")

        self.display_board()
        self.display_labels()

        self.board = [
            [-5, -3, -4, -9, -2, -4, -3, -5],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [5, 3, 4, 9, 2, 4, 3, 5]
        ]

    def display_board(self):
        for row in range(0, SIZE):
            y1 = row * SPACE_SIZE
            y2 = y1 + SPACE_SIZE
            for col in range(0, SIZE):
                if((row + col) %2 == 0):
                    color = SQUARES_COLORS[0]
                else:
                    color = SQUARES_COLORS[1]
                x1 = col * SPACE_SIZE
                x2 = x1 + SPACE_SIZE
                self.canvas_board.create_rectangle(x1,
                                        y1,
                                        x2,
                                        y2,
                                        fill=color)

        self.canvas_board.place(x=50, y=100)
        # iterujemy po boardzie, jeśli miejsce = 0 to pass, a jesli nie to wyswietlamy figurę
    def display_labels(self):
        self.canvas_label1.place(x=0, y=100)
        self.canvas_label2.place(x=50, y=700)

    def move(self, start, end):
        # check if the move is valid
        # if valid, make the move
        # if not valid, raise an error
        pass

    def pawn_promotion(self, pawn, new_piece):
        pass

    def castling(self):
        pass