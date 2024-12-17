from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHeaderView, QTableWidgetItem, QFileDialog, QInputDialog
from stockfish import Stockfish


from src.figures import utils
from src import figures, constants


class Board:
    def __init__(self):
        self.color = constants.WHITE
        self.field = []
        self.castling_0 = set()
        self.castling_7 = set()
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            figures.Rook(constants.BLACK), figures.Knight(constants.BLACK), figures.Bishop(constants.BLACK), figures.Queen(constants.BLACK),
            figures.King(constants.BLACK), figures.Bishop(constants.BLACK), figures.Knight(constants.BLACK), figures.Rook(constants.BLACK)
        ]
        self.field[1] = [
            figures.Pawn(constants.BLACK), figures.Pawn(constants.BLACK), figures.Pawn(constants.BLACK), figures.Pawn(constants.BLACK),
            figures.Pawn(constants.BLACK), figures.Pawn(constants.BLACK), figures.Pawn(constants.BLACK), figures.Pawn(constants.BLACK)
        ]
        self.field[6] = [
            figures.Pawn(constants.WHITE), figures.Pawn(constants.WHITE), figures.Pawn(constants.WHITE), figures.Pawn(constants.WHITE),
            figures.Pawn(constants.WHITE), figures.Pawn(constants.WHITE), figures.Pawn(constants.WHITE), figures.Pawn(constants.WHITE)
        ]
        self.field[7] = [
            figures.Rook(constants.WHITE), figures.Knight(constants.WHITE), figures.Bishop(constants.WHITE), figures.Queen(constants.WHITE),
            figures.King(constants.WHITE), figures.Bishop(constants.WHITE), figures.Knight(constants.WHITE), figures.Rook(constants.WHITE)
        ]

    def castling0(self):
        if self.color in self.castling_0:
            return False
        if self.color == constants.WHITE:
            for i in range(1, 4):
                if not (self.get_piece(0, i) is None):
                    return False
            if type(self.field[0][0]) != figures.Rook or type(self.field[0][4]) != figures.King:
                return False
            self.field[0][0] = None
            self.field[0][4] = None
            self.field[0][3] = figures.Rook(constants.WHITE)
            self.field[0][2] = figures.King(constants.WHITE)
        else:
            for i in range(1, 4):
                if not (self.get_piece(7, i) is None):
                    return False
            if type(self.field[7][0]) != figures.Rook or type(self.field[7][4]) != figures.King:
                return False
            self.field[7][0] = None
            self.field[7][4] = None
            self.field[7][3] = figures.Rook(constants.BLACK)
            self.field[7][2] = figures.King(constants.BLACK)
        self.color = utils.opponent(self.color)
        return True

    def castling7(self):
        if self.color in self.castling_7:
            return False
        if self.color == constants.WHITE:
            for i in range(5, 7):
                if not (self.get_piece(7, i) is None):
                    return False
            if type(self.field[0][7]) != figures.Rook or type(self.field[0][4]) != figures.King:
                return False
            self.field[0][7] = None
            self.field[0][4] = None
            self.field[0][5] = figures.Rook(constants.WHITE)
            self.field[0][6] = figures.King(constants.WHITE)
        else:
            for i in range(5, 7):
                if not (self.get_piece(7, i) is None):
                    return False
            if type(self.field[7][7]) != figures.Rook or type(self.field[7][4]) != figures.King:
                return False
            self.field[7][7] = None
            self.field[7][4] = None
            self.field[7][5] = figures.Rook(constants.BLACK)
            self.field[7][6] = figures.King(constants.BLACK)
        self.color = utils.opponent(self.color)
        return True

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '　'
        color = piece.get_color()
        c = 'w' if color == constants.WHITE else 'b'
        return constants.SIGNS[c + piece.char()]

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False"""
        if not utils.correct_coords(row, col) or not utils.correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if self.king_is_under_attack(constants.WHITE, row, col, row1, col1) and piece.get_color() == constants.WHITE:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                if piece.get_color() == constants.BLACK:
                    return self.castling_0() if col == 3 else self.castling_7
                return False
        elif self.field[row1][col1].get_color() == utils.opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = utils.opponent(self.color)
        return True

    def get_piece(self, row, col):
        if utils.correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def king_is_under_attack(self, color, row, col, row1, col1):
        for r in range(8):
            for c in range(8):
                if type(self.field[r][c]) == figures.King:
                    piece = self.field[row2 := r][col2 := c]
                    if type(self.field[row][col]) == figures.King:
                        if self.is_under_attack(row1, col1, utils.opponent(color)):
                            return True
                        return False
                    if self.is_under_attack(row2, col2, utils.opponent(piece.get_color())):
                        return piece.get_color() == color

    def is_under_attack(self, row, col, color):
        for r in range(8):
            for c in range(8):
                piece = self.field[r][c]
                if piece is None:
                    continue
                if piece.get_color() == color and piece.can_move(self, r, c, row, col):
                    return True
        return False
