from Const import *
from board import *
from figures import *
from game_menu import *
from tkinter import *
from tkinter import messagebox

class Game:
    def __init__(self):
        self.game_window = Tk()
        self.game_window.title("GAME")
        # self.game_window.geometry('850x750')
        self.game_window.resizable(False, False)
        self.frame = Frame(self.game_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.frame.pack()
        self.game_on = True
        self.white_turn = True
        self.game_menu = Game_menu(self.frame)
        self.board = Board(self.frame)
        self.figures = Figures(self.board)
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

