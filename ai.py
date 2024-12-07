import random
import copy
from Const import *
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
class Ai:
    def __init__(self):
        # self.engine = board.engine
        # self.copy_engine = copy.deepcopy(self.engine)
        self.best_move = None
        self.iteration = 0


    def negamax(self, depth, color, engine_copy, alpha, beta, moves):
        if depth == 0:
            return color * self.evaluate(engine_copy), self.best_move

        for_white = True if color == 1 else False
        max_eval = float('-inf')

        moves = self.order_moves(moves, engine_copy)
        for move in moves:
            start_x, start_y, end_x, end_y, *promotion = move
            promotion_type = promotion[0] if promotion else None

            piece, is_white, changes, last2_move = engine_copy.move_board(start_x, start_y, end_x, end_y, promotion_type)
            engine_copy.update_valid_moves(True)

            next_moves  = engine_copy.valid_moves_black if for_white is True else engine_copy.valid_moves_white

            evaluation, _ = self.negamax( depth - 1, -color, engine_copy, -beta, -alpha, next_moves)
            evaluation = -evaluation

            engine_copy.undo_move_board(start_x, start_y, end_x, end_y, piece, is_white, changes, last2_move)

            engine_copy.update_valid_moves(True)

            if evaluation > max_eval:
                max_eval = evaluation
                if depth == DEPTH:
                    self.best_move = move

            self.iteration += 1

            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break

        return (max_eval, self.best_move)

    def find_best_move(self, depth, color, engine, return_queue=None):
        engine_copy = copy.deepcopy(engine)

        for_white = True if color == 1 else False
        valid_moves = engine_copy.all_valid_moves(for_white)
        score, best_move = self.negamax(depth, color, engine_copy, -MATE, MATE, valid_moves)
        # score, best_move = self.parallel_negamax(depth, color, engine_copy, -MATE, MATE)
        print(f"Best move found: {best_move} with score {score}")

        return best_move, score


    def generate_random_move(self, is_white, engine):
        valid_moves = engine.all_valid_moves(is_white)

        if not valid_moves:
            return None

        random_move = random.choice(valid_moves)

        return random_move

    def order_moves(self, moves, engine_copy):
        eval_moves = []
        for move in moves:
            start_x, start_y, end_x, end_y, *promotion = move

            promotion_bonus = 10 if promotion else 0
            capture_bonus = engine_copy.get_figure(end_x, end_y)

            eval_moves.append((capture_bonus + promotion_bonus, move))

        # Zwracnie ruchów posortowanych malejąco
        return [move for _, move in sorted(eval_moves, key=lambda x: x[0], reverse=True)]

    # def update_copy_engine(self, engine):
    #     self.copy_engine = copy.deepcopy(engine)

    def evaluate(self, engine):
        material_score = self.evaluate_material(engine)
        position_score = self.evaluate_position(engine)
        mobility_score = self.evaluate_mobility(engine)

        return (
                material_score * 1.2 +
                position_score * 0.5 +
                mobility_score * 0.1
        )

    def evaluate_mobility(self, engine):
        return len(engine.valid_moves_white) - len(engine.valid_moves_black)

    def evaluate_material(self, engine):
        piece_values = {1: 1, 2: 100, 3: 3, 4: 3, 5: 5, 9: 9, -1: -1, -2: -100, -3: -3, -4: -3, - 5: -5, -9: -9,}
        score = 0
        for col in range(SIZE):
            for row in range(SIZE):
                piece = engine.get_figure(row, col)
                if piece != 0:
                    value = piece_values[piece]
                    score += value
        return score

    def piece_square_score(self, piece, x, y, color):
        if abs(piece) == 1:
            return self.pawn_table[y][x] if color == 1 else self.pawn_table[7 - y][x]

        elif abs(piece) == 2:
            return self.king_table_early[y][x] if color == 1 else self.king_table_early[7 - y][x]

        elif abs(piece) == 3:
            return self.knight_table[y][x] if color == 1 else self.knight_table[7 - y][x]

        elif abs(piece) == 4:
            return self.bishop_table[y][x]

        elif abs(piece) == 5:
            return self.rook_table[y][x]

        elif abs(piece) == 9:
            return self.queen_table[y][x]


    def evaluate_position(self, engine):
        score = 0

        for col in range(SIZE):
            for row in range(SIZE):
                piece = engine.get_figure(row, col)
                piece_abs = abs(piece)
                for_white = engine.is_white_piece(row, col)
                color = 1 if for_white else -1
                position_value = self.piece_square_score(piece, row, col, color)
                if piece!= 0:
                    total_value = piece_abs + position_value
                    score += total_value if engine.is_white_piece(row, col ) else -total_value


        return score

    def evaluate_king_safety(self, board, color):
        pass

    def evaluate_pawn_structure(self, board):
        pass

    def evaluate_center_control(self, board):
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


   #  def evaluate_move(self, move, depth, color, engine_copy, alpha, beta, negamax_func):
   #      """
   #      Standalone function to evaluate a single move.
   #      This function must be at the top level to be pickled by ProcessPoolExecutor.
   #      """
   #      local_engine = copy.deepcopy(engine_copy)  # Ensure thread/process safety
   #      start_x, start_y, end_x, end_y, *promotion = move
   #      promotion_type = promotion[0] if promotion else None
   #
   #      piece, is_white, changes, last2_move = local_engine.move_board(
   #          start_x, start_y, end_x, end_y, promotion_type
   #      )
   #      next_moves = local_engine.all_valid_moves(not is_white)
   #      evaluation, _ = negamax_func(depth - 1, -color, local_engine, -beta, -alpha, next_moves)
   #      local_engine.undo_move_board(start_x, start_y, end_x, end_y, piece, is_white, changes, last2_move)
   #
   #      return -evaluation, move
   #  def negamax_parallel(self, depth, color, engine_copy, alpha, beta, moves):
   #      if depth == 0 or engine_copy.game_over():
   #          return color * self.evaluate(engine_copy), self.best_move
   #
   #      max_eval = float('-inf')
   #      best_move = None
   #      for_white = True if color == 1 else False
   #
   #      if depth == DEPTH:  # Root level parallelization
   #          # Parallelize move evaluation
   #          with ProcessPoolExecutor() as executor:
   #              futures = [
   #                  executor.submit(
   #                      self.evaluate_move, move, depth, color, engine_copy, alpha, beta, self.negamax
   #                  )
   #                  for move in moves
   #              ]
   #
   #              for future in futures:
   #                  evaluation, move = future.result()
   #                  if evaluation > max_eval:
   #                      max_eval = evaluation
   #                      best_move = move
   #
   #                  alpha = max(alpha, max_eval)
   #                  if alpha >= beta:
   #                      break  # Beta cutoff
   #
   #          if depth == DEPTH:
   #              self.best_move = best_move
   #
   #      else:  # Inner nodes: Sequential
   #          for move in moves:
   #              start_x, start_y, end_x, end_y, *promotion = move
   #              promotion_type = promotion[0] if promotion else None
   #
   #              piece, is_white, changes, last2_move = engine_copy.move_board(
   #                  start_x, start_y, end_x, end_y, promotion_type
   #              )
   #              next_moves = engine_copy.all_valid_moves(not for_white)
   #              evaluation, _ = self.negamax(depth - 1, -color, engine_copy, -beta, -alpha, next_moves)
   #              evaluation = -evaluation
   #
   #              engine_copy.undo_move_board(start_x, start_y, end_x, end_y, piece, is_white, changes, last2_move)
   #
   #              if evaluation > max_eval:
   #                  max_eval = evaluation
   #                  if depth == DEPTH:
   #                      self.best_move = move
   #
   #              alpha = max(alpha, max_eval)
   #              if alpha >= beta:
   #                  break
   #
   #      return max_eval, best_move
   #
   # def parallel_negamax(self, depth, color, engine_copy, alpha, beta):
   #      for_white = True if color == 1 else False
   #      moves = engine_copy.all_valid_moves(for_white)
   #      args = [( depth, color, engine_copy, alpha, beta, [move]) for move in moves]
   #
   #      eval_moves = []
   #
   #      with Pool(processes=PROCESSES) as pool:
   #          eval_moves = pool.map(self.negamax_wrapper, args)
   #
   #      eval_moves.sort(reverse=True, key=lambda x: x[0])
   #
   #      return eval_moves[0]
   #
   #  def negamax_wrapper(self, args):
   #      # Unpack arguments from the tuple (move, depth, color, engine_copy, alpha, beta)
   #      depth, color, engine_copy, alpha, beta, move = args
   #      return self.negamax(depth, color, engine_copy, alpha, beta, move)