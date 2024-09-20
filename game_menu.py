from tkinter import *
from Const import *

class Game_menu:
    def __init__(self,frame):
        self.frame = frame
        self.canvas_game_menu_1= Canvas(self.frame, width=GAME_MENU_1WIDTH, height=GAME_MENU_1HEIGHT)
        self.canvas_game_menu_2 = Canvas(self.frame, width=GAME_MENU_2WIDTH, height=GAME_MENU_2HEIGHT)
        self.canvas_game_menu_1.place(x=0, y=0)
        self.canvas_game_menu_2.place(x=650, y=0)