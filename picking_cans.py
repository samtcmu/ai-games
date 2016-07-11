import random
import termcolor

class Board:
    def __init__(self, rows, columns, board=None):
        self._rows = rows
        self._columns = columns
        if board is None:
            self._board = [[False for _ in range(columns)] for _ in range(rows)]
        else:
            self._board = board

    def Randomize(self):
        for r in range(self._rows):
            for c in range(self._columns):
                self._board[r][c] = random.randint(0, 1) % 2

    def ContainsCan(self, r, c):
        return self._board[r][c]

    def __str__(self):
        output = ""
        for r in range(self._rows):
            for c in range(self._columns):
                color = "on_yellow"
                if self.ContainsCan(r, c):
                    color = "on_red"
                output += "|" + termcolor.colored("  ", on_color=color)
            output += "|\n"
        return output

def main():
    board = Board(10, 10)
    board.Randomize()
    print board
