import picking_cans_board
import termcolor

class RadiusOneAgentState():
    def __init__(self, state):
        self._state = state

    @staticmethod
    def AgentStateForCell(board, r, c):
        # Contets of the 3x3 matrix returned to represent the current state of
        # the agent. The current position of the agent is the cell labeled "2".
        # The cells labeled "0", "1", "3", and "4" represent the cells directly
        # above, to the left, to the rigth, and directly below respectively.
        # Cells labeled "-" are not visible to the agent.
        #  | 0 | 1 | 2 |
        #  | 3 | 4 | 5 |
        #  | 6 | 7 | 8 |
        state = [[None for _ in range(3)] for _ in range(3)]
        state[0][0] = board.GetContents(r - 1, c - 1)
        state[0][1] = board.GetContents(r - 1, c)
        state[0][2] = board.GetContents(r - 1, c + 1)
        state[1][0] = board.GetContents(r, c - 1)
        state[1][1] = board.GetContents(r, c)
        state[1][2] = board.GetContents(r, c + 1)
        state[2][0] = board.GetContents(r + 1, c - 1)
        state[2][1] = board.GetContents(r + 1, c)
        state[2][2] = board.GetContents(r + 1, c + 1)

        return RadiusOneAgentState(state)

    @staticmethod
    def AgentStateForBoardPosition(position):
        len_cells = len(picking_cans_board.CELLS)

        # Exponent of 2 for each board position relative to current position
        # (where 2 is).
        #  | 0 | 1 | 2 |
        #  | 3 | 4 | 5 |
        #  | 6 | 7 | 8 |
        state = [[None for _ in range(3)] for _ in range(3)]
        state[0][0] = (position / (len_cells ** 0)) % len_cells
        state[0][1] = (position / (len_cells ** 1)) % len_cells
        state[0][2] = (position / (len_cells ** 2)) % len_cells
        state[1][0] = (position / (len_cells ** 3)) % len_cells
        state[1][1] = (position / (len_cells ** 4)) % len_cells
        state[1][2] = (position / (len_cells ** 5)) % len_cells
        state[2][0] = (position / (len_cells ** 6)) % len_cells
        state[2][1] = (position / (len_cells ** 7)) % len_cells
        state[2][2] = (position / (len_cells ** 8)) % len_cells

        return RadiusOneAgentState(state)

    @staticmethod
    def NumberOfVisibleCells():
        # The agent can view the numbered cells relative to its current
        # location (cell labeled 2).
        #  | 0 | 1 | 2 |
        #  | 3 | 4 | 5 |
        #  | 6 | 7 | 8 |
        return 9

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
        output = 0
        output += (len(picking_cans_board.CELLS) ** 0) * self._state[0][0]
        output += (len(picking_cans_board.CELLS) ** 1) * self._state[0][1]
        output += (len(picking_cans_board.CELLS) ** 2) * self._state[0][2]
        output += (len(picking_cans_board.CELLS) ** 3) * self._state[1][0]
        output += (len(picking_cans_board.CELLS) ** 4) * self._state[1][1]
        output += (len(picking_cans_board.CELLS) ** 5) * self._state[1][2]
        output += (len(picking_cans_board.CELLS) ** 6) * self._state[2][0]
        output += (len(picking_cans_board.CELLS) ** 7) * self._state[2][1]
        output += (len(picking_cans_board.CELLS) ** 8) * self._state[2][2]
        return output

    def GetContents(self, r, c):
        return self._state[r][c]
