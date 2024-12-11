from tkinter import *
from Const import *
from PIL import Image, ImageTk

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

        pady = 50

        button1.place(x=(GAME_MENU_2WIDTH) // 2 - width_button1 * 100,
                      y=GAME_MENU_2HEIGHT // 2 + 15 * height_button1 )

        button2.place(x=(GAME_MENU_2WIDTH) / 2 - width_button2 * 100,
                      y=GAME_MENU_2HEIGHT // 2 + 15 * ( height_button1 + height_button2) + pady)

        self.move_history_text = Text(self.canvas_game_menu_2, width=20, height=20, wrap="word")
        self.move_history_text.tag_configure("center", justify="center")
        self.move_history_text.place(x=10, y=10, width=GAME_MENU_2WIDTH - 20, height= GAME_MENU_2HEIGHT // 2)
        self.move_history_text.config(state=DISABLED)

        self.white_pieces = 0
        self.black_pieces = 0
        self.images = []

        self.evaluation_label = None
        self.score_of_game = None
    def display_history(self, history):
        self.move_history_text.config(state=NORMAL)
        self.move_history_text.delete(1.0, END)

        formatted_moves = ""
        for i, move in enumerate(history):
            if i % 2 == 0:
                formatted_moves += f"{(i // 2) + 1}. "
            formatted_moves += f"{move} "
        self.move_history_text.insert(END, formatted_moves.strip())
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
        result_label.place(x = 250, y = 19)

    def display_score(self, score):
        padx = 30
        pady = 0

        y = SMALL_PIECE_SIZE + (pady)
        x = padx

        if self.score_of_game is not None:
            self.score_of_game.destroy()

        self.score_of_game = Label(self.canvas_game_menu_1, text=f"Punkty: {score}", font=("Arial", 20), fg = "blue")
        self.score_of_game.place(x = x, y = y)

    def display_eval(self, eval):
        y = 600
        x = 70

        if self.evaluation_label is not None:
            self.evaluation_label.destroy()

        self.evaluation_label = Label(self.canvas_game_menu_2, text=f"Ocena: {eval}", font=("Arial", 20), fg="blue")
        self.evaluation_label.place(x=x, y=y)

    def add_piece_to_player(self, for_white, tags):
        start_coords = (int(tags[0]), int(tags[1]))
        pady = 10
        padx = 30
        y = GAME_MENU_1HEIGHT - pady

        if not for_white:
            x = SMALL_PIECE_SIZE * self.black_pieces + padx
            self.black_pieces += 1

        if for_white:
            x = GAME_MENU_1WIDTH - SMALL_PIECE_SIZE * self.white_pieces - padx
            self.white_pieces += 1

        piece = self.start_coordinates_to_figure(start_coords)

        image = ImageTk.PhotoImage(Image.open(f"images/small/{piece}.png"))
        self.images.append(image)
        self.canvas_game_menu_1.create_image(x, y, image=image)

    def start_coordinates_to_figure(self, coord):
        if coord[1] == 1:
            piece_value = -1
            return piece_value
        elif coord[1] == 6:
            piece_value = 1
            return piece_value

        if coord[1] == 0 or coord[1] == 7:
            abs_value = None
            if coord[0] == 0 or coord[0] == 7:
                abs_value = 5
            if coord[0] == 1 or coord[0] == 6:
                abs_value = 3
            if coord[0] == 2 or coord[0] == 5:
                abs_value = 4
            if coord[0] == 3:
                abs_value = 9
            if coord[0] == 4:
                abs_value = 2

            color = -1 if coord[1] == 0 else 1

            return abs_value * color

