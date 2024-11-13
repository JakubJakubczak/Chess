import random
import copy
from Const import *

class Ai:
    def __init__(self, board):
        self.engine = board.engine
        self.copy_engine = copy.deepcopy(self.engine)
        self.best_move = None

    # algorytm mniej więcej, bez żadnych cięć, promotio move zrobić i przerobić to żeby działało
    def negamax(self, depth, color):
        if depth == 0 or self.copy_engine.game_over() != None:
            return color * self.evaluate(), self.best_move

        for_white = True if color == 1 else False
        max_eval = float('-inf')

        for move in self.copy_engine.all_valid_moves(for_white):
            start_x, start_y, end_x, end_y, *promotion = move
            promotion_type = promotion[0] if promotion else None

            piece, is_white, changes, last2_move = self.copy_engine.move_board(start_x, start_y, end_x, end_y, promotion_type)
            evaluation, _ = self.negamax( depth - 1, -color)
            evaluation = -evaluation

            self.copy_engine.undo_move_board(start_x, start_y, end_x, end_y, piece, is_white, changes, last2_move)

            if evaluation > max_eval:
                max_eval = evaluation
                self.best_move = move

        return max_eval, self.best_move

    def find_best_move(self, depth, color):
        score, best_move = self.negamax(depth, color)
        print(f"Best move found: {best_move} with score {score}")

        return best_move, score

    def generate_random_move(self, is_white):
        valid_moves = self.engine.all_valid_moves(is_white)

        if not valid_moves:
            return None

        random_move = random.choice(valid_moves)

        return random_move


    def update_copy_engine(self, engine):
        self.copy_engine = copy.deepcopy(engine)

    def evaluate(self):
        material_score = self.evaluate_material()
        position_score = self.evaluate_position()
        # king_safety_score = self.evaluate_king_safety(board, color)
        # pawn_structure_score = self.evaluate_pawn_structure(board)
        # center_control_score = self.evaluate_center_control(board)
        # mobility_score = self.evaluate_mobility(board)

        # Sum with weights
        return (
                material_score * 1.0 +
                position_score * 0.5
                # king_safety_score * 1.5 +
                # pawn_structure_score * 0.8 +
                # center_control_score * 0.6 +
                # mobility_score * 0.3
        )

    def evaluate_material(self):
        piece_values = {1: 1, 2: 100, 3: 3, 4: 3, 5: 5, 9: 9, -1: -1, -2: -100, -3: -3, -4: -3, - 5: -5, -9: -9,}
        score = 0
        for col in range(SIZE):
            for row in range(SIZE):
                piece = self.engine.get_figure(row, col)
                if piece != 0:
                    value = piece_values[piece]
                    score += value
        return score

    def piece_square_score(self, piece, x, y):
        if abs(piece) == 1:
            return self.pawn_table[y][x] if self.engine.is_white_piece(x, y) else self.pawn_table[7 - y][x]

        elif abs(piece) == 2:
            return self.king_table_early[y][x] if self.engine.is_white_piece(x, y) else self.king_table_early[7 - y][x]

        elif abs(piece) == 3:
            return self.knight_table[y][x] if self.engine.is_white_piece(x, y) else self.knight_table[7 - y][x]

        elif abs(piece) == 4:
            return self.bishop_table[y][x]

        elif abs(piece) == 5:
            return self.rook_table[y][x]

        elif abs(piece) == 9:
            return self.queen_table[y][x]


    def evaluate_position(self):
        score = 0

        for col in range(SIZE):
            for row in range(SIZE):
                piece = self.engine.get_figure(row, col)
                piece_abs = abs(piece)
                position_value = self.piece_square_score(piece, row, col)
                if piece!= 0:
                    total_value = piece_abs + position_value ######## piece jest zalezne od koloru a position_value jedynie od położenia jak to polaczyc
                    score += total_value if self.engine.is_white_piece(row, col ) else -total_value


        return score

    def evaluate_king_safety(self, board, color):
        pass

    def evaluate_pawn_structure(self, board):
        pass

    def evaluate_center_control(self, board):
        pass

    def evaluate_mobility(self, board, color):
        pass

    pawn_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 2, 3, 3, 2, 1, 1],
        [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
        [0.5, 1, 1, -2, -2, 1, 1, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    knight_table = [
        [-5, -4, -3, -3, -3, -3, -4, -5],
        [-4, -2, 0, 0, 0, 0, -2, -4],
        [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
        [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
        [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
        [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
        [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
        [-5, -4, -3, -3, -3, -3, -4, -5]
    ]

    bishop_table = [
        [-2, -1, -1, -1, -1, -1, -1, -2],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-1, 0, 1, 2, 2, 1, 0, -1],
        [-1, 0, 1, 2, 2, 1, 0, -1],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-2, -1, -1, -1, -1, -1, -1, -2]
    ]

    rook_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 2, 2, 2, 1, 0],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [0, 1, 2, 3, 3, 2, 1, 0],
        [0, 1, 2, 2, 2, 2, 1, 0],
        [0, 0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    queen_table = [
        [-2, -1, -1, 0, 0, -1, -1, -2],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-1, 1, 1, 2, 2, 1, 1, -1],
        [0, 1, 2, 2, 2, 2, 1, 0],
        [0, 1, 2, 2, 2, 2, 1, 0],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-2, -1, -1, 0, 0, -1, -1, -2],
        [-2, -1, -1, 0, 0, -1, -1, -2]
    ]

    king_table_early = [
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-2, -3, -3, -4, -4, -3, -3, -2],
        [-2, -3, -3, -4, -4, -3, -3, -2],
        [-1, -2, -2, -3, -3, -2, -2, -1],
        [2, 2, 0, 0, 0, 0, 2, 2]
    ]

    king_table_endgame = [
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-30, -10, 10, 20, 20, 10, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 10, 20, 20, 10, -10, -30],
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-50, -40, -30, -20, -20, -30, -40, -50]
    ]



