import model
import picking_cans_board
import random

class ReinforcementLearningModel(model.Model):
    def __init__(self, learning_rate=0.1, discount_rate=1.0, q_matrix=None):
        self._learning_rate = learning_rate
        self._discount_rate = discount_rate
        if q_matrix:
            self._q_matrix = q_matrix
        else:
            self._q_matrix = [
                [0.0 for _ in picking_cans_board.ACTIONS] for _ in range(32)]

    def __str__(self):
        return str(self._q_matrix)

    def ActionForPosition(self, position):
        best_actions = MaxIndices(self._q_matrix[position])
        return best_actions[random.randrange(len(best_actions))]

    def Update(self, initial_position, action, final_position, reward, score):
        assert -10 <= reward <= 10
        best_action = MaxIndices(self._q_matrix[final_position])[0]
        self._q_matrix[initial_position][action] = (
            ((1.0 - self._learning_rate) *
             self._q_matrix[initial_position][action]) +
            (self._learning_rate *
             (reward + (self._discount_rate *
              self._q_matrix[final_position][best_action]))))

def Train(rows=10, columns=10, games=200, actions_per_game=200,
          learning_rate=0.1, discount_rate=0.9, verbose=False):
    model = ReinforcementLearningModel(learning_rate=learning_rate,
                                       discount_rate=discount_rate)
    board = picking_cans_board.Board(rows, columns)
    latest_score = [0 for _ in range(1000)]
    for i in range(1, games + 1):
        board.Randomize()
        board.RandomizeCurrentPosition()
        score = board.PickCansWithModel(
            model, actions_per_game=actions_per_game)
        latest_score[i % len(latest_score)] = score

        if verbose:
            print "game %7d: %3d %.2f" % (i, score, sum(latest_score) / float(len(latest_score)))
            if i % 10000 == 0:
                print model

    return model

def MaxIndices(L):
    max_indices = [0]
    for i in range(1, len(L)):
        if L[i] > L[max_indices[0]]:
            max_indices = [i]
        elif L[i] == L[max_indices[0]]:
            # TODO(samt): Since we are comparing floating point numbers we
            # might want a better comparison method.
            max_indices.append(i)
    return max_indices
