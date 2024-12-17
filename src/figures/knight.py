class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        delta_row = abs(row1 - row)
        delta_col = abs(col1 - col)
        return max(delta_col, delta_row) == 2 and min(delta_col, delta_row) == 1

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
