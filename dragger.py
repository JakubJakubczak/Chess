import board
from Const import *
class Dragger:
    def __init__(self, figures, canvas, board, game):
        self.figures = figures
        self.board = board
        self.canvas = canvas
        self.game = game

        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.initial_position = {"x": 0, "y": 0, "item": None}
        self.initial_index = [None,None]
        self.figure = 0

    def calculate_board_position(self, x ,y):
       if x < 0 or y < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
           return None,None

       x_index = int (x // SPACE_SIZE)
       y_index = int (y // SPACE_SIZE)

       return x_index,y_index

    def drag_start(self, event):
        if settings["AI"] and self.board.white_turn == settings["TURN"] or not settings["AI"]:
            self.board.dehighlight_valid_moves()
            x_board,y_board = self.calculate_board_position(event.x, event.y)

            if self.board.engine.is_white_piece(x_board, y_board) == self.board.white_turn:
                self.drag_data["item"] = self.figures.canvas_images[y_board][x_board]

            if self.drag_data["item"]:
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                self.initial_index = [x_board, y_board]
                self.figure = self.board.engine.get_figure(x_board, y_board)

                # centrowanie figury po kliknięciu
                x, y = self.canvas.coords(self.drag_data["item"])
                delta_x = x - event.x
                delta_y = y - event.y
                self.initial_position = {'x': x, 'y': y, 'item': self.drag_data["item"]}
                self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)

                valid_moves = self.board.engine.valid_moves(x_board, y_board)
                self.board.highlight_valid_moves(valid_moves)


    def drag_motion(self, event):
        if self.drag_data["item"] is not None:
            ## compute how much the mouse has moved
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            # move the object the appropriate amount
            self.canvas.move(self.drag_data["item"], delta_x, delta_y)
            # record the new position
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def drag_stop(self, event):
        if self.drag_data["item"] is not None:
            x_start, y_start = self.calculate_board_position(self.initial_position["x"], self.initial_position["y"])
            delta_x = self.drag_data["x"] - self.initial_position["x"]
            delta_y = self.drag_data["y"] - self.initial_position["y"]
            x_end, y_end = self.calculate_board_position(self.drag_data["x"], self.drag_data["y"])
            if x_end is None or y_end is None:
                self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
                self.drag_data["item"] = None
                return

            if x_start == x_end and y_start == y_end:
                self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
                self.drag_data["item"] = None
                return

            if not self.board.engine.is_valid_move(x_start, y_start, x_end, y_end):
                self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
                self.drag_data["item"] = None
                return


            self.game.move(self.drag_data, x_start, y_start, x_end, y_end)

            print(self.board.board)
            self.drag_data["item"] = None



