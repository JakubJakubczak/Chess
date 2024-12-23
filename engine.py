from Const import *
import copy

class Engine:
    def __init__(self, board, info, turn = None):
        self.board = board
        self.info = info
        self.turn = turn
        self.boolean = False
        self.last_valid_moves_white = None
        self.last_valid_moves_black = None
        self.valid_moves_white = None
        self.valid_moves_black = None


    def is_check(self, for_white):
        king_position = self.king_position(for_white)
        all_moves = self.valid_moves_black if for_white else self.valid_moves_white
        if all_moves is None:   # Przy inicjacji
            return False

        length = len(all_moves)

        for i in range(length):
            move = all_moves[i]
            if move[2] == king_position[0] and move[3] == king_position[1]:
                return True

        return False

    def is_king_on_board(self, for_white):
        if for_white:
            value = 2
        else:
            value = -2

        for col in range(SIZE):
            for row in range(SIZE):
                piece = self.board[col][row]
                if piece == value:
                    return True

        return False

    def checkmate(self):
        if self.is_check(WHITE) and self.valid_moves_white == []:
            return False
        if self.is_check(BLACK) and self.valid_moves_black == []:
            return True

        return None

    def is_stalemate(self):
        if self.valid_moves_white == [] and not self.is_check(WHITE):
            return True
        if self.valid_moves_black == [] and not self.is_check(BLACK):
            return True

        return False
    def draw(self):
        if self.is_threefold_repetition() or self.is_fifty_move_rule() or self.is_insufficient_material() or self.is_stalemate():
            return True

        return False

    def is_threefold_repetition(self):
        pass

    def game_over(self):
        checkmate = self.checkmate()
        if checkmate == True:
            return 1
        if checkmate == False:
            return -1
        elif self.draw():
            print("draw")
            return 0
        else:
            return None

    def is_fifty_move_rule(self):
        if self.info[9] >= 100:
            print("50 powtorzen")
            return True

        return False
    def is_pawn_move(self, x_start, y_start):
        piece = self.board[y_start][x_start]

        if abs(piece) == 1:
            return True

        return False
    def update_fifty_move_rule(self, x_start, y_start, x_end, y_end):
        prev = self.info[9]
        if self.is_pawn_move(x_start, y_start) or self.is_it_capture(x_end, y_end):
            self.info[9] = 0

        else:
            self.info[9] += 1

        return prev

    def is_insufficient_material(self):
        pieces_white = []
        pieces_black = []
        white_sum = 0
        black_sum = 0

        for i in range(SIZE):
            for j in range(SIZE):
                piece = self.board[i][j]
                if piece!= 0:
                    if piece > 0:
                        pieces_white.append(piece)
                        white_sum += piece
                    else:
                        pieces_black.append(piece)
                        black_sum += piece

                if white_sum > 8 or abs(black_sum) > 8: # 8, ponieważ KNN dają sume największą
                    return False

        # KB vs K
        # KN vs K
        if len(pieces_white) == 2 and len(pieces_black) == 1:
            if 4 in pieces_white or 3 in pieces_white:
                return True

        if len(pieces_black) == 2 and len(pieces_white) == 1:
            if -4 in pieces_black or -3 in pieces_black:
                return True

        # KNN vs K
        if len(pieces_white) == 3 and len(pieces_black) == 1:
            if pieces_white.count(3) == 2:
                return True

        if len(pieces_black) == 3 and len(pieces_white) == 1:
            if pieces_black.count(-3) == 2:
                return True

        return False

    def is_square_empty(self,x, y):
        if self.board[y][x] == 0:
            return True

        return False
    def is_pawn_move_of_2_sqr(self, x_start, y_start, x_end, y_end):
        piece = self.get_figure(x_end, y_end)
        if abs(piece) != 1:
            return False

        if abs(y_end - y_start) == 2:
            return True

        return False

    def is_enpassanat_pawn_nearby(self, x_pawn, y_pawn, x_enpas, y_enpas):
        if not y_enpas == y_pawn:
            return False, None

        if x_enpas == x_pawn - 1:
            return True, -1

        if x_enpas == x_pawn + 1:
            return True, +1

        return False, None

    def is_enpassant(self, x_start, y_start, x_end, y_end, piece):
        if abs(piece) != 1:
            return False

        if abs(x_end - x_start) == 0:
            return False

        if self.is_square_empty(x_end, y_end):
            return True

        return False


    def is_pawn_promotion(self, x_start, y_start, x_end, y_end):

        piece = self.get_figure(x_start, y_start)
        if not abs(piece) == 1:
            return False

        if y_end == 0 or y_end == 7:
            return True

        return False

    def promote(self,x,y, piece):
        color = 1 if self.is_white_piece(x,y) else -1

        self.board[y][x] = piece * color


    def is_square_attacked(self, for_white, x, y):
        all_moves = self.valid_moves_black if for_white else self.valid_moves_white

        for move in all_moves:
            if move[2] == x and move[3] == y:
                return True

        return False

    def queen_castling_rights(self, for_white):
        if for_white:
            return self.info[0]
        else:
            return self.info[2]

    def king_castling_rights(self,for_white):
        if for_white:
            return self.info[1]
        else:
            return self.info[3]

    def change_queen_castling_rights(self,for_white, change):
        if for_white:
            self.info[0] = change
        else:
            self.info[2] = change

    def change_king_castling_rights(self, for_white, change):
        if for_white:
            self.info[1] = change
        else:
            self.info[3] = change

    def is_queen_castling_possible(self, for_white):
        if for_white:
            row = 7
        else:
            row = 0

        if not self.is_check(for_white) and \
            self.board[row][1] == 0 and self.board[row][2] == 0 and self.board[row][3] == 0 and \
            not self.is_square_attacked(for_white, 2, row) and not self.is_square_attacked(for_white, 3, row):

            return True

        return False

    def is_king_castling_possible(self, for_white):
        if for_white:
            row = 7
        else:
            row = 0

        if not self.is_check(for_white) and \
                self.board[row][5] == 0 and self.board[row][6] == 0 and \
                not self.is_square_attacked(for_white, 5, row) and not self.is_square_attacked(for_white, 6, row):
            return True

        return False

    def is_castling(self, x_start, y_start, x_end, y_end, piece):
        if abs(piece) == 2: # jest to król
            if abs(x_start - x_end) == 2:   # ruch o 2 pola to roszada
                return True

        return False

    def is_left_castling(self, x_start, x_end):
        if x_start > x_end:
            return True
        else:
            return False

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
        move = (x_start, y_start, x_end, y_end)

        if moves == None:
            return False

        for valid_move in moves:
            if valid_move[:4] == move:
                return True

        return False

    def all_valid_moves(self, for_white, checking = False):
        all_moves = []
        for i in range(SIZE):
            for k in range(SIZE):
                if self.board[i][k] == 0:
                    continue

                if for_white != self.is_white_piece(k, i):
                    continue

                moves = self.valid_moves(k, i, checking)
                length = len(moves)
                for j in range(length):
                    all_moves.append(moves[j])

        return all_moves

    def append_move_as_promotion(self, x_start, y_start, x_end, y_end, moves):
        moves.append((x_start, y_start, x_end, y_end, 9))
        moves.append((x_start, y_start, x_end, y_end, 5))
        moves.append((x_start, y_start, x_end, y_end, 4))
        moves.append((x_start, y_start, x_end, y_end, 3))

    def generate_pawn_moves(self, x, y, piece, moves, color):
        # vertical for white pawn
        if piece == 1 and y > 0 and self.board[y - 1][x] == 0:
            if y - 1 == 0:
                self.append_move_as_promotion(x, y, x, y - 1, moves)
            else:
                moves.append((x, y, x, y - 1))

            if y == 6 and self.board[y - 2][x] == 0:
                moves.append((x, y, x, y - 2))

        # vertical for black pawn
        if piece == -1 and y + 1 < SIZE and self.board[y + 1][x] == 0:
            if y + 1 == 7:
                self.append_move_as_promotion(x, y, x, y + 1, moves)
            else:
                moves.append((x, y, x, y + 1))

            if y == 1 and self.board[y + 2][x] == 0:
                moves.append((x, y, x, y + 2))

        # diagonal to left for white pawn
        if piece == 1 and y > 0 and x > 0 and self.board[y - 1][x - 1] < 0:
            if y - 1 == 0:
                self.append_move_as_promotion(x, y, x - 1, y - 1, moves)
            else:
                moves.append((x, y, x - 1, y - 1))

        # diagonal to right for white pawn
        if piece == 1 and y > 0 and x < SIZE - 1 and self.board[y - 1][x + 1] < 0:
            if y - 1 == 0:
                self.append_move_as_promotion(x, y, x + 1, y - 1, moves)
            else:
                moves.append((x, y, x + 1, y - 1))

        # diagonal to left for black pawn
        if piece == -1 and y < SIZE - 1 and x > 0 and self.board[y + 1][x - 1] > 0:
            if y + 1 == 7:
                self.append_move_as_promotion(x, y, x - 1, y + 1, moves)
            else:
                moves.append((x, y, x - 1, y + 1))

        # diagonal to right for black pawn
        if piece == -1 and y < SIZE - 1 and x < SIZE - 1 and self.board[y + 1][x + 1] > 0:
            moves.append((x, y, x + 1, y + 1))
            if y + 1 == 7:
                self.append_move_as_promotion(x, y, x + 1, y + 1, moves)
            else:
                moves.append((x, y, x + 1, y + 1))

        ## EN PASSANT
        move = self.info[5]
        # print(f"move {move}")
        if move != None:
            if self.is_pawn_move_of_2_sqr(move[0], move[1], move[2], move[3]):
                enpassant = self.is_enpassanat_pawn_nearby(x, y, move[2], move[3])
                if enpassant[0]:
                    moves.append((x, y, x + enpassant[1], y - color))

    def generate_bishop_moves(self, x, y, moves):
        direction = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        is_white = self.is_white_piece(x, y)

        for dx, dy in direction:
            for k in range(1, SIZE):
                x_move = x + k * dx
                y_move = y + k * dy
                move = (x, y, x_move, y_move)
                if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                    continue
                if self.board[y_move][x_move] != 0:
                    if self.is_white_piece(x_move, y_move) == is_white:
                        break
                    else:
                        moves.append(move)
                        break
                moves.append(move)

    def generate_knight_moves(self, x, y, moves):
        direction = [(1, 2), (2, 1), (1, -2), (-1, 2), (-2, 1), (-1, -2), (-2, -1), (2, -1)]
        is_white = self.is_white_piece(x, y)

        for dx, dy in direction:
            x_move = x + dx
            y_move = y + dy
            move = (x, y, x_move, y_move)
            if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                continue
            if self.board[y_move][x_move] != 0:
                if self.is_white_piece(x_move, y_move) == is_white:
                    continue
                else:
                    moves.append(move)
                    continue
            moves.append(move)

    def generate_rook_moves(self, x, y, moves):
        direction = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        is_white = self.is_white_piece(x, y)

        for dx, dy in direction:
            for k in range(1, SIZE):
                x_move = x + k * dx
                y_move = y + k * dy
                move = (x, y, x_move, y_move)
                if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                    continue
                if self.board[y_move][x_move] != 0:
                    if self.is_white_piece(x_move, y_move) == is_white:
                        break
                    else:
                        moves.append(move)  ## capture
                        break
                moves.append(move)
    def generate_queen_moves(self, x, y, moves):
        direction = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        is_white = self.is_white_piece(x, y)

        for dx, dy in direction:
            for k in range(1, SIZE):
                x_move = x + k * dx
                y_move = y + k * dy
                move = (x, y, x_move, y_move)
                if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                    continue
                if self.board[y_move][x_move] != 0:
                    if self.is_white_piece(x_move, y_move) == is_white:
                        break
                    else:
                        moves.append(move)  ## capture
                        break
                moves.append(move)
    def generate_king_moves(self, x, y, moves, checking):
        direction = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        is_white = self.is_white_piece(x, y)

        for dx, dy in direction:
            x_move = x + dx
            y_move = y + dy
            move = (x, y, x_move, y_move)
            if not (x_move >= 0 and y_move >= 0 and x_move < SIZE and y_move < SIZE):
                continue
            if self.board[y_move][x_move] != 0:
                if self.is_white_piece(x_move, y_move) == is_white:
                    continue
                else:
                    moves.append(move)
                    continue
            moves.append(move)

        if is_white:
            row = 7
        else:
            row = 0

        if not checking:
            if self.queen_castling_rights(is_white):
                if self.is_queen_castling_possible(is_white):
                    moves.append((x, y, 2, row))

            if self.king_castling_rights(is_white):
                if self.is_king_castling_possible(is_white):
                    moves.append((x, y, 6, row))

    def delete_moves_with_check(self, moves, color):
        copy_board = copy.deepcopy(self.board)
        copy_info = copy.deepcopy(self.info)
        valid_moves = []  # Collect only the valid moves

        new_engine = Engine(copy_board, copy_info)

        for move in moves:

            # Make the move on the copy of the board
            if len(move) == 5:
                piece, is_white, changes, last2_move = new_engine.move_board(move[0], move[1], move[2], move[3],
                                                                             move[4])
            else:
                piece, is_white, changes, last2_move = new_engine.move_board(move[0], move[1], move[2], move[3])

            new_engine.update_valid_moves(True)

            # Check if the move results in a check for the current player
            if not new_engine.is_check(is_white):  # Valid if it doesn't put the king in check
                valid_moves.append(move)
            # Undo the move to restore the original board state
            new_engine.undo_move_board(move[0], move[1], move[2], move[3], piece, is_white, changes, last2_move)
            new_engine.update_valid_moves(True)

        return valid_moves

    def valid_moves(self,x,y, checking = False):
        piece = self.get_figure(x, y)
        moves = []
        if piece is None:
            return moves

        if x < 0 and y < 0 or x >= SIZE or y >= SIZE:
            return moves

        color = 1 if self.is_white_piece(x,y) else -1

        ## Ruchy pionkiem
        if abs(piece) == 1:
            self.generate_pawn_moves(x,y, piece, moves, color)

        ## Ruchy skoczkiem
        if abs(piece) == 3:
            self.generate_knight_moves(x, y, moves)

        ## Ruchy gońcem
        if abs(piece) == 4:
            self.generate_bishop_moves(x, y, moves)

        ## Ruchy wieżą
        if abs(piece) == 5:
            self.generate_rook_moves(x, y, moves)

        ## Ruchy królową
        if abs(piece) == 9:
            self.generate_queen_moves(x, y, moves)

        ## Ruchy królem(wraz z roszadą)
        if abs(piece) == 2:
            self.generate_king_moves(x, y, moves, checking)

        # Usuwanie tych ruchów, po których wykonaniu król jest szachowany.
        if not checking:
            valid_moves = self.delete_moves_with_check(moves, color)

            return valid_moves

        return moves

    def castle(self, start_x, start_y, end_x, color):
        if start_x - end_x == 2:  # Castling long
            self.board[start_y][2] = 2 * color
            self.board[start_y][4] = 0
            self.board[start_y][3] = 5 * color
            self.board[start_y][0] = 0
        elif start_x - end_x == -2:  # Castling short
            self.board[start_y][6] = 2 * color
            self.board[start_y][4] = 0
            self.board[start_y][5] = 5 * color
            self.board[start_y][7] = 0

    def promotion(self, start_x, start_y, end_x, end_y, color, promotion):
        self.info[6] = True
        self.board[end_y][end_x] = promotion * color
        self.board[start_y][start_x] = 0

    def enpassant(self, start_x, start_y, end_x, end_y, color, piece_from):
        self.board[end_y][end_x] = piece_from
        self.board[start_y][start_x] = 0
        self.board[end_y + color][end_x] = 0
        self.info[7] = True

    def regular_move(self,start_x, start_y, end_x, end_y, piece_from):
        if piece_from != 0:
            self.board[end_y][end_x] = piece_from
            self.board[start_y][start_x] = 0

    def update_info_castling_rights(self, start_x, end_x, changes, is_white, piece_from, piece_to):
        if abs(piece_from) == 2:

            if self.queen_castling_rights(is_white):
                self.change_queen_castling_rights(is_white, False)
                changes[0] = True  # change of rigths for castling to enable undo_move

            if self.king_castling_rights(is_white):
                self.change_king_castling_rights(is_white, False)
                changes[1] = True

                # ruch wieżą
        if abs(piece_from) == 5:
            if start_x == 0:  # left_rook
                if self.queen_castling_rights(is_white):
                    self.change_queen_castling_rights(is_white, False)
                    changes[0] = True
            if start_x == 7:  # right_rook
                if self.king_castling_rights(is_white):
                    self.change_king_castling_rights(is_white, False)
                    changes[1] = True

        # zbicie wieży przez przeciwnika
        if abs(piece_to) == 5:
            if end_x == 0:
                if self.queen_castling_rights(is_white):
                    self.change_queen_castling_rights(is_white, False)
                    changes[0] = True
            if end_x == 7:
                if self.king_castling_rights(is_white):
                    self.change_king_castling_rights(is_white, False)
                    changes[1] = True
    def move_board(self, start_x, start_y, end_x, end_y, promotion = None):
        is_white = self.is_white_piece(start_x, start_y)
        piece_from = self.get_figure(start_x, start_y)
        piece_to = self.get_figure(end_x, end_y)

        color = 1 if is_white else -1

        prev_promotion = self.info[6]
        prev_enpassant = self.info[7]
        self.info[6] = False # promotion
        self.info[7] = False # enpassant move

        prev_50 = self.update_fifty_move_rule(start_x, start_y, end_x, end_y)
        prev_score = self.info[10]

        # [queen_castling_rigths, king_castling_rigths, prev_50_move, promotion, enpassant]
        changes = [False, False, prev_50, prev_promotion, prev_enpassant, prev_score]

        if self.is_it_capture(end_x, end_y):
            self.info[10] -= piece_to


        if self.is_castling(start_x, start_y, end_x, end_y, piece_from):
            self.castle(start_x, start_y, end_x, color)

        elif self.is_pawn_promotion(start_x, start_y, end_x, end_y):
            self.promotion(start_x, start_y, end_x, end_y, color, promotion)

        elif self.is_enpassant(start_x, start_y, end_x, end_y, piece_from):
            self.enpassant(start_x, start_y, end_x, end_y, color, piece_from)
        else:
            self.regular_move(start_x, start_y, end_x, end_y, piece_from)


        last2_move = self.info[4]
        last_move = self.info[5] # now last move is previous move
        self.info[4] = last_move
        self.info[5] = (start_x, start_y, end_x, end_y)

        self.update_info_castling_rights(start_x, end_x, changes, is_white, piece_from, piece_to)

        return piece_to, is_white, changes, last2_move


    def update_valid_moves(self,checking = False):
        # ## zapisywanie valid_mmoves
        self.last_valid_moves_white = self.valid_moves_white
        self.last_valid_moves_black = self.valid_moves_black
        self.valid_moves_white = self.all_valid_moves(True,checking)
        self.valid_moves_black = self.all_valid_moves(False,checking)

    def update_valid_moves_white(self,checking = False):
        self.last_valid_moves_white = self.valid_moves_white
        self.valid_moves_white = self.all_valid_moves(True,checking)

    def update_valid_moves_black(self,checking = False):
        self.last_valid_moves_black = self.valid_moves_black
        self.valid_moves_black = self.all_valid_moves(False,checking)

    def undo_update_valid_moves(self):
        self.valid_moves_white = self.last_valid_moves_white
        self.valid_moves_black = self.last_valid_moves_black
        self.last_valid_moves_white = None
        self.last_valid_moves_black = None

    def undo_valid_moves_white(self):
        self.valid_moves_white = self.last_valid_moves_white
        self.last_valid_moves_white = None

    def undo_valid_moves_black(self):
        self.valid_moves_black = self.last_valid_moves_black
        self.last_valid_moves_black = None

    def undo_castlig_right_changes(self, changes, is_white):
        if changes[0]:
            self.change_queen_castling_rights(is_white, True)
        if changes[1]:
            self.change_king_castling_rights(is_white, True)

    def uncastle(self, start_x, start_y, end_x, end_y, color):
        if start_x - end_x == 2:  # Castling long
            self.board[start_y][0] = 5 * color
            self.board[start_y][2] = 0
            self.board[start_y][3] = 0
            self.board[start_y][4] = 2 * color
        elif start_x - end_x == -2:  # Castling short
            self.board[start_y][4] = 2 * color
            self.board[start_y][5] = 0
            self.board[start_y][6] = 0
            self.board[start_y][7] = 5 * color

    def undo_enpassant(self,  start_x, start_y, end_x, end_y, color, piece_from):
        self.board[end_y][end_x] = 0
        self.board[start_y][start_x] = piece_from
        self.board[end_y + color][end_x] = -color

    def undo_regular_move(self, start_x, start_y, end_x, end_y, color, piece_from, piece):
        piece_from = self.get_figure(end_x, end_y)
        if piece_from != 0:
            self.board[start_y][start_x] = piece_from
            self.board[end_y][end_x] = piece
    def undo_move_board(self, start_x, start_y, end_x, end_y, piece, is_white,changes, last2_move):
        self.undo_castlig_right_changes(changes, is_white)

        self.info[5] = self.info[4] ## cofanie aktualnego ruchu na ostatni ruchu
        self.info[4] = last2_move


        color = 1 if is_white else -1

        piece_from = self.get_figure(end_x, end_y)

        if self.is_castling(start_x, start_y, end_x, end_y, piece_from):
            self.uncastle(start_x, start_y, end_x, end_y, color)
        elif self.info[7]: # enpssant
            self.undo_enpassant(start_x, start_y, end_x, end_y, color, piece_from)
        else:
           self.undo_regular_move(start_x, start_y, end_x, end_y, color, piece_from, piece)

        self.info[6] = changes[3] # cofanie promocji
        self.info[7] = changes[4] # cofanie enpassant
        self.info[9] = changes[2] # cofanie zasady 50 ruchow
        self.info[10] = changes[5] # cofanie score

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

