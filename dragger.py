from Const import *
class Dragger:
    def __init__(self, figures, canvas, board):
        self.figures = figures
        self.board = board
        self.canvas = canvas
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.initial_position = {"x": 0, "y": 0, "item": None}
        self.initial_index = [None,None]
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


    def drag_start(self, event):
        print("drag_start")
        x,y = self.calculate_board_position(event.x, event.y)
        print(f"valid moves {self.board.engine.valid_moves(x, y)}")
        print(f"x: {x}, y: {y}")
        print(self.board.engine.is_white_piece(x,y, self.board.board))
        print(self.board.white_turn)
        print(self.board.board)
        if self.board.engine.is_white_piece(x, y,self.board.board) == self.board.white_turn:
            self.drag_data["item"] = self.figures.canvas_images[y][x]

        if self.drag_data["item"]:
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.initial_index = [x, y]
            self.figure = self.board.engine.get_figure(x, y, self.board.board)

            # centrowanie figury po kliknięciu
            x, y = self.canvas.coords(self.drag_data["item"])
            delta_x = x - event.x
            delta_y = y - event.y
            self.initial_position = {'x': x, 'y': y, 'item': self.drag_data["item"]}
            self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
            print(self.board.board)


    def drag_motion(self, event):
        # print("drag_motion")
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
        # print("drag_stop")
        if self.drag_data["item"] is not None:
            x_start, y_start = self.calculate_board_position(self.initial_position["x"], self.initial_position["y"])
            delta_x = self.drag_data["x"] - self.initial_position["x"]
            delta_y = self.drag_data["y"] - self.initial_position["y"]
            x_end, y_end = self.calculate_board_position(self.drag_data["x"], self.drag_data["y"])
            if x_end is None or y_end is None:
                ## change it to one function in figures class
                self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
                self.drag_data["item"] = None
                return

            if x_start == x_end and y_start == y_end:
                self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
                self.drag_data["item"] = None
                return

            print("Valid move, making move...  ")
            if not self.board.engine.is_valid_move(x_start, y_start, x_end, y_end):
                self.canvas.move(self.drag_data["item"], -delta_x, -delta_y)
                self.drag_data["item"] = None
                return


            self.board.move(x_start, y_start, x_end, y_end)
            self.board.white_turn = not self.board.white_turn
            self.figures.move_images(self.drag_data, x_start, y_start, x_end, y_end)

            # self.board.engine.is_check(self.board.white_turn)

            print(self.board.board)
            self.drag_data["item"] = None



