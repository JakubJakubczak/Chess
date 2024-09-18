from Const import *
from tkinter import *
from tkinter import messagebox

class Game:
    def __init__(self):
        self.game_window = Tk()
        game_window.title("GAME")
        game_window.resizable(False, False)
        self.canvas = Canvas(game_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.game_on = True
        self.white_turn = True
        self.board = Board(canvas)
        self.figures = Figures(canvas)
        self.game_menu = Game_Menu()
        self.game_window.mainloop()

    def is_Game_On(self):
        if self.game_on:
            return True
        else:
            return False
    def is_white_turn(self):
        if self.white_turn:
            return True
        else:
            return False

    ### Later for time management
    def start_Game(self):
        pass

    def display_Game(self):
        ## display board
        ## display figures
        ## display game_menu
        pass

