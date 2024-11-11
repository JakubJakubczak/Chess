from Const import *
from board import *
from figures import *
from game_menu import *
from tkinter import *
from ai import *
from tkinter import messagebox
from Const import *
from menu import *


class Game:
    def __init__(self, back_to_menu_callback):
        self.back_to_menu_callback = back_to_menu_callback
        self.game_window = Tk()
        self.game_window.title("GAME")
        self.game_window.resizable(False, False)
        self.frame = Frame(self.game_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.frame.pack()
        self.board = Board(self.frame, self)
        self.game_menu = Game_menu(self.frame, self)
        self.figures = Figures(self.board, self)
        self.ai = Ai(self.board)
        self.game_menu.display_score(self.board.score)
        eval = self.ai.evaluate()
        self.game_menu.display_eval(eval)
        self.game_window.mainloop()

        if settings["AI"] == True and settings["TURN"] == False:
           random_move =  self.ai.generate_random_move(not settings["TURN"] )
           self.move(None, random_move[0], random_move[1], random_move[2], random_move[3])
    def handle_game_end(self):
        print("Game ended")
        result = self.board.get_result()
        # Handle game over logic here as before (message box or print)
        # from tkinter import messagebox
        # messagebox.showinfo("Game Over", f"Game Over: {result}")
        self.game_menu.display_result(result)

    def update(self):
        if settings["AI"] and self.board.white_turn != settings["TURN"] and self.board.game_on:
            random_move = self.ai.generate_random_move(not settings["TURN"])
            self.move(None, random_move[0], random_move[1], random_move[2], random_move[3])



    def move(self, drag_data, x_start, y_start, x_end, y_end):
        self.board.white_turn = not self.board.white_turn
        self.board.engine.move_board(x_start, y_start, x_end, y_end)
        if self.board.engine.is_pawn_promotion(x_end, y_end, x_end, y_end):
            print("promotion")
            value = self.board.choose_piece()
            print(f"value {value}")
            self.board.engine.promote(x_end, y_end, value)
        self.figures.move_images(drag_data, x_start, y_start, x_end, y_end)
        self.board.check_game_state()

        self.board.add_to_history(x_start, y_start, x_end, y_end)
        self.game_menu.display_history(self.board.history)
        self.game_menu.display_score(self.board.info[10])
        eval = self.ai.evaluate()
        self.game_menu.display_eval(eval)


        # print(f"move {self.board.info[5]}")
        self.board.dehighlight_valid_moves()
        self.board.dehighlight_last_move()
        self.board.highlight_move()

        self.board.game.update()



    def surrender(self):
        self.board.result = -1 if self.board.white_turn else 1
        self.board.game_on = False
        self.handle_game_end()

    def back_to_menu(self):
        self.game_window.destroy()
        self.back_to_menu_callback()

