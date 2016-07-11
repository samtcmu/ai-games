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
        return ((0 <= r <= self._rows) and
                (0 <= c <= self._columns) and
                self._board[r][c])

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

ACTION_PICK_UP_CAN = 0
ACTION_UP = 1
ACTION_DOWN = 2
ACTION_RIGHT = 3
ACTION_LEFT = 4
ACTIONS = [
    ACTION_PICK_UP_CAN,
    ACTION_UP,
    ACTION_DOWN,
    ACTION_RIGHT,
    ACTION_LEFT,
]

class Model:
    #     |  |
    #  |  |  |  |
    #     |  |
    def __init__(self, actions = None):
        if actions is None:
            self._actions = [ACTION_UP for _ in range(32)]
        else:
            self._actions = actions

    def Randomize(self):
        for i in range(32):
            self._actions[] = ACTIONS[random.randint(0, len(ACTIONS))]

    def ActionForCurrentPosition(self, board, r, c):
        position = 0
        position += (1 << 1) * board.ContainsCan(r - 1, c)
        position += (1 << 2) * board.ContainsCan(r, c - 1)
        position += (1 << 3) * board.ContainsCan(r, c)
        position += (1 << 4) * board.ContainsCan(r, c + 1)
        position += (1 << 5) * board.ContainsCan(r + 1, c)
        return self._actions[position]

def main():
    board = Board(10, 10)
    board.Randomize()
    model = Model()
    model.Randomize()
    print board
