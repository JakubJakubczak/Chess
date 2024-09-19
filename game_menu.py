from tkinter import *
from Const import *

class Game_menu:
    def __init__(self,frame):
        self.frame = frame
        self.canvas_game_menu_1= Canvas(self.frame, width=GAME_MENU_1WIDTH, height=GAME_MENU_1HEIGHT)
        self.canvas_game_menu_2 = Canvas(self.frame, width=GAME_MENU_2WIDTH, height=GAME_MENU_2HEIGHT)

        self.canvas_game_menu_1.create_text(0, 0, text="Game Menu1", font=("Arial", 16), fill="black")
        self.canvas_game_menu_2.create_text(0, 0, text="Game Menu2", font=("Arial", 16), fill="black")
        self.canvas_game_menu_1.pack(side=TOP, anchor=NW)
        self.canvas_game_menu_2.pack(side=TOP, anchor=NE)