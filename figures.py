### jak zrobic wyswietlanie caly czas stanu jak i zmian
### w konstruktorze figury dodać boarda, po to, żeby init zrobić
### poprawic boarda z przekazywania funkcją na po prostu sel.board
############ JAK DOBRZE WGRAC IMAGES
############## PRZEKAZAC INFORMACJE O BIERCE I POZYCJI W DRAG

from tkinter import *
from PIL import Image, ImageTk
from Const import *
from dragger import *

class Figures:
    def __init__(self, board):
       self.board = board
       images = self.load_canvas_images(board.board) # list
       image_dimensions = self.calculate_image_dimensions(images[0][0]) ## imgaes[0][0] because all images are the same size
       first_cordinates = self.calculate_first_cordinates(image_dimensions)
       canvas_images = self.display_figures(first_cordinates, images, board.canvas_board, board.board) # list
       self.bind_figures(board.canvas_board, canvas_images)

    def load_canvas_images(self, board):
        number_of_images = 12
        numbers_of_pieces = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 9, -9]
        images = [[None for _ in range(SIZE)] for _ in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] != 0:
                    piece = board[i][j]
                    image = ImageTk.PhotoImage(Image.open(f"images/{piece}.png"))
                    images[i][j] = image
        return images


    def calculate_image_dimensions(self, image):
        dimensions = [image.width(),image.height()]
        return dimensions

    def calculate_first_cordinates(self, image_dimensions):
        figure_coords_x = (SPACE_SIZE - image_dimensions[0]) / 2
        figure_coords_y = (SPACE_SIZE - image_dimensions[1]) / 2
        return [figure_coords_x, figure_coords_y]

    def display_figures(self, first_cordinates, images, canvas, board):
        canvas_images = []
        for i in range(SIZE):
            for j in range(SIZE):
                if board[i][j] != 0:
                    canvas_image = canvas.create_image(first_cordinates[0] + (j * SPACE_SIZE), first_cordinates[1] + (i * SPACE_SIZE), image=images[i][j])
                    canvas_images.append(canvas_image)
        return canvas_images

    def bind_figures(self, canvas, canvas_images):
        dragger = Dragger(canvas)
        for i in range(len(canvas_images)):
            canvas.tag_bind(canvas_images[i],  "<ButtonPress-1>", dragger.drag_start)
            canvas.tag_bind(canvas_images[i],  "<B1-Motion>", lambda: dragger.drag_motion(canvas))
            canvas.tag_bind(canvas_images[i], "<ButtonRelease-1>", lambda: dragger.drag_stop(canvas))

