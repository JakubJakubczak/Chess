from tkinter import *
class Menu:
    def __init__(self):
        display_menu()

    def display_menu(self):
        global menu_window
        menu_window = Tk()
        menu_window.title("Chess")
        menu_window.resizable(False, False)

        global canvas_menu
        canvas_menu = Canvas(menu_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        canvas_menu.pack()

        background_photo = PhotoImage(file='tlo2.png')
        background = canvas_menu.create_image(0, 0, image=background_photo, anchor=NW)
        canvas_menu.coords(background, 0, 100)

        image_size = canvas_menu.bbox(background)
        end_of_backgroundY = image_size[3]

        game_Name = "CHESS GAME"
        font_size = 25
        game_label = canvas_menu.create_text(GAME_WIDTH / 2, 0 + font_size, text=game_Name, font=("Roboto:", font_size),
                                        fill="green")

        button1 = Button(menu_window, text="Start the game",
                         font=("Roboto"),
                         command=start,
                         fg="#00FF00",
                         bg="black",
                         borderwidth=5,
                         relief="raised")
        button2 = Button(menu_window, text="Exit",
                         font=("Roboto"),
                         command=exit,
                         fg="#00FF00",
                         bg="black", )
        button1.pack()
        button2.pack()
        menu_window.update()

        width_button1 = button1.winfo_width()
        height_button1 = button1.winfo_height()
        width_button2 = button2.winfo_width()

        end_of_button1Y = end_of_backgroundY + height_button1

        start_of_button2Y = end_of_button1Y + 5

        button1.place(x=(GAME_WIDTH - width_button1) / 2,
                      y=end_of_backgroundY)  # Adjust the coordinates (x, y) as needed
        button2.place(x=(GAME_WIDTH - width_button2) / 2,
                      y=start_of_button2Y)  # Adjust the coordinates (x, y) as needed

        menu_window.mainloop()

    def start(self):
        global menu_window
        menu_window.destroy()
        game = Game()

        # global canvas_game
        # canvas_game = canvas_game(game_window, width=GAME_WIDTH, height=GAME_HEIGHT)
        # drawBoard(game_window, canvas_game)
        # loadFigures(canvas_game)
        # drawFigures()

    def setup(self):
        pass

    def exit(self):
        global menu_window
        menu_window.destroy()