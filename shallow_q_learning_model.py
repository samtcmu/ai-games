import linear_regression
import model
import picking_cans_board
import pickle
import random

class ShallowQLearningModel(model.Model):
    def __init__(self, learning_rate=1.0, discount_rate=1.0,
                 exploration_rate=0.1, linear_regression_learning_rate=0.1,
                 filename=None):
        self._learning_rate = learning_rate
        self._discount_rate = discount_rate
        self._exploration_rate = exploration_rate
        self._linear_regression_learning_rate = linear_regression_learning_rate
        if filename:
            self.LoadFromFile(filename)
        else:
            self._q_matrix_model = linear_regression.LinearRegression(
                len(picking_cans_board.CELLS)**5 * len(picking_cans_board.ACTIONS))
            self._q_matrix_model.RandomizeWeights(random_range=(-1.0, 1.0))

    def __str__(self):
        return str(self._q_matrix_model)

    def SaveToFile(self, filename):
        model_file = open(filename, "w")
        pickle.dump(self._q_matrix_model, model_file)
        model_file.close()

    def LoadFromFile(self, filename):
        model_file = open(filename, "r")
        self._q_matrix_model = pickle.load(model_file)
        model_file.close()

    def _FeatureVector(self, position, action):
        feature_vector = [[0.0 for _ in range(len(picking_cans_board.CELLS)**5)]
                               for _ in range(len(picking_cans_board.ACTIONS))]
        feature_vector[action][position] = 1.0
        return reduce(lambda x, y: x + y, feature_vector, [])

    def ActionForPosition(self, position):
        if random.random() < self._exploration_rate:
            # For exploration we pick a random action some of the time.
            best_actions = [a[0] for a in picking_cans_board.ACTIONS]
        else:
            action_values = [self._q_matrix_model.Infer(self._FeatureVector(position, a[0]))
                             for a in picking_cans_board.ACTIONS]
            best_actions = MaxIndices(action_values)

        return random.choice(best_actions)

    def Update(self, initial_position, action, final_position, reward, score):
        action_values = [self._q_matrix_model.Infer(self._FeatureVector(final_position, a[0]))
                         for a in picking_cans_board.ACTIONS]
        best_action = MaxIndices(action_values)[0]
        updated_q_value = (
            ((1.0 - self._learning_rate) *
             self._q_matrix_model.Infer(self._FeatureVector(initial_position, action))) +
            (self._learning_rate *
             (reward + (self._discount_rate *
              self._q_matrix_model.Infer(self._FeatureVector(
                  final_position, best_action))))))

        self._q_matrix_model.Train([
            [self._FeatureVector(initial_position, action), updated_q_value]],
            learning_rate=self._linear_regression_learning_rate,
            learning_iterations=1,
            regularization_rate=0.0,
            verbose=False)

def Train(rows=10, columns=10, random_wall=False, games=200,
          actions_per_game=200, learning_rate=0.1, discount_rate=0.9,
          exploration_rate=0.1, linear_regression_learning_rate=0.1,
          model_save_frequency=1000, model_file_prefix=None, verbose=False):
    model = ShallowQLearningModel(
        learning_rate=learning_rate,
        discount_rate=discount_rate,
        exploration_rate=exploration_rate,
        linear_regression_learning_rate=linear_regression_learning_rate)
    board = picking_cans_board.Board(rows, columns)
    latest_score = [0 for _ in range(1000)]
    for i in range(1, games + 1):
        board.Randomize(random_wall=random_wall)
        board.RandomizeCurrentPosition()
        score = board.PickCansWithModel(
            model, actions_per_game=actions_per_game)
        latest_score[i % len(latest_score)] = score

        if verbose:
            print "game %7d: %3d %.2f" % (i, score, sum(latest_score) / float(len(latest_score)))
        if model_file_prefix and (i % model_save_frequency == 0):
            model.SaveToFile("%s-%d.txt" % (model_file_prefix, i))

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
