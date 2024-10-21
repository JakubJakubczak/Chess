from tkinter.constants import BOTTOM
from tkinter import *
from Const import *
from engine import *
###############
## NOTATION ##
## QUEEN - 9
## ROOK - 5
## BISHOP - 4
## KNIGHT - 3
## KING - 2
## PAWN - 1

class Board:
    def __init__(self, frame, game):
        self.game_on = True
        self.white_turn = True
        self.history = [] # historia jest w formacie PGN
        self.result = None
        self.threefold_repetition = 0
        self.fifty_move_rule = 0

        self.info = []

        self.game = game
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
        self.engine = Engine(self.board)

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

    # przemieszczanie tylko w tablicy, grafika zostaje
    def move(self, start_x, start_y, end_x, end_y):
        # srpawdzic czy to moze roszada albo promocja pionka
        piece = self.board[start_y][start_x]
        if piece!= 0:
            self.board[end_y][end_x] = piece
            self.board[start_y][start_x] = 0

        self.check_game_state()

    def castling(self, color):
        pass

    def pawn_promotion(self, x_start, y_start, x_end, y_end):
        pass

    def move_pgn(self, string):
        pass

    def add_to_history(self,x_start, y_start, x_end, y_end):
        # is it castling
        # is it en passant
        # is it promotion
        # is it beating
        # is it only possible move
        pass


    def is_Game_On(self):
        print("is_game_on")
        if self.engine.game_over() == None:
            return True

        else:
            self.game_on = False
            self.result = self.engine.game_over()
            return False


    def is_white_turn(self):
        if self.white_turn:
            return True
        else:
            return False

    def get_result(self):
        return self.result  # Return the result (could be checkmate, stalemate, etc.)

    def check_game_state(self):
        print("check_game_state")
        # Check the game state in the Board class and inform the Game class
        if not self.is_Game_On():
            self.game.handle_game_end()