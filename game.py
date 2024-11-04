from Const import *
from board import *
from figures import *
from game_menu import *
from tkinter import *
from ai import *
from tkinter import messagebox
from Const import *

class Game:
    def __init__(self):
        self.game_window = Tk()
        self.game_window.title("GAME")
        self.game_window.resizable(False, False)
        self.frame = Frame(self.game_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.frame.pack()
        self.board = Board(self.frame, self)
        self.game_menu = Game_menu(self.frame, self)
        self.figures = Figures(self.board, self)
        self.ai = Ai(self.board)
        self.game_window.mainloop()

        if settings["AI"] == True and settings["TURN"] == False:
           random_move =  self.ai.generate_random_move(not settings["TURN"] )
           self.move(None, random_move[0], random_move[1], random_move[2], random_move[3])
    def handle_game_end(self):
        print("Game ended")
        result = self.board.get_result()
        # Handle game over logic here as before (message box or print)
        from tkinter import messagebox
        messagebox.showinfo("Game Over", f"Game Over: {result}")

    def update(self):
        if settings["AI"] and self.board.white_turn != settings["TURN"]:
            random_move = self.ai.generate_random_move(not settings["TURN"])
            self.move(None, random_move[0], random_move[1], random_move[2], random_move[3])
        self.game_menu.update_move_history(self.board.history)

    def move(self, drag_data, x_start, y_start, x_end, y_end):
        self.board.white_turn = not self.board.white_turn
        self.board.engine.move_board(x_start, y_start, x_end, y_end)
        if self.board.engine.is_pawn_promotion(x_end, y_end, x_end, y_end):
            print("promotion")
            value = self.board.choose_piece()
            print(f"value {value}")
            self.board.engine.promote(x_end, y_end, value)
        self.figures.move_images(drag_data, x_start, y_start, x_end, y_end)
        self.board.game.update()
        self.board.check_game_state()

        self.board.add_to_history(x_start, y_start, x_end, y_end)

        # print(f"move {self.board.info[5]}")
        self.board.dehighlight_valid_moves()
        self.board.dehighlight_last_move()
        self.board.highlight_move()

        print(f"AI {settings["AI"]}")
