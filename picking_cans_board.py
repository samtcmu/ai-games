import random
import termcolor

ACTION_PICK_UP_CAN = 0
ACTION_UP = 1
ACTION_DOWN = 2
ACTION_RIGHT = 3
ACTION_LEFT = 4
ACTION_STAY = 5
ACTION_MOVE_RANDOM = 6
ACTIONS = [
    (ACTION_PICK_UP_CAN, "pickup can"),
    (ACTION_UP,          "move up"),
    (ACTION_DOWN,        "move down"),
    (ACTION_RIGHT,       "move right"),
    (ACTION_LEFT,        "move left"),
    (ACTION_STAY,        "stay"),
    (ACTION_MOVE_RANDOM, "move random"),
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
            return 10
        return -1

    def MoveUp(self):
        if self._r > 0:
            self._r -= 1
            return 0
        return -5

    def MoveDown(self):
        if self._r < self._rows - 1:
            self._r += 1
            return 0
        return -5

    def MoveRight(self):
        if self._c < self._columns - 1:
            self._c += 1
            return 0
        return -5

    def MoveLeft(self):
        if self._c > 0:
            self._c -=1 
            return 0
        return -5

    def Stay(self):
        return 0

    def MoveRandom(self):
        move_actions = [
            self.MoveUp, self.MoveDown, self.MoveLeft, self.MoveRight]
        return move_actions[random.randint(0, 3)]()

    def PickCansWithModel(self, model, actions_per_game=200, verbose=False):
        score = 0
        for t in range(actions_per_game):
            action = model.ActionForCurrentPosition(self, self._r, self._c)
            if verbose:
                print "time: %d\nscore: %d\naction: %s" % (t, score, ACTIONS[action][1])
                print self

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
            elif action == ACTION_STAY:
                score += self.Stay()
            elif action == ACTION_MOVE_RANDOM:
                score += self.MoveRandom()

        return score

