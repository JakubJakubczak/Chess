from tkinter import *
import Const
from Const import *
from game import *
from PIL import Image, ImageTk
class Menu_own:
    def __init__(self):
        self.menu_window = Tk()
        self.background_photo = None
        self.display_menu()
        self.menu_window.mainloop()

    def display_menu(self):
        self.menu_window.title("Chess")
        self.menu_window.resizable(False, False)

        canvas_menu = Canvas(self.menu_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        canvas_menu.pack()

        self.background_photo = ImageTk.PhotoImage(Image.open(f"images/tlo2.png"))
        background = canvas_menu.create_image(0, 0, image=self.background_photo, anchor=NW)
        canvas_menu.coords(background, 0, 100)

        image_size = canvas_menu.bbox(background)
        end_of_backgroundY = image_size[3]

        game_Name = "SZACHY"
        font_size = 25
        game_label = canvas_menu.create_text(GAME_WIDTH / 2, 0 + font_size, text=game_Name, font=("Roboto:", font_size),
                                        fill="green")

        button1 = Button(self.menu_window, text="Nowa gra",
                         font=("Roboto"),
                         command=self.start,
                         fg="#00FF00",
                         bg="black",
                         borderwidth=5,
                         relief="raised")

        button3 = Button(self.menu_window, text="Zagraj z komputerem",
                         font=("Roboto"),
                         command=self.start_ai,
                         fg="#00FF00",
                         bg="black",
                         borderwidth=5,
                         relief="raised")

        button2 = Button(self.menu_window, text="Wyjscie",
                         font=("Roboto"),
                         command=self.exit,
                         fg="#00FF00",
                         bg="black", )
        button1.place(x=0, y=0)
        button2.place(x=0, y=0)
        button3.place(x=0, y=0)
        self.menu_window.update_idletasks()

        width_button1 = button1.winfo_width()
        height_button1 = button1.winfo_height()
        height_button2 = button2.winfo_height()
        width_button2 = button2.winfo_width()
        width_button3 = button3.winfo_width()

        end_of_button1Y = end_of_backgroundY + height_button1
        end_of_button2Y = end_of_backgroundY + 2 * height_button1
        start_of_button3Y = end_of_backgroundY + 3 * height_button1 + 10

        start_of_button2Y = end_of_button1Y + 5

        end_of_button2Y = start_of_button2Y + height_button2

        start_of_button3Y = end_of_button2Y + 10

        button1.place(x=(GAME_WIDTH - width_button1) // 2, y=end_of_backgroundY)
        button3.place(x=(GAME_WIDTH - width_button3) // 2, y=start_of_button2Y)
        button2.place(x=(GAME_WIDTH - width_button2) // 2, y=start_of_button3Y)


    def start(self):
        self.menu_window.destroy()
        Const.settings["AI"] = False
        game = Game(self.back_to_menu)

    def start_ai(self):
        self.menu_window.destroy()
        Const.settings["AI"] = True
        game = Game(self.back_to_menu)

    def setup(self):
        pass

    def exit(self):
        self.menu_window.destroy()

    def back_to_menu(self):
        menu = Menu_own()