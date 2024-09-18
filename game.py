class Game:
    def __init__(self, canvas, window):
        self.canvas = canvas
        self.game_on = True
        self.window = window
        self.white_turn = True

    def is_Game_On(self):
        if self.game_on:
            return True
        else:
            return False

    def start_Game(self):
        pass

    def display_Game(self):
        pass

    def is_white_turn(self):
        if self.white_turn:
            return True
        else:
            return False