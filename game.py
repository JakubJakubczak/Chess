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
        self.game_window.resizable(False, False)
        self.frame = Frame(self.game_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        self.frame.pack()
        self.board = Board(self.frame, self)
        self.game_menu = Game_menu(self.frame, self)
        self.figures = Figures(self.board)
        self.game_window.mainloop()

    def handle_game_end(self):
        print("Game ended")
        result = self.board.get_result()
        # Handle game over logic here as before (message box or print)
        from tkinter import messagebox
        messagebox.showinfo("Game Over", f"Game Over: {result}")

    def update(self):
        self.game_menu.update_move_history(self.board.history)
