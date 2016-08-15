import model
import picking_cans_board
import random

class ReinforcementLearningModel(model.Model):
    def __init__(self, learning_rate, discount_rate):
        self._learning_rate = learning_rate
        self._discount_rate = discount_rate
        self._q_matrix = [
            [0.0 for _ in picking_cans_board.ACTIONS] for _ in range(32)]

    def __str__(self):
        raise Exception, "TODO(samtet)"

    def ActionForPosition(self, position):
        best_actions = MaxIndices(self._q_matrix[position])
        return best_actions[random.randrange(len(best_actions))]

    def Update(self, initial_position, action, final_position, reward, score):
        pass

    def Train(rows=10, columns=10, games=200, actions_per_game=200):
        raise Exception, "TODO(samtet)"

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
