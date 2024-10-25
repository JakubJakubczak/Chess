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
        self.white_queen_castling_right = True
        self.black_queen_castling_right = True
        self.white_king_castling_right = True
        self.black_king_castling_right = True

        # dodać o en_passant też pewnie
        move = None
        last_move = None
        self.info = [self.white_queen_castling_right, self.white_king_castling_right, self.black_queen_castling_right, self.black_king_castling_right,  last_move, move]

        self.game = game
        self.frame = frame
        self.canvas_board = Canvas(self.frame, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.canvas_label1 = Canvas(self.frame, width=LABEL_VERTUCAL_WIDTH, height=LABEL_VERTICAL_HEIGHT)
        self.canvas_label2 = Canvas(self.frame, width=LABEL_VERTICAL_HEIGHT, height=LABEL_VERTUCAL_WIDTH)
        self.canvas_label1.create_text(20, 20, text="1", font=("Arial", 16), fill="black")
        self.canvas_label2.create_text(20, 20, text="1", font=("Arial", 16), fill="black")

        self.squares = [[None for _ in range(SIZE)] for _ in range(SIZE)]
        self.squares_highlighted = [[None for _ in range(SIZE)] for _ in range(SIZE)]

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


        self.engine = Engine(self.board, self.info)

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
                item = self.canvas_board.create_rectangle(x1,
                                        y1,
                                        x2,
                                        y2,
                                        fill=color)
                self.squares[row][col] = item

        self.canvas_board.place(x=50, y=100)
        # iterujemy po boardzie, jeśli miejsce = 0 to pass, a jesli nie to wyswietlamy figurę
    def display_labels(self):
        self.canvas_label1.place(x=0, y=100)
        self.canvas_label2.place(x=50, y=700)

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
        # Check the game state in the Board class and inform the Game class
        if not self.is_Game_On():
            self.game.handle_game_end()

    def change_color_of_square(self,x,y, color):
        item = self.squares[y][x]
        self.canvas_board.itemconfig(item, fill=color)

    def highlight_valid_moves(self, valid_moves):
        for move in valid_moves:
            x = move[2]
            y = move[3]
            self.change_color_of_square(x,y, "red")
            self.squares_highlighted[y][x] = True
        pass

    def dehighlight_valid_moves(self):
        for row in range(SIZE):
            for col in range(SIZE):
                if self.squares_highlighted[row][col]:
                    self.change_color_of_square(col, row, SQUARES_COLORS[(row + col )% 2])
                    self.squares_highlighted[row][col] = False
        pass

    def highlight_move(self):
        move = self.info[5]

        if move != None:
            self.change_color_of_square(move[0], move[1], "blue")
            self.change_color_of_square(move[2], move[3], "yellow")
        pass

    def dehighlight_last_move(self):
        last_move = self.info[4]

        if last_move != None:
            self.change_color_of_square(last_move[0], last_move[1], SQUARES_COLORS[(last_move[0] + last_move[1] )% 2])
            self.change_color_of_square(last_move[2], last_move[3], SQUARES_COLORS[(last_move[2] + last_move[3])% 2])
        pass
