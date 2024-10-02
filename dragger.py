
from Const import *
class Dragger:
    def __init__(self, canvas, board):
        self.board = board
        self.canvas = canvas
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.initial_position = {"x": 0, "y": 0, "item": None}
        self.initial_index  = [None,None]
        self.figure = 0


    # ustalic pozycje na boardzie za pomocą położenia myszy
    # ustalic jaka to figura na podstawie boarda
    # zmiana boarda
    # walidacja
    # drag stop
    def calculate_board_position(self, x ,y):
       if x < 0 or y < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
           return None,None

       x_index = int (x // SPACE_SIZE)
       y_index = int (y // SPACE_SIZE)

       return x_index,y_index

    def get_figure(self, x, y):
        if x == None or y == None or x >= SIZE or y >= SIZE:
            return None

        figure = self.board.board[x][y]
        return figure

    def drag_start(self, event):
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        x,y = self.calculate_board_position(event.x, event.y)
        self.initial_position = {'x': event.x, 'y': event.y, 'item': self.drag_data["item"]}
        self.initial_index = [x, y]
        self.figure = self.get_figure(x, y)

        # centrowanie figury po kliknięciu
        x, y = self.canvas.coords(self.drag_data["item"])
        delta_x = x - event.x
        delta_y = y - event.y
        self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
        print(self.board.board)

    def drag_motion(self, event):
        # compute how much the mouse has moved
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self.drag_data["item"], delta_x, delta_y)
        # record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag_stop(self, event):
        x_start, y_start = self.calculate_board_position(self.initial_position["x"], self.initial_position["y"])
        delta_x = self.drag_data["x"] - self.initial_position["x"]
        delta_y = self.drag_data["y"] - self.initial_position["y"]
        x_end, y_end = self.calculate_board_position(self.drag_data["x"], self.drag_data["y"])
        if x_end is None or y_end is None:
            self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
            return

        if not self.board.engine.is_valid_move(x_start, y_start, y_start, y_end):
            self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
            return

        self.board.move(x_start, y_start, x_end, y_end)


        figure_coords_x = SPACE_SIZE / 2
        figure_coords_y = SPACE_SIZE / 2

        center_coords_x = figure_coords_x + (x_end * SPACE_SIZE)
        center_coords_y = figure_coords_y + (y_end * SPACE_SIZE)

        delta_center_x = self.drag_data["x"] - center_coords_x
        delta_center_y = self.drag_data["y"] - center_coords_y

        print(center_coords_x)
        print(center_coords_y)
        print(delta_center_x)
        print(delta_center_y)
        print(self.drag_data["x"])
        print(self.drag_data["y"])

        self.canvas.move(self.drag_data["item"], -delta_center_x, -delta_center_y)
        print(self.board.board)

def get_center_of_object(canvas, rect):
    # Get the bounding box coordinates of the object
    x1, y1, x2, y2 = canvas.coords(rect)

    # Calculate the center
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    return center_x, center_y


