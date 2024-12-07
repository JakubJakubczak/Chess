from tkinter.constants import BOTTOM
from tkinter import *
from Const import *
from engine import *
import numpy as np
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
        self.history = [] # historia jest w formacie LAN
        self.result = None
        self.threefold_repetition = 0
        self.fifty_move_rule = 0
        self.white_queen_castling_right = True
        self.black_queen_castling_right = True
        self.white_king_castling_right = True
        self.black_king_castling_right = True
        self.score = 0

        # dodać o en_passant też pewnie
        move = None
        last_move = None
        promotion = False
        enpassant = None
        self.promotion_choice = None
        self.info = [self.white_queen_castling_right, self.white_king_castling_right, self.black_queen_castling_right,
                     self.black_king_castling_right,  last_move, move, promotion, enpassant, self.threefold_repetition,
                     self.fifty_move_rule, self.score]

        self.game = game
        self.frame = frame
        self.canvas_board = Canvas(self.frame, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.canvas_label1 = Canvas(self.frame, width=LABEL_VERTUCAL_WIDTH, height=LABEL_VERTICAL_HEIGHT)
        self.canvas_label2 = Canvas(self.frame, width=LABEL_VERTICAL_HEIGHT, height=LABEL_VERTUCAL_WIDTH)

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

        for rank in range(8):
            rank_label = Label(self.canvas_label1, text=str(8 - rank), font=("Arial", 12))
            letter_height = rank_label.winfo_height()
            letter_width = rank_label.winfo_width()
            rank_label.place(x=LABEL_VERTUCAL_WIDTH - 10 * letter_width, y= rank * SPACE_SIZE + SPACE_SIZE // 2 - 5 * letter_height) # - SPACE_SIZE // 2

        for file in range(8):
            file_label = Label(self.canvas_label2, text=chr(file + 97), font=("Arial", 12))  # 97 is ASCII for 'a'
            letter_width = file_label.winfo_width()
            file_label.place(x=file * SPACE_SIZE + SPACE_SIZE // 2 - 5 * letter_width, y = 0) # - SPACE_SIZE // 2

        self.canvas_label1.place(x=0, y=100)
        self.canvas_label2.place(x=50, y=700)



    def draw_game(self):
        self.result = -1 if self.white_turn else 1
        self.game_on = False

    def end_game(self):
        pass

    def choose_piece(self):
        popup = Toplevel(self.frame)
        popup.title("Promocja")
        popup.geometry("300x200")
        popup.transient(self.frame)  # Keeps it on top of the main window

        label = Label(popup, text="Wybierz figurę do promocji:")
        label.pack(pady=10)

        self.promotion_choice = None
        def set_piece(value):
            self.promotion_choice = value
            popup.destroy()

        # Buttons for each piece
        Button(popup, text="Hetman (Q)", command=lambda: set_piece(9)).pack(pady=5)
        Button(popup, text="Wieża (R)", command=lambda: set_piece(5)).pack(pady=5)
        Button(popup, text="Goniec (B)", command=lambda: set_piece(4)).pack(pady=5)
        Button(popup, text="Skoczek (N)", command=lambda: set_piece(3)).pack(pady=5)

        # Pause the program until the popup window is closed
        popup.wait_window()

        return self.promotion_choice
    def move_pgn(self, string):
        pass

    def change_move_to_LAN(self, x_start, y_start, x_end, y_end):
        move_lan = f"{chr(x_start + 97)}{8 - y_start}{chr(x_end + 97)}{8 - y_end}"

        return move_lan

    def change_move_to_SAN(self, x_start, y_start, x_end, y_end):
        pass
    def add_to_history(self,x_start, y_start, x_end, y_end):
        # is it castling
        # is it en passant
        # is it promotion
        # is it beating
        # is it only possible move
        move_lan = self.change_move_to_LAN(x_start, y_start, x_end, y_end)
        self.history.append(move_lan)

    def save_pgn(self, filename, metadata):
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
