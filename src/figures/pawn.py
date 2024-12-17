from src import constants


class Pawn:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False

        if self.color == constants.WHITE:
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        if row + direction == row1:
            return True

        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = -1 if (self.color == constants.WHITE) else 1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))
