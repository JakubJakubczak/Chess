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
       self.images = self.load_canvas_images(board.board) # list
       image_dimensions = self.calculate_image_dimensions(self.images[0][0]) ## imgaes[0][0] because all images are the same size
       first_cordinates = self.calculate_first_cordinates(image_dimensions)
       canvas_images = self.display_figures(first_cordinates, board.canvas_board, board.board) # list
       self.bind_figures(board.canvas_board, canvas_images)

    def load_canvas_images(self, board):
        number_of_images = 12
        numbers_of_pieces = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 9, -9]
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] != 0:
                    piece = board[i][j]
                    image = ImageTk.PhotoImage(Image.open(f"images/{piece}.png"))
                    self.images[i][j] = image
        return self.images


    def calculate_image_dimensions(self, image):
        return [image.width(),image.height()]

    def calculate_first_cordinates(self, image_dimensions):
        figure_coords_x = SPACE_SIZE/2
        figure_coords_y = SPACE_SIZE/2
        return [figure_coords_x, figure_coords_y]

    def display_figures(self, first_cordinates, canvas, board):
        canvas_images = []
        ##### dict that will store position and figure
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] != 0:
                    canvas_image = canvas.create_image(first_cordinates[0] + (j * SPACE_SIZE), first_cordinates[1] + (i * SPACE_SIZE), image=self.images[i][j])
                    canvas_images.append(canvas_image)
                    # Bring piece image to the top to ensure it is above the board
                    canvas.tag_raise(canvas_image)
        return canvas_images

    def bind_figures(self, canvas, canvas_images):
        dragger = Dragger(canvas, self.board)
        position = [0, 0]
        figure = None
        for image in canvas_images:
            canvas.tag_bind(image,  "<ButtonPress-1>", dragger.drag_start(position, figure)) ######## DO IT
            canvas.tag_bind(image,  "<B1-Motion>", dragger.drag_motion)
            canvas.tag_bind(image, "<ButtonRelease-1>", dragger.drag_stop)

