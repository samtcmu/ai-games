import default_agent_state
import neural_network
import list_util
import math_util
import model
import picking_cans_board
import pickle
import random

class DeepQLearningModel(model.Model):
    def __init__(self, learning_rate=1.0, discount_rate=1.0,
                 exploration_rate=0.1, neural_network_learning_rate=0.1,
                 agent_state_class=default_agent_state.DefaultAgentState,
                 filename=None, disable_training=False):
        self._learning_rate = learning_rate
        self._discount_rate = discount_rate
        self._exploration_rate = exploration_rate
        self._neural_network_learning_rate = neural_network_learning_rate
        self._agent_state_class = agent_state_class
        self._disable_training = disable_training
        number_of_visible_cells = (
            self._agent_state_class.NumberOfVisibleCells())
        self._feature_vector_size = (
            (len(picking_cans_board.CELLS) * number_of_visible_cells) +
            len(picking_cans_board.ACTIONS) +
            (len(picking_cans_board.CELLS) * len(picking_cans_board.ACTIONS) *
             number_of_visible_cells))
        if filename:
            self.LoadFromFile(filename)
        else:
            self._q_matrix_model = neural_network.NeuralNetwork(
                self._feature_vector_size, 1, hidden_layer_widths=[])
            self._q_matrix_model.RandomizeWeights(random_range=(-0.1, 0.1))

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

    def _StateAsArray(self, state):
        output = []
        diameter = self._agent_state_class.VisibleDiameter()
        for r in range(diameter):
            for c in range(diameter):
                cell_contents = state.GetContents(r, c)
                if cell_contents is not None:
                    output.append(cell_contents)
        return output

    def _FeatureVector(self, state, action):
        feature_vector = [0.0 for _ in range(self._feature_vector_size)]
        state_array = self._StateAsArray(state)
        len_cells = len(picking_cans_board.CELLS)
        len_actions = len(picking_cans_board.ACTIONS)
        len_action_cell_pairs = len_cells * len_actions
        i = 0

        # For each of the cells in the position add a categorical feature for
        # each of the possible contents of the cell.
        for c in state_array:
            feature_vector[i + int(c)] = 1.0
            i += len_cells

        # Add a categorical feature for each of the possible actions.
        feature_vector[i + int(action)] = 1.0
        i += len_actions
        # Add a categorical feature for each combination of position cell, its
        # contents, and action.
        for c in state_array:
            feature_vector[i + ((action * len_cells) + int(c))] = 1.0
            i += len_action_cell_pairs

        assert i == self._feature_vector_size

        return feature_vector

    def SetDisableTraining(self, disable_training):
        self._disable_training = disable_training

    def ActionForState(self, state):
        if not self._disable_training and (random.random() < self._exploration_rate):
            # For exploration we pick a random action some of the time.
            best_actions = [a[0] for a in picking_cans_board.ACTIONS]
        else:
            action_values = [
                math_util.InverseSigmoid(
                    self._q_matrix_model.Infer(
                        self._FeatureVector(state, a[0])),
                    max_value=2000.0)
                for a in picking_cans_board.ACTIONS]
            best_actions = list_util.MaxIndices(action_values)

        return random.choice(best_actions)

    def Update(self, initial_state, action, final_state, reward):
        if self._disable_training:
            return

        action_values = [
            math_util.InverseSigmoid(
                self._q_matrix_model.Infer(
                    self._FeatureVector(final_state, a[0])),
                max_value=2000.0)
            for a in picking_cans_board.ACTIONS]
        best_action = list_util.MaxIndices(action_values)[0]
        initial_feature_vector = self._FeatureVector(initial_state, action)
        updated_q_value = (
            ((1.0 - self._learning_rate) *
             math_util.InverseSigmoid(
                self._q_matrix_model.Infer(initial_feature_vector),
                max_value=2000.0)) +
            (self._learning_rate *
             (reward + (self._discount_rate * action_values[best_action]))))

        self._q_matrix_model.Train([
            [initial_feature_vector, math_util.Sigmoid(updated_q_value / 2000.0)]],
            learning_rate=self._neural_network_learning_rate,
            learning_iterations=1,
            regularization_rate=0.0,
            verbose=False)

def Train(rows=10, columns=10, random_wall=False, games=200,
          actions_per_game=200, learning_rate=0.1, discount_rate=0.9,
          exploration_rate=0.1, neural_network_learning_rate=0.1,
          model_save_frequency=1000, model_file_prefix=None,
          agent_state_class=default_agent_state.DefaultAgentState,
          verbose=False):
    model = DeepQLearningModel(
        learning_rate=learning_rate,
        discount_rate=discount_rate,
        exploration_rate=exploration_rate,
        neural_network_learning_rate=neural_network_learning_rate,
        agent_state_class=agent_state_class)
    board = picking_cans_board.Board(
        rows, columns, agent_state_class=agent_state_class)
    latest_score = []
    for i in range(1, games + 1):
        board.Randomize(random_wall=random_wall)
        board.RandomizeCurrentPosition()
        score = board.PickCansWithModel(
            model, actions_per_game=actions_per_game)

        if len(latest_score) < 1000:
            latest_score.append(score)
        else:
            latest_score[i % len(latest_score)] = score

        if verbose:
            print "game %7d: %3d %.2f %.2f" % (
                i, score, list_util.Mean(latest_score),
                list_util.StandardDeviation(latest_score))
        if model_file_prefix and (i % model_save_frequency == 0):
            model.SaveToFile("%s-%d.txt" % (model_file_prefix, i))

    return model
