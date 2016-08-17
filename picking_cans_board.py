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

CELL_EMPTY = 0
CELL_CONTAINS_CAN = 1
CELL_WALL = 2
CELLS = [
    CELL_EMPTY,
    CELL_CONTAINS_CAN,
    CELL_WALL,
]

class Board:
    def __init__(self, rows, columns, board=None):
        self._rows = rows
        self._columns = columns
        if board is None:
            self._board = [[CELL_EMPTY for _ in range(columns)] for _ in range(rows)]
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
                self._board[r][c] = CELLS[random.randrange(len(CELLS))]

    def RandomizeCurrentPosition(self):
        self._r = random.randint(0, self._rows - 1)
        self._c = random.randint(0, self._columns - 1)

    def BoardPosition(self, r, c):
        # Exponent of 2 for each board position relative to current position
        # (where 4 is).
        #      | 0 |
        #  | 1 | 2 | 3 |
        #      | 4 |
        position = 0
        position += (len(CELLS) ** 0) * self.GetContents(r - 1, c)
        position += (len(CELLS) ** 1) * self.GetContents(r, c - 1)
        position += (len(CELLS) ** 2) * self.GetContents(r, c)
        position += (len(CELLS) ** 3) * self.GetContents(r, c + 1)
        position += (len(CELLS) ** 4) * self.GetContents(r + 1, c)
        return position

    def CurrentBoardPosition(self):
        return self.BoardPosition(self._r, self._c)

    def GetContents(self, r, c):
        if (0 <= r < self._rows) and (0 <= c < self._columns):
            return self._board[r][c]
        return CELL_WALL

    def ContainsCan(self, r, c):
        return CELL_CONTAINS_CAN == self.GetContents(r, c)

    def PickUpCan(self):
        if self.ContainsCan(self._r, self._c):
            self._board[self._r][self._c] = CELL_EMPTY
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
        return move_actions[random.randrange(len(move_actions))]()

    def PickCansWithModel(self, model, actions_per_game=200, verbose=False):
        score = 0
        for t in range(actions_per_game):
            initial_position = self.CurrentBoardPosition()
            action = model.ActionForPosition(initial_position)
            if verbose:
                print "time: %d\nscore: %d\naction: %s\nposition: %d" % (
                    t, score, ACTIONS[action][1], initial_position)
                print self
                print model

            reward = 0
            if action == ACTION_PICK_UP_CAN:
                reward = self.PickUpCan()
            elif action == ACTION_UP:
                reward = self.MoveUp()
            elif action == ACTION_DOWN:
                reward = self.MoveDown()
            elif action == ACTION_RIGHT:
                reward = self.MoveRight()
            elif action == ACTION_LEFT:
                reward = self.MoveLeft()
            elif action == ACTION_STAY:
                reward = self.Stay()
            elif action == ACTION_MOVE_RANDOM:
                reward = self.MoveRandom()
            score += reward

            final_position = self.CurrentBoardPosition()
            model.Update(initial_position, action, final_position, reward, score)

        return score
