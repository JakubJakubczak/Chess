class Dragger:
    def __init__(self, canvas, board):
        self.canvas = canvas
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.initial_position = {"x": 0, "y": 0, "item": None}
        self.figure = None

### dragge musi miec info w jakim polozeniu startowym byla bierka oraz jaka to bierka
    def drag_start(self, event):
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.initial_position = {'x': event.x, 'y': event.y, 'item': self.drag_data["item"]}
        # self.figure =

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
        """End drag of an object"""
        # reset the drag data
       # if mouse is on board; else back to initial position
       # validate - move(start, end) - a function that checks if the move is valid
       # calculate position on the board and on the canvas


