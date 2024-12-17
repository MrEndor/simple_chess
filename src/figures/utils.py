from PIL import Image
from src import constants


def opponent(color):
    if color == constants.WHITE:
        return constants.BLACK
    return constants.WHITE


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def print_board(board):
    print('     +––––+–––––+––––+–––––+––––+–––––+––––+–––––+')
    for row in range(8):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
            if col != 7:
                print("|", end="")
        print('|')
        print('     +––––+–––––+––––+–––––+––––+–––––+––––+–––––+')
    print(end='  　    ')
    for letter in "ABCDEFGH":
        print(letter, end='　   ')
    print()


def save_image(board, track):
    im = Image.open("images/desk.png")
    for row in range(8):
        for col in range(8):
            im2 = constants.IMAGES.get(board.cell(row, col), False)
            if im2:
                im2 = Image.open(im2)
                x, y = im2.size
                im2.thumbnail((x, y))
                im.paste(im2, (71 + 86 * col, 85 * row - 50), mask=im2)
    im.save(track)


def return_cell(x, y):
    letters = "abcdefgh"
    nums = "12345678"
    x, y = (x - 90) // 86, (y - 120) // 85
    if 0 <= x <= 7 and 0 <= y <= 7:
        return letters[x], nums[y]
    return letters[0], nums[0]


def return_cell_num(x, y):
    x, y = (x - 90) // 86, (y - 120) // 85
    if 0 <= x <= 7 and 0 <= y <= 7:
        return x, y
    return None
