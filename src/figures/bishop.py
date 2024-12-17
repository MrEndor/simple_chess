class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        return abs(row - row1) == abs(col - col1)

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
