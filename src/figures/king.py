from src import constants
from src.figures import utils


class King:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def get_moves(self, board, x, y):
        moves = []
        y += -1 if self.color == constants.WHITE else 1
        piece = board.get_piece
        if y == -1 or y == 8:
            return moves
        if x > 0 and board.get_color(x - 1, y) == utils.opponent(self.color):
            moves.append([x - 1, y])
        if x < 7 and board.get_piece.color(x + 1, y) == utils.opponent(self.color):
            moves.append([x + 1, y])
        if not board.get_piece(x, y):
            moves.append([x, y])
            if self.color == constants.WHITE and y == 5 and not board.get_piece(x, y - 1):
                moves.append([x, y - 1])
            if self.color == constants.BLACK and y == 2 and not board.get_piece(x, y - 1):
                moves.append([x, y + 1])
        return moves

    def can_move(self, board, row, col, row1, col1):
        if abs(row - row1) > 1 or abs(col - col1) > 1 or row1 > 8 or col1 > 8:
            return False
        if board.field[row1][col1] is None and utils.correct_coords(row1, col1):
            board.castling_0.add(self.color)
            board.castling_7.add(self.color)
            return True
        if utils.correct_coords(row1, col1):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
