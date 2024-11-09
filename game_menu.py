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

        button1 = Button(self.canvas_game_menu_2, text="Poddaj się",
                         font=("Roboto"),
                         command=self.game.surrender,
                         fg="#00FF00",
                         bg="black",
                         borderwidth=5,
                         relief="raised")

        button2 = Button(self.canvas_game_menu_2, text="Wróc do menu",
                         font=("Roboto"),
                         command=self.game.back_to_menu,
                         fg="#00FF00",
                         bg="black",
                         borderwidth=5,
                         relief="raised")

        width_button1 = button1.winfo_width()
        height_button1 = button1.winfo_height()
        width_button2 = button2.winfo_width()
        height_button2 = button2.winfo_height()

        pady = 30

        button1.place(x=(GAME_MENU_2WIDTH - width_button1) / 2,
                      y=GAME_MENU_2HEIGHT // 2 - height_button1 )  # Adjust the coordinates (x, y) as needed

        button2.place(x=(GAME_MENU_2WIDTH - width_button2) / 2,
                      y=GAME_MENU_2HEIGHT // 2 + pady)  # Adjust the coordinates (x, y) as needed

        self.move_history_text = Text(self.canvas_game_menu_2, width=20, height=20, wrap="word")
        self.move_history_text.tag_configure("center", justify="center")
        self.move_history_text.place(x=10, y=10, width=GAME_MENU_2WIDTH - 20, height= GAME_MENU_2HEIGHT // 2)
        self.move_history_text.config(state=DISABLED)
    def display_history(self, history):
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


    def display_result(self, result):
        text = None
        if result == 0:
            text = "REMIS"

        if result == 1:
            text = "WYGRANA BIAŁYCH"

        if result == -1:
            text = "WYGRANA CZARNYCH"

        result_label = Label(self.canvas_game_menu_1, text=text, font=("Arial", 24), fg = "red")
        result_label.pack(padx=100)

    def display_score(self, score):
        pass