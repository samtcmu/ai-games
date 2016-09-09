import picking_cans_board
import termcolor

class RadiusOneAgentState():
    def __init__(self, state):
        self._state = state

    @staticmethod
    def AgentStateForCell(board, r, c):
        # Contets of the 3x3 matrix returned to represent the current state of
        # the agent. The current position of the agent is the cell labeled "2".
        #  | 0 | 1 | 2 |
        #  | 3 | 4 | 5 |
        #  | 6 | 7 | 8 |
        radius = RadiusOneAgentState.VisibleRadius()
        diameter = RadiusOneAgentState.VisibleDiameter()
        state = [[None for _ in range(diameter)] for _ in range(diameter)]
        for i in range(diameter):
            for j in range(diameter):
                state[i][j] = board.GetContents((r - radius) + i,
                                                (c - radius) + j)
        return RadiusOneAgentState(state)

    @staticmethod
    def AgentStateForBoardPosition(position):
        len_cells = len(picking_cans_board.CELLS)

        # Exponent of 2 for each board position relative to current position
        # (where 2 is).
        #  | 0 | 1 | 2 |
        #  | 3 | 4 | 5 |
        #  | 6 | 7 | 8 |
        diameter = RadiusOneAgentState.VisibleDiameter()
        state = [[None for _ in range(diameter)] for _ in range(diameter)]
        for i in range(diameter):
            for j in range(diameter):
                exponent = (diameter * i) + j
                state[i][j] = (position / (len_cells ** exponent)) % len_cells
        return RadiusOneAgentState(state)

    @staticmethod
    def VisibleRadius():
        return 1

    @staticmethod
    def VisibleDiameter():
        return (2 * RadiusOneAgentState.VisibleRadius()) + 1

    @staticmethod
    def NumberOfVisibleCells():
        # The agent can view the numbered cells relative to its current
        # location (cell labeled 2).
        #  | 0 | 1 | 2 |
        #  | 3 | 4 | 5 |
        #  | 6 | 7 | 8 |
        return RadiusOneAgentState.VisibleDiameter()**2

    @staticmethod
    def NumberOfStates():
        return (len(picking_cans_board.CELLS)**
                RadiusOneAgentState.NumberOfVisibleCells())

    def __str__(self):
        output = []
        color_for_board_contents_function = (
            picking_cans_board.Board.ColorForBoardContents)
        for row in self._state:
            output.append([])
            for cell in row:
                if cell is not None:
                    output[-1].append(termcolor.colored(
                        "  ", on_color=color_for_board_contents_function(cell)))
                else:
                    output[-1].append("  ")

            # Handle placing the separators.
            output[-1] = (("|" if row[0] is not None else " ") +
                          "|".join(output[-1]) +
                          ("|" if row[-1] is not None else " "))

        return "\n".join(output)

    def __int__(self):
        # Exponent of 2 for each board cell relative to current cell
        # (where 2 is).
        #  | 0 | 1 | 2 |
        #  | 3 | 4 | 5 |
        #  | 6 | 7 | 8 |
        diameter = RadiusOneAgentState.VisibleDiameter()
        output = 0
        for i in range(diameter):
            for j in range(diameter):
                exponent = (diameter * i) + j
                output += ((len(picking_cans_board.CELLS) ** exponent) *
                           self._state[i][j])
        return output

    def GetContents(self, r, c):
        return self._state[r][c]
