###############
## NOTATION ##
## QUEEN - 9
## ROOK - 5
## BISHOP - 4
## KNIGHT - 3
## KING - 2
## PAWN - 1

class Board:
    def __init__(self):
        self.board = [
            [5, 3, 4, 9, 2, 4, 3, 5]
            [1, 1, 1, 1, 1, 1, 1, 1]
            [0, 0, 0, 0, 0, 0, 0, 0]
            [0, 0, 0, 0, 0, 0, 0, 0]
            [0, 0, 0, 0, 0, 0, 0, 0]
            [0, 0, 0, 0, 0, 0, 0, 0]
            [1, 1, 1, 1, 1, 1, 1, 1]
            [5, 3, 4, 9, 2, 4, 3, 5]
        ]

    def display_board(self):
        pass

    def move(self, start, end):
        # check if the move is valid
        # if valid, make the move
        # if not valid, raise an error
        pass

    def pawn_promotion(self, pawn, new_piece):
        pass

    def castling(self):
        pass