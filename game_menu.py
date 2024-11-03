from tkinter import *
from Const import *

class Game_menu:
    def __init__(self,frame, game):
        self.frame = frame
        self.game = game

        self.canvas_game_menu_1= Canvas(self.frame, width=GAME_MENU_1WIDTH, height=GAME_MENU_1HEIGHT)
        self.canvas_game_menu_2 = Canvas(self.frame, width=GAME_MENU_2WIDTH, height=GAME_MENU_2HEIGHT)
        self.canvas_game_menu_1.place(x=0, y=0)
        self.canvas_game_menu_2.place(x=650, y=0)

        self.move_history_text = Text(self.canvas_game_menu_2, width=20, height=20, wrap="word")
        self.move_history_text.tag_configure("center", justify="center")
        self.move_history_text.pack(padx=10, pady=10)
        self.move_history_text.config(state=DISABLED)

    def update_move_history(self, history):
        self.move_history_text.config(state=NORMAL)  # Allow editing
        self.move_history_text.delete(1.0, END)  # Clear current text
        # Display moves, two moves per line with numbering
        formatted_moves = ""
        for i, move in enumerate(history):
            if i % 2 == 0:
                formatted_moves += f"{(i // 2) + 1}. "  # Move number for each new turn
            formatted_moves += f"{move} "
        self.move_history_text.insert(END, formatted_moves.strip())  # Insert updated moves
        self.move_history_text.tag_add("center", 1.0, END)
        self.move_history_text.config(state=DISABLED)