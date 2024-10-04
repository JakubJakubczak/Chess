from Const import *

class Engine:
    def __init__(self, board):
        self.board = board

    def is_check(self):
        pass

    def is_checkmate(self):
        pass

    def is_stalemate(self):
        pass

    def is_threefold_repetition(self):
        pass

    def is_fifty_move_rule(self):
        pass

    def is_insufficient_material(self):
        pass

    def is_pawn_promotion(self, x_start, y_start, x_end, y_end):
        pass

    def is_castling_possible(self, x_start, y_start, x_end, y_end):
        pass

    def is_king_in_check(self, x, y):
        pass

    def is_legal_en_passant(self, x_start, y_start, x_end, y_end):
        pass
    def is_valid_move(self, x_start, y_start, x_end, y_end):
        return True

    ## generating all posible moves for AI
    def all_valid_moves(self):
        pass
    def valid_moves(self,x,y):
        piece = self.get_figure(x, y)
        moves = []
        if piece is None:
            return moves

        ## pawn moves
        if abs(piece) == 1:
            if piece == 1 and y < SIZE - 1 and self.board[y + 1][x] == 0:
                moves.append((x, y + 1))

            if piece == -1 and y > 0 and self.board[y - 1][x] == 0:
                moves.append((x, y - 1))

            if piece == 1 and y > 0 and x > 0 and self.board[y - 1][x - 1] < 0:
                moves.append((x - 1, y - 1))

            if piece == 1 and y > 0 and x < SIZE - 1 and self.board[y - 1][x + 1] < 0:
                moves.append((x + 1, y - 1))

            if piece == -1 and y < SIZE - 1 and x > 0 and self.board[y + 1][x - 1] < 0:
                moves.append((x - 1, y + 1))

            if piece == -1 and y < SIZE - 1 and x < SIZE - 1 and self.board[y + 1][x + 1] < 0:
                moves.append((x + 1, y + 1))

            ## EN PASSANT !

        ## knight moves

        if abs(piece) == 3:

            is_white = self.is_white_piece(x,y)









    def is_white_piece(self, x, y):
        piece = self.get_figure(x, y)

        # Check if the piece is owned by the current player
        if piece > 0 :  print(piece); return True
        elif piece < 0 : print(piece); return False
        return None

    def get_figure(self, x, y):
        if x == None or y == None or x >= SIZE or y >= SIZE:
            return None

        figure = self.board[y][x]
        return figure