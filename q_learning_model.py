import default_agent_state
import list_util
import model
import picking_cans_board
import pickle
import random

class QLearningModel(model.Model):
    def __init__(self, learning_rate=0.1, discount_rate=1.0,
                 exploration_rate=0.1, filename=None,
                 agent_state_class=default_agent_state.DefaultAgentState):
        self._learning_rate = learning_rate
        self._discount_rate = discount_rate
        self._exploration_rate = exploration_rate
        if filename:
            self.LoadFromFile(filename)
        else:
            self._q_matrix = [
                [0.0 for _ in picking_cans_board.ACTIONS]
                for _ in range(agent_state_class.NumberOfStates())]
        self._agent_state_class = agent_state_class

    def __str__(self):
        output = ""
        for i in range(len(self._q_matrix)):
            output += "%2d: " % (i,)
            for j in range(len(self._q_matrix[i])):
                output += "%3.3f " % (self._q_matrix[i][j],)
            output += "\n"
        return output

    def SaveToFile(self, filename):
        model_file = open(filename, "w")
        pickle.dump(self._q_matrix, model_file)
        model_file.close()

    def LoadFromFile(self, filename):
        model_file = open(filename, "r")
        self._q_matrix = pickle.load(model_file)
        model_file.close()

    def ActionForState(self, state):
        if random.random() < self._exploration_rate:
            # For exploration we pick a random action some of the time.
            best_actions = [a[0] for a in picking_cans_board.ACTIONS]
        else:
            best_actions = list_util.MaxIndices(self._q_matrix[int(state)])

        return random.choice(best_actions)

    def Update(self, initial_state, action, final_state, reward):
        best_action = list_util.MaxIndices(self._q_matrix[int(final_state)])[0]
        self._q_matrix[int(initial_state)][action] = (
            ((1.0 - self._learning_rate) *
             self._q_matrix[int(initial_state)][action]) +
            (self._learning_rate *
             (reward + (self._discount_rate *
              self._q_matrix[int(final_state)][best_action]))))

def Train(rows=10, columns=10, random_wall=False, games=200,
          actions_per_game=200, learning_rate=0.1, discount_rate=0.9,
          exploration_rate=0.1, model_save_frequency=1000,
          model_file_prefix=None,
          agent_state_class=default_agent_state.DefaultAgentState,
          verbose=False):
    model = QLearningModel(learning_rate=learning_rate,
                           discount_rate=discount_rate,
                           exploration_rate=exploration_rate,
                           agent_state_class=agent_state_class)
    board = picking_cans_board.Board(
        rows, columns, agent_state_class=agent_state_class)
    latest_score = [0 for _ in range(1000)]
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
