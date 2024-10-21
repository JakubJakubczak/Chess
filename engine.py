from Const import *
import copy

class Engine:
    def __init__(self, board):
        self.board = board

    def is_check(self, for_white, board = None):
        if board is None:
            board = self.board

        king_position = self.king_position(for_white, board)
        all_moves = self.all_valid_moves(not for_white, True, board)
        length = len(all_moves)

        for i in range(length):
            move = all_moves[i]
            if move[2] == king_position[0] and move[3] == king_position[1]:
                return True

        return False


    def checkmate(self, board = None):
        if board is None:
            board = self.board

        white = True
        black = False

        if self.is_check(white, board) and self.all_valid_moves(white, False, board) == []:
            is_white_winner = False
            return is_white_winner
        if self.is_check(black, board) and self.all_valid_moves(black, False, board) == []:
            is_white_winner = True
            return is_white_winner

        return None

    def is_stalemate(self, board = None):
        if board is None:
            board = self.board

        ## check if it will generate bugs, probalby turns required
        if self.all_valid_moves(True, False, board) == [] and not self.is_check(True, board):
            return True
        if self.all_valid_moves(False,False, board) == [] and not self.is_check(False, board):
            return True

        return False
    def draw(self):
        pass

    def game_over(self):
        print("game_over")
        checkmate = self.checkmate()
        if checkmate == True:
            return 1
        if checkmate == False:
            return -1
        elif self.is_stalemate():
            return 0
        elif self.draw():
            return 0
        else:
            return None
    def is_threefold_repetition(self):
        pass

    def is_fifty_move_rule(self):
        pass

    def is_insufficient_material(self):
        pass

    def is_legal_en_passant(self, x_start, y_start, x_end, y_end):
        pass

    def is_pawn_promotion(self, x_start, y_start, x_end, y_end):
        pass

    def is_castling_possible(self, x_start, y_start, x_end, y_end):
        pass

    def is_square_attacked(self, for_white, x, y, board):
        all_moves = self.all_valid_moves(not for_white, False, board)

        for move in all_moves:
            if move[2] == x and move[3] == y:
                return True

        return False




    ## it should be called always after checking if move is valid
    def is_it_capture(self, x_end, y_end, board = None):
        if board is None:
            board = self.board

        if board[y_end][x_end] == 0:
            return False
        else:
            return True

    def king_position(self, for_white, board = None):
        if board is None:
            board = self.board

        if for_white:
            value = 2
        else:
            value = -2

        for i in range(SIZE):
            for k in range(SIZE):
                if board[k][i] == value:
                    position = (i, k)
                    return position

    def is_valid_move(self, x_start, y_start, x_end, y_end, board = None):
        if board is None:
            board = self.board

        moves = self.valid_moves(x_start, y_start,False, board) ## nie działa  self.valid_moves(x_start, y_start, board) ??
        move = (x_start, y_start, x_end, y_end)

        if moves == None:
            return False

        if move in moves:
            return True
        else:
            return False

    ## generating all posible moves for white or for black
    def all_valid_moves(self, for_white, checking = False, board = None):
        if board is None:
            board = self.board

        all_moves = []
        for i in range(SIZE):
            for k in range(SIZE):
                if board[k][i] == 0:
                    continue

                if for_white != self.is_white_piece(i, k, board):
                    continue

                moves = self.valid_moves(i, k, checking, board)
                length = len(moves)
                for j in range(length):
                    all_moves.append(moves[j])

        return all_moves



    def valid_moves(self,x,y, checking = False, board = None):
        if board is None:
            board = self.board

        piece = self.get_figure(x, y, board)
        moves = []
        if piece is None:
            return moves

        if x < 0 and y < 0 or x >= SIZE or y >= SIZE:
            return moves
        ## pawn moves
        # check if in check or bound
        if abs(piece) == 1:

            # vertical for white pawn
            if piece == 1 and y > 0 and board[y - 1][x] == 0:
                moves.append((x, y, x, y - 1))
                if y == 6 and board[y - 2][x] == 0:
                    moves.append((x, y, x, y - 2))

            # vertical for black pawn
            if piece == -1 and y + 1 < SIZE and board[y + 1][x] == 0:
                moves.append((x, y, x, y + 1))
                if y == 1 and board[y + 2][x] == 0:
                    moves.append((x, y, x, y + 2))

            # diagonal to left for white pawn
            if piece == 1 and y > 0 and x > 0 and board[y - 1][x - 1] < 0:
                moves.append((x, y, x - 1, y - 1))

            # diagonal to right for white pawn
            if piece == 1 and y > 0 and x < SIZE - 1 and board[y - 1][x + 1] < 0:
                moves.append((x, y, x + 1, y - 1))

            # diagonal to left for black pawn
            if piece == -1 and y < SIZE - 1 and x > 0 and board[y + 1][x - 1] > 0:
                moves.append((x, y, x - 1, y + 1))

            # diagonal to right for black pawn
            if piece == -1 and y < SIZE - 1 and x < SIZE - 1 and board[y + 1][x + 1] > 0:
                moves.append((x, y, x + 1, y + 1))

            ## EN PASSANT !

        ## knight moves

        if abs(piece) == 3:
            direction = [(1,2),(2,1),(1, -2),(-1,2),(-2,1),(-1,-2),(-2,-1),(2,-1)]
            is_white = self.is_white_piece(x,y, board)

            for dx, dy in direction:
                x_move = x + dx
                y_move = y + dy
                move = (x, y, x_move, y_move)
                if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE ):
                    continue
                if board[y_move][x_move]!= 0:  ## if there is a piece
                    if self.is_white_piece(x_move, y_move, board) == is_white: ## if the piece is the same color
                        continue
                    else:
                        moves.append(move)
                        continue
                moves.append(move)

        ## bishop moves
        if abs(piece) == 4:
            direction = [(1,1),(-1,1),(1,-1),(-1,-1)]
            is_white = self.is_white_piece(x,y, board)

            for dx, dy in direction:
                for k in range(1, SIZE):
                    x_move = x + k * dx
                    y_move = y + k * dy
                    move = (x, y, x_move, y_move)
                    if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE ):
                        continue
                    if board[y_move][x_move]!= 0:  ## if there is a piece
                        if self.is_white_piece(x_move, y_move, board) == is_white: ## if the piece is the same color
                            break
                        else:
                            moves.append(move) ## capture
                            break
                    moves.append(move)

        ## rook moves
        if abs(piece) == 5:
            direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]
            is_white = self.is_white_piece(x, y, board)

            for dx, dy in direction:
                for k in range(1, SIZE):
                    x_move = x + k * dx
                    y_move = y + k * dy
                    move = (x, y, x_move, y_move)
                    if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                        continue
                    if board[y_move][x_move] != 0:  ## if there is a piece
                        if self.is_white_piece(x_move, y_move, board) == is_white:  ## if the piece is the same color
                            break
                        else:
                            moves.append(move)  ## capture
                            break
                    moves.append(move)

        ## king moves
        # add castling
        if abs(piece) == 2:
            direction = [(1, 0), (-1, 0), (0, -1), (0, 1), (1,1),(-1,1),(1,-1),(-1,-1)]
            is_white = self.is_white_piece(x, y, board)

            for dx, dy in direction:
                x_move = x +  dx
                y_move = y +  dy
                move = (x, y, x_move, y_move)
                if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                    continue
                if board[y_move][x_move] != 0:  ## if there is a piece
                    if self.is_white_piece(x_move, y_move, board) == is_white:  ## if the piece is the same color
                        continue
                    else:
                        moves.append(move)  ## capture
                        continue
                moves.append(move)

        ## queen moves
        if abs(piece) == 9:
            direction = [(1, 0), (-1, 0), (0, -1), (0, 1), (1,1),(-1,1),(1,-1),(-1,-1)]
            is_white = self.is_white_piece(x, y, board)

            for dx, dy in direction:
                for k in range(1, SIZE):
                    x_move = x + k * dx
                    y_move = y + k * dy
                    move = (x, y, x_move, y_move)
                    if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                        continue
                    if board[y_move][x_move] != 0:  ## if there is a piece
                        if self.is_white_piece(x_move, y_move, board) == is_white:  ## if the piece is the same color
                            break
                        else:
                            moves.append(move)  ## capture
                            break
                    moves.append(move)

            # Handle king safety by checking if any moves put the king in check
        if not checking:
            copy_board = copy.deepcopy(self.board)
            is_white = self.is_white_piece(x, y, board)
            valid_moves = []  # Collect only the valid moves

            for move in moves:

                # Make the move on the copy of the board
                piece = self.move_board(move[0], move[1], move[2], move[3], copy_board)

                # Check if the move results in a check for the current player
                if not self.is_check(is_white, copy_board):  # Valid if it doesn't put the king in check
                    valid_moves.append(move)
                # # Undo the move to restore the original board state
                self.undo_move_board(move[0], move[1], move[2], move[3], copy_board, piece)

            return valid_moves

        return moves

    def move_board(self, start_x, start_y, end_x, end_y, board):
        # srpawdzic czy to moze roszada albo promocja pionka
        # Save the state of the pieces involved in the move
        piece_from = self.get_figure(start_x, start_y, board)
        piece_to = self.get_figure(end_x, end_y, board)
        if piece_from != 0:
            board[end_y][end_x] = piece_from
            board[start_y][start_x] = 0

        return piece_to

    def undo_move_board(self, start_x, start_y, end_x, end_y, board, piece):
        # srpawdzic czy to moze roszada albo promocja pionka
        # Save the state of the pieces involved in the move
        piece_from = self.get_figure(end_x, end_y, board)
        if piece_from != 0:
            board[start_y][start_x] = piece_from
            board[end_y][end_x] = piece

    def is_white_piece(self, x, y, board):
        piece = self.get_figure(x, y, board)

        # Check if the piece is owned by the current player
        if piece > 0 :  return True
        elif piece < 0 : return False
        return None

    def get_figure(self, x, y, board):
        if x == None or y == None or x >= SIZE or y >= SIZE:
            return None

        figure = board[y][x]
        return figure

