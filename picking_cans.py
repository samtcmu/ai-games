import random
import termcolor

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

class Board:
    def __init__(self, rows, columns, board=None):
        self._rows = rows
        self._columns = columns
        if board is None:
            self._board = [[False for _ in range(columns)] for _ in range(rows)]
        else:
            self._board = board

        # Current position.
        self._r, self._c = (0, 0)

    def __str__(self):
        output = ""
        for r in range(self._rows):
            for c in range(self._columns):
                color = "on_yellow"
                if self.ContainsCan(r, c):
                    color = "on_red"
                current_position_str = "  "
                if (r == self._r) and (c == self._c):
                    current_position_str = "<>"
                output += "|" + termcolor.colored(current_position_str,
                                                  on_color=color)
            output += "|\n"
        return output

    def Randomize(self):
        for r in range(self._rows):
            for c in range(self._columns):
                self._board[r][c] = random.randint(0, 1) % 2

    def RandomizeCurrentPosition(self):
        self._r = random.randint(0, self._rows - 1)
        self._c = random.randint(0, self._columns - 1)

    def ContainsCan(self, r, c):
        return ((0 <= r < self._rows) and
                (0 <= c < self._columns) and
                self._board[r][c])

    def PickUpCan(self):
        if self.ContainsCan(self._r, self._c):
            self._board[self._r][self._c] = False
            return 1
        return 0

    def MoveUp(self):
        if self._r > 0:
            self._r -= 1
            return 0
        return -1

    def MoveDown(self):
        if self._r < self._rows:
            self._r += 1
            return 0
        return -1

    def MoveRight(self):
        if self._c < self._columns:
            self._c += 1
            return 0
        return -1

    def MoveLeft(self):
        if self._c > 0:
            self._c -=1 
            return 0
        return -1

    def PickCansWithModel(self, model, time_limit=200, verbose=False):
        score = 0
        for t in range(time_limit):
            if verbose:
                print (t, score)
                print self

            action = model.ActionForCurrentPosition(self, self._r, self._c)
            if action == ACTION_PICK_UP_CAN:
                score += self.PickUpCan()
            elif action == ACTION_UP:
                score += self.MoveUp()
            elif action == ACTION_DOWN:
                score += self.MoveDown()
            elif action == ACTION_RIGHT:
                score += self.MoveRight()
            elif action == ACTION_LEFT:
                score += self.MoveLeft()

        return score

class Model:
    def __init__(self, actions = None):
        if actions is None:
            self._actions = [ACTION_UP for _ in range(32)]
        else:
            self._actions = actions

    def __str__(self):
        return str(self._actions)

    def Randomize(self):
        for i in range(32):
            self._actions[i] = ACTIONS[random.randint(0, len(ACTIONS) - 1)]

    def ActionForCurrentPosition(self, board, r, c):
        # Exponent of 2 for each board position relative to current position
        # (where 4 is).
        #      | 0 |
        #  | 1 | 2 | 3 |
        #      | 4 |
        position = 0
        position += (1 << 0) * board.ContainsCan(r - 1, c)
        position += (1 << 1) * board.ContainsCan(r, c - 1)
        position += (1 << 2) * board.ContainsCan(r, c)
        position += (1 << 3) * board.ContainsCan(r, c + 1)
        position += (1 << 4) * board.ContainsCan(r + 1, c)
        return self._actions[position]

def main():
    board = Board(10, 10)
    board.Randomize()
    board.RandomizeCurrentPosition()
    print board
    model = Model()
    model.Randomize()
    print model

    print "\nscore: %d" % (board.PickCansWithModel(model),)
    print board
