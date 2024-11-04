import random

class Ai:
    def __init__(self, board):
        self.board = board.board
        self.info = board.info
        self.engine = board.engine

    def negamax(self):
        pass

    def evaluate_board(self):
        pass

    def best_move(self):
        pass

    def generate_random_move(self, is_white):
        valid_moves = self.engine.all_valid_moves(is_white)

        if not valid_moves:
            return None

        random_move = random.choice(valid_moves)

        return random_move



