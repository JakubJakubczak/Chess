### jak zrobic wyswietlanie caly czas stanu jak i zmian
### w konstruktorze figury dodać boarda, po to, żeby init zrobić
### poprawic boarda z przekazywania funkcją na po prostu sel.board
############ JAK DOBRZE WGRAC IMAGES
############## PRZEKAZAC INFORMACJE O BIERCE I POZYCJI W DRAG
### DODAC CANVAS JAKO ZMIENNA KLASY
## TE BOARDY LEPIEJ ZROBIC W FUNKCJACH, BEZ SENSU JE PRZEKAZYWAC ARGUMENTEM


###########################
##### TRZEBA PRZECHOWYWAC PHOTO IMAGE BO INACZEJ GARBAGE COLLECTOR USUNIE JE
##########################
from tkinter import *
from PIL import Image, ImageTk
from Const import *
from dragger import *

class Figures:
    def __init__(self, board):
       self.board = board
       self.images = [[None for _ in range(SIZE)] for _ in range(SIZE)]
       self.canvas_images = [[None for _ in range(SIZE)] for _ in range(SIZE)]
       self.images = self.load_canvas_images(board.board) # list
       image_dimensions = self.calculate_image_dimensions(self.images[0][0]) ## imgaes[0][0] because all images are the same size
       first_cordinates = self.calculate_first_cordinates()
       self.display_figures(first_cordinates, board.canvas_board, board.board) # list
       self.bind_figures(board.canvas_board)

    def load_canvas_images(self, board):
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] != 0:
                    piece = board[i][j]
                    image = ImageTk.PhotoImage(Image.open(f"images/{piece}.png"))
                    self.images[i][j] = image
        return self.images

    def move_images(self, drag_data, x_start, y_start, x_end, y_end):
        if self.board.engine.is_it_capture(x_end, y_end):
            item_del = self.canvas_images[y_end][x_end]
            self.board.canvas_board.delete(item_del)

        ## castling to do

        ## centrowanie figury po przeniesieniu

        figure_coords_x, figure_coords_y = self.calculate_first_cordinates()

        center_coords_x = figure_coords_x + (x_end * SPACE_SIZE)
        center_coords_y = figure_coords_y + (y_end * SPACE_SIZE)

        delta_center_x = drag_data["x"] - center_coords_x
        delta_center_y = drag_data["y"] - center_coords_y

        item = self.canvas_images[y_start][x_start]
        self.board.canvas_board.move(item, -delta_center_x, -delta_center_y)
        self.canvas_images[y_start][x_start] = None
        self.canvas_images[y_end][x_end] = item

    def calculate_image_dimensions(self, image):
        return [image.width(),image.height()]

    def calculate_first_cordinates(self):
        figure_coords_x = SPACE_SIZE/2
        figure_coords_y = SPACE_SIZE/2
        return [figure_coords_x, figure_coords_y]

    def display_figures(self, first_cordinates, canvas, board):
        ##### dict that will store position and figure
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] != 0:
                    self.canvas_images[i][j] = canvas.create_image(first_cordinates[0] + (j * SPACE_SIZE), first_cordinates[1] + (i * SPACE_SIZE), image=self.images[i][j])
                    # Bring piece image to the top to ensure it is above the board
                    canvas.tag_raise(self.canvas_images[i][j])

        return self.canvas_images

    def bind_figures(self, canvas):
        dragger = Dragger(self, canvas, self.board)
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board.board[i][j] != 0:

                    # Add a specific tag to all piece images
                    canvas.addtag_withtag("piece", self.canvas_images[i][j])

                    canvas.tag_bind(self.canvas_images[i][j],  "<ButtonPress-1>", dragger.drag_start) ######## DO IT
                    canvas.tag_bind(self.canvas_images[i][j],  "<B1-Motion>", dragger.drag_motion)
                    canvas.tag_bind(self.canvas_images[i][j], "<ButtonRelease-1>", dragger.drag_stop)

