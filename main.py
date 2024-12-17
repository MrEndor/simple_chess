import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QHeaderView,
    QTableWidgetItem, QFileDialog, QInputDialog
)
from stockfish import Stockfish
from PyQt5 import uic
import csv

from src.board import Board
from src.constants import IMAGES, NUMTOLET, MOVES, BLACK, WHITE, NAME, DIRECTORY
from src.figures.utils import save_image, print_board, return_cell_num


class Chess(QMainWindow):
    def __init__(self):
        super(Chess, self).__init__()
        self.stockfish = Stockfish(path="third_party\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
        uic.loadUi("template\design.ui", self)
        self.setWindowTitle("Шахматы PyQt с ИИ")
        self.figure_chosed = 0
        self.figure = 0
        self.lab = QLabel(self)
        self.lab.move(10, 33)
        self.lab.resize(150, 25)
        self.pixmap = QPixmap("images/desk.png")
        self.desk.setPixmap(self.pixmap)
        self.board = Board()
        self.field = []
        self.place_figures()
        self.steps = []
        for elem in (self.level, self.take_hint, self.save):
            elem.setStyleSheet("""background-color: 'white';
                                    border-radius: 15px; 
                                    outline: 2px solid #CCC;
                                    """)
        with open("steps.csv", "w", encoding="utf8") as csv_file:
            writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(title := ["Игрок", "Откуда", "Куда"])
            self.steps_table.setColumnCount(len(title))
            self.steps_table.setHorizontalHeaderLabels(title)
            self.steps_table.setRowCount(0)
            self.steps_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.steps_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.take_hint.clicked.connect(self.hint)
        self.save.clicked.connect(self.save_file)
        self.save_file_1.triggered.connect(self.save_file)
        self.save_photo.triggered.connect(self.save_photo_)
        self.correct_name.triggered.connect(self.cor_name)
        self.direct.triggered.connect(self.cor_dir)
        self.chose_level.triggered.connect(self.cor_level)
        self.level.clicked.connect(self.cor_level)

    def cor_level(self):
        try:
            num, ok_pressed = QInputDialog.getText(self, "Введите число",
                                                   "Введите число от 1 до 25")
            if ok_pressed:
                self.stockfish.set_skill_level(int(num))
        except Exception as e:
            print(e)

    def cor_dir(self):
        global DIRECTORY
        try:
            fname = QFileDialog.getExistingDirectory(self, 'Выбрать папку', f'{DIRECTORY}')
            DIRECTORY = fname[0]
        except Exception as e:
            print(e)

    def cor_name(self):
        global NAME
        name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                "Как к вам обращаться?")
        if ok_pressed:
            NAME = name

    def save_photo_(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Создать картинку', f'{DIRECTORY}\\res', 'Картинка (*.png);;'
                                                                                               'Картинка (*.jpeg);;'
                                                                                               'Картинка (*.jpg);;'
                                                                                               'Все файлы (*)')
            save_image(self.board, fname[0])
        except Exception as e:
            print(e)

    def hint(self):
        self.condition.setText(self.stockfish.get_best_move())

    def save_file(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Создать файл', f'{DIRECTORY}\\file',
                                                'Таблица (*.csv);;Все файлы (*)')
            with open("steps.csv", "r", encoding="utf-8") as csv_input:
                with open(fname[0], "w", encoding="utf-8") as csv_output:
                    for line in csv_input:
                        csv_output.write(line)
        except Exception as e:
            print(e)

    def steps_checker(self, step, ai):
        with open("steps.csv", encoding="utf8") as csv_file:
            reader = csv.reader(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            rows = list(reader)
            with open("steps.csv", "w", encoding="utf8") as csv_file:
                writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                rows.append([("Компьютер" if ai else NAME), step[:2], step[2:]])
                rows = [row for row in rows if row]
                for i, row in enumerate(rows[1:]):
                    self.steps_table.setRowCount(
                        len(rows[1:]) + 1)
                    for j, elem in enumerate(row):
                        self.steps_table.setItem(
                            i, j, QTableWidgetItem(elem))
                self.steps_table.resizeColumnToContents(0)
                writer.writerows(rows)

    def place_figures(self):
        self.field = []
        print_board(self.board)
        for i in range(len(self.board.field)):
            row = []
            for j in range(len(self.board.field[i])):
                figure = self.board.field[i][j]
                if figure is not None:
                    pixmap = QPixmap(IMAGES[self.board.cell(i, j)])
                    label = QLabel(self)
                    label.resize(116, 268)
                    label.setPixmap(pixmap)
                    label.move(90 + 86 * j, 85 * i)
                    row.append(label)
                else:
                    row.append(None)
            self.field.append(row)

    def replace_figures(self):
        print_board(self.board)
        for i in range(len(self.board.field)):
            for j in range(len(self.board.field[i])):
                figure = self.board.field[i][j]
                if figure is not None:
                    label = self.field[i][j]
                    if not label:
                        pixmap = QPixmap(IMAGES[self.board.cell(i, j)])
                        label = QLabel(self)
                        label.resize(116, 268)
                        label.setPixmap(pixmap)
                        self.field[i][j] = label
                        label = self.field[i][j]
                    label.move(90 + 86 * j, 85 * i)
                    label.raise_()
                elif self.field[i][j] is not None:
                    self.field[i][j].hide()
                    self.field[i][j] = None

    def move_piece(self, row, col, row1, col1):
        figure = self.field[row][col]
        self.steps.append("".join((NUMTOLET[col], str(8 - row), NUMTOLET[col1], str(8 - row1))).lower())
        self.steps_checker("".join((NUMTOLET[col], str(8 - row), NUMTOLET[col1], str(8 - row1))).lower(), 0)
        self.stockfish.set_position([*self.steps])
        self.field[row][col] = None
        if self.field[row1][col1]:
            self.field[row1][col1].hide()
        self.field[row1][col1] = figure
        if self.board.king_is_under_attack(WHITE, row, col, row1, col1):
            self.condition.setText("Вам шах!")

        self.steps.append(move := self.stockfish.get_best_move())
        self.stockfish.set_position([*self.steps])

        col, row, col1, row1 = list(move)
        row, col, row1, col1 = int(row) - 1, MOVES[col], int(row1) - 1, MOVES[col1]
        self.steps_checker(move, 1)
        figure = self.field[7 - row][col]
        if self.field[7 - row1][col1]:
            self.field[7 - row1][col1].hide()
        self.field[7 - row1][col1] = figure
        self.field[7 - row][col] = None
        self.board.move_piece(7 - row, col, 7 - row1, col1)
        if self.board.king_is_under_attack(BLACK, row, col, row1, col1):
            self.condition.setText("Шах!")

    def mouseReleaseEvent(self, event):
        try:
            if self.board.move_piece(*self.figure_chosed[::-1], *self.coords):
                self.move_piece(*self.figure_chosed[::-1], *self.coords)
                self.condition.setText("Ход успешен")
            self.replace_figures()
            self.figure_chosed, self.figure = None, None
        except Exception as e:
            print(e)
            self.replace_figures()
            self.figure_chosed, self.figure = None, None

    def mouseMoveEvent(self, event):
        if return_cell_num(event.x(), event.y()):
            letter, num = return_cell_num(event.x(), event.y())
            if not self.figure_chosed:
                self.figure_chosed = (letter, num)
                self.figure = self.field[num][letter]
            if self.figure:
                self.figure.move(86 * (event.x() // 86) + 90, event.y() - 150)
            if self.figure_chosed and self.figure is not None:
                self.figure.move(event.x(), event.y())
                self.coords = return_cell_num(event.x(), event.y())[::-1]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chess = Chess()
    chess.show()
    sys.exit(app.exec())