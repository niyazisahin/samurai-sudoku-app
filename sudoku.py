from typing import Tuple
import xlsxwriter
import pyxel
import threading


input_text = ""
sudoku_table = []

with open("source.txt", "r") as f:
    input_text = f.readlines()

for line in input_text:

    line = line.rstrip()

    if(len(line) == 18):
        line = line[:9] + "---" + line[9:]

    if(len(line) == 9):
        line = "------" + line + "------"

    sudoku_table.append(list(line))


for line in sudoku_table:
    print(''.join(line))


class SudokuSolver(threading.Thread):
    def __init__(self, root: dict) -> None:

        self.completed = False

        threading.Thread.__init__(self)
        self.root = root
        self.x = root['x']
        self.y = root['y']                              

    def run(self):
        self.solve()

    def possible(self, x, y, n):

        

        n = str(n)

        # x = sütun // y = satır
        # dikey kontrol
        for i in range(9):
            if self.getCellValue(i, y) == n:
                return False

        # yatay kontrol
        for i in range(9):
            if self.getCellValue(x, i) == n:
                return False

        x += self.x
        y += self.y

        x1 = (x//3)*3
        y1 = (y//3)*3

        for i in range(3):
            for j in range(3):
                if sudoku_table[y1 + i][x1 + j] == n:
                    return False

        return True

    def getCellValue(self, x, y):
        return sudoku_table[self.root['y'] + y][self.root['x'] + x]

    def setCellValue(self, x, y, value):
        sudoku_table[self.root['y'] + y][self.root['x'] + x] = str(value)

    def solve(self):

        for row in range(9):
            for column in range(9):
                if self.getCellValue(column, row) == '*':
                    for value in range(1, 10):
                        if self.possible(column, row, value):
                            self.setCellValue(column, row, value)
                            self.solve()
                            if self.completed:
                                return
                            self.setCellValue(column, row, '*')
                    return

        self.completed = True
        
        return
        

s1 = SudokuSolver(dict(x=0, y=0))
s2 = SudokuSolver(dict(x=12, y=0))
s3 = SudokuSolver(dict(x=0, y=12))
s4 = SudokuSolver(dict(x=12, y=12)) 
s5 = SudokuSolver(dict(x=6, y=6))

s5.start()
s1.start()
s2.start()
s3.start()
s4.start() 


pyxel.init(210, 210)
pyxel.mouse(True)


def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()


def draw():
    pyxel.cls(7)
    for y, i in enumerate(sudoku_table):
        for x, j in enumerate(i):

            x1 = 10*x
            y1 = 10*y

            if(j == '-'):
                continue

            pyxel.rect(x1, y1, 10, 10, 0)
            pyxel.rect(x1 + 1, y1 + 1, 8, 8, 7)

            if(j != '*'):
                pyxel.text(x1+3, y1+3, j, 8)


pyxel.run(update, draw)
