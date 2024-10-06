from Const import *

class Engine:
    def __init__(self, board):
        self.board = board

    def is_check(self, for_white):
        king_position = self.king_position(for_white)
        all_moves = self.all_valid_moves(not for_white)

        length = len(all_moves)

        for i in range(length):
            move = all_moves[i]
            if move[2] == king_position[0] and move[3] == king_position[1]:
                print("CHECK")
                return True

        return False


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

    def is_piece_bound(self,x,y):
        pass
    def is_legal_en_passant(self, x_start, y_start, x_end, y_end):
        pass

    ## it should be called always after checking if move is valid
    def is_it_capture(self, x_end, y_end):
        if self.board[y_end][x_end] == 0:
            return False
        else:
            return True

    def king_position(self, for_white):
        if for_white:
            value = 2
        else:
            value = -2

        for i in range(SIZE):
            for k in range(SIZE):
                if self.board[k][i] == value:
                    position = (i, k)
                    return position

    def is_valid_move(self, x_start, y_start, x_end, y_end):
        moves = self.valid_moves(x_start, y_start)
        print(f"valid moves {moves}")
        move = (x_start, y_start, x_end, y_end)

        if moves == None:
            return False

        if move in moves:
            return True
        else:
            return False

    ## generating all posible moves for white or for black
    def all_valid_moves(self, for_white):
        all_moves = []
        for i in range(SIZE):
            for k in range(SIZE):
                if self.board[k][i] == 0:
                    continue

                moves = self.valid_moves(i, k)
                length = len(moves)
                if for_white and self.board[k][i] > 0:
                    for j in range(length):
                        all_moves.append(moves[j])
                if not for_white and self.board[k][i] < 0:
                    for j in range(length):
                        all_moves.append(moves[j])

        if (1, 6, 1, 5) in all_moves:
            print("Found")
        else:
            print("Not Found")

        return all_moves



    def valid_moves(self,x,y):
        piece = self.get_figure(x, y)
        moves = []
        if piece is None:
            return moves

        ## pawn moves
        # check if in check or bound
        if abs(piece) == 1:

            # vertical for white pawn
            if piece == 1 and y < SIZE - 1 and self.board[y - 1][x] == 0:
                moves.append((x, y, x, y - 1))
                if y == 6 and self.board[y - 2][x] == 0:
                    moves.append((x, y, x, y - 2))

            # vertical for black pawn
            if piece == -1 and y > 0 and self.board[y + 1][x] == 0:
                moves.append((x, y, x, y + 1))
                if y == 1 and self.board[y + 2][x] == 0:
                    moves.append((x, y, x, y + 2))

            # diagonal to left for white pawn
            if piece == 1 and y > 0 and x > 0 and self.board[y - 1][x - 1] < 0:
                moves.append((x, y, x - 1, y - 1))

            # diagonal to right for white pawn
            if piece == 1 and y > 0 and x < SIZE - 1 and self.board[y - 1][x + 1] < 0:
                moves.append((x, y, x + 1, y - 1))

            # diagonal to left for black pawn
            if piece == -1 and y < SIZE - 1 and x > 0 and self.board[y + 1][x - 1] > 0:
                moves.append((x, y, x - 1, y + 1))

            # diagonal to right for black pawn
            if piece == -1 and y < SIZE - 1 and x < SIZE - 1 and self.board[y + 1][x + 1] > 0:
                moves.append((x, y, x + 1, y + 1))

            ## EN PASSANT !

        ## knight moves

        if abs(piece) == 3:
            direction = [(1,2),(2,1),(1, -2),(-1,2),(-2,1),(-1,-2),(-2,-1),(2,-1)]
            is_white = self.is_white_piece(x,y)

            for dx, dy in direction:
                x_move = x + dx
                y_move = y + dy
                move = (x, y, x_move, y_move)
                if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE ):
                    continue
                if self.board[y_move][x_move]!= 0:  ## if there is a piece
                    if self.is_white_piece(x_move, y_move) == is_white: ## if the piece is the same color
                        continue
                    else:
                        moves.append(move)
                        continue
                moves.append(move)

        ## bishop moves
        if abs(piece) == 4:
            direction = [(1,1),(-1,1),(1,-1),(-1,-1)]
            is_white = self.is_white_piece(x,y)

            for dx, dy in direction:
                for k in range(1, SIZE):
                    x_move = x + k * dx
                    y_move = y + k * dy
                    move = (x, y, x_move, y_move)
                    if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE ):
                        continue
                    if self.board[y_move][x_move]!= 0:  ## if there is a piece
                        if self.is_white_piece(x_move, y_move) == is_white: ## if the piece is the same color
                            break
                        else:
                            moves.append(move) ## capture
                            break
                    moves.append(move)

        ## rook moves
        if abs(piece) == 5:
            direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]
            is_white = self.is_white_piece(x, y)

            for dx, dy in direction:
                for k in range(1, SIZE):
                    x_move = x + k * dx
                    y_move = y + k * dy
                    move = (x, y, x_move, y_move)
                    if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                        continue
                    if self.board[y_move][x_move] != 0:  ## if there is a piece
                        if self.is_white_piece(x_move, y_move) == is_white:  ## if the piece is the same color
                            break
                        else:
                            moves.append(move)  ## capture
                            break
                    moves.append(move)

        ## king moves
        # add castling
        # check if opposite king is nearby
        if abs(piece) == 2:
            direction = [(1, 0), (-1, 0), (0, -1), (0, 1), (1,1),(-1,1),(1,-1),(-1,-1)]
            is_white = self.is_white_piece(x, y)

            for dx, dy in direction:
                x_move = x +  dx
                y_move = y +  dy
                move = (x, y, x_move, y_move)
                if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                    continue
                if self.board[y_move][x_move] != 0:  ## if there is a piece
                    if self.is_white_piece(x_move, y_move) == is_white:  ## if the piece is the same color
                        continue
                    else:
                        moves.append(move)  ## capture
                        continue
                moves.append(move)

        ## queen moves
        if abs(piece) == 9:
            direction = [(1, 0), (-1, 0), (0, -1), (0, 1), (1,1),(-1,1),(1,-1),(-1,-1)]
            is_white = self.is_white_piece(x, y)

            for dx, dy in direction:
                for k in range(1, SIZE):
                    x_move = x + k * dx
                    y_move = y + k * dy
                    move = (x, y, x_move, y_move)
                    if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                        continue
                    if self.board[y_move][x_move] != 0:  ## if there is a piece
                        if self.is_white_piece(x_move, y_move) == is_white:  ## if the piece is the same color
                            break
                        else:
                            moves.append(move)  ## capture
                            break
                    moves.append(move)

        return moves




    def is_white_piece(self, x, y):
        piece = self.get_figure(x, y)

        # Check if the piece is owned by the current player
        if piece > 0 :  return True
        elif piece < 0 : return False
        return None

    def get_figure(self, x, y):
        if x == None or y == None or x >= SIZE or y >= SIZE:
            return None

        figure = self.board[y][x]
        return figure