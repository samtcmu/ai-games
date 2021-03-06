import default_agent_state
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
    def __init__(self, rows, columns, board=None,
                 agent_state_class=default_agent_state.DefaultAgentState):
        self._rows = rows
        self._columns = columns
        if board is None:
            self._board = [[CELL_EMPTY for _ in range(columns)] for _ in range(rows)]
        else:
            self._board = board

        # Current position.
        self._r, self._c = (0, 0)

        # Count the number of cans initially on the board.
        self._num_cans = 0
        self.SetNumCans()

        self._agent_state_class = agent_state_class

    def __str__(self):
        output = ""
        for r in range(self._rows):
            for c in range(self._columns):
                color = Board.ColorForBoardContents(self.GetContents(r, c))
                current_position_str = "  "
                if (r == self._r) and (c == self._c):
                    current_position_str = "<>"
                output += "|" + termcolor.colored(current_position_str,
                                                  on_color=color)
            output += "|\n"
        return output

    @staticmethod
    def ColorForBoardContents(contents):
        colors = {
            CELL_EMPTY: "on_yellow",
            CELL_CONTAINS_CAN: "on_red",
            CELL_WALL: "on_cyan",
        }
        return colors[contents]

    def SetNumCans(self):
        self._num_cans = 0
        for r in range(self._rows):
            for c in range(self._columns):
                if self.ContainsCan(r, c):
                    self._num_cans += 1

    def Randomize(self, random_wall=False):
        inner_cells = [CELL_EMPTY, CELL_CONTAINS_CAN]
        for r in range(self._rows):
            for c in range(self._columns):
                self._board[r][c] = inner_cells[
                    random.randrange(len(inner_cells))]

        if random_wall:
            self.AddRandomWall()

        self.SetNumCans()

    def AddRandomWall(self):
        wall_start = [random.randrange(1, self._rows - 1) for _ in range(2)]
        wall_end = [random.randrange(1, self._rows - 1) for _ in range(2)]
        while True:
            self._board[wall_start[0]][wall_start[1]] = CELL_WALL
            if wall_start == wall_end:
                break

            if wall_start[0] != wall_end[0]:
                wall_start[0] += ((wall_end[0] - wall_start[0]) /
                                  abs(wall_end[0] - wall_start[0]))
            elif wall_start[1] != wall_end[1]:
                wall_start[1] += ((wall_end[1] - wall_start[1]) /
                                  abs(wall_end[1] - wall_start[1]))

    def RandomizeCurrentPosition(self):
        while True:
            self._r = random.randint(0, self._rows - 1)
            self._c = random.randint(0, self._columns - 1)
            if not self.ContainsWall(self._r, self._c):
                break

    def CurrentAgentState(self):
        return self._agent_state_class.AgentStateForCell(self, self._r, self._c)

    def GetContents(self, r, c):
        if (0 <= r < self._rows) and (0 <= c < self._columns):
            return self._board[r][c]
        return CELL_WALL

    def ContainsWall(self, r, c):
        return CELL_WALL == self.GetContents(r, c)

    def ContainsCan(self, r, c):
        return CELL_CONTAINS_CAN == self.GetContents(r, c)

    def PickUpCan(self):
        if self.ContainsCan(self._r, self._c):
            self._board[self._r][self._c] = CELL_EMPTY
            self._num_cans -= 1
            return 10
        return -1

    def MoveUp(self):
        if not self.ContainsWall(self._r - 1, self._c):
            self._r -= 1
            return 0
        return -5

    def MoveDown(self):
        if not self.ContainsWall(self._r + 1, self._c):
            self._r += 1
            return 0
        return -5

    def MoveRight(self):
        if not self.ContainsWall(self._r, self._c + 1):
            self._c += 1
            return 0
        return -5

    def MoveLeft(self):
        if not self.ContainsWall(self._r, self._c - 1):
            self._c -=1 
            return 0
        return -5

    def Stay(self):
        return 0

    def MoveRandom(self):
        move_actions = [
            self.MoveUp, self.MoveDown, self.MoveLeft, self.MoveRight]
        return move_actions[random.randrange(len(move_actions))]()

    def PickCansWithModel(self, model, actions_per_game=200,
                          completion_bonus=False, verbose=False):
        score = 0
        all_cans_bonus_reached = False
        for t in range(actions_per_game):
            initial_state = self.CurrentAgentState()
            action = model.ActionForState(initial_state)
            if verbose:
                print "time: %d\nscore: %d\n" % (t, score)
                print self
                print "action: %s" % (ACTIONS[action][1],)
                print "position: %d" % (int(initial_state),)
                print initial_state

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

            if (completion_bonus and (self._num_cans == 0) and
                (not all_cans_bonus_reached)):
                reward += score
                all_cans_bonus_reached = True

            score += reward

            final_state = self.CurrentAgentState()
            model.Update(initial_state, action, final_state, reward)

        return score
