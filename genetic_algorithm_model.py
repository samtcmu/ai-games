import default_agent_state
import list_util
import model
import picking_cans_board
import pickle
import random

class GeneticAlgorithmModel(model.Model):
    def __init__(self, filename=None, randomize=False, parents=None,
                 mutation_rate=0.005,
                 agent_state_class=default_agent_state.DefaultAgentState):
        self._mutation_rate = mutation_rate
        self._agent_state_class = agent_state_class

        if parents is not None:
            self._actions = [
                picking_cans_board.ACTION_UP
                for _ in range(self._agent_state_class.NumberOfStates())]
            for i in range(len(self._actions)):
                self._actions[i] = (
                    random.choice(parents)._actions[i])
                self._actions[i] = (
                    (self._actions[i] +
                     ((1 if random.random() < self._mutation_rate else 0) *
                       random.choice(picking_cans_board.ACTIONS)[0])) %
                    len(picking_cans_board.ACTIONS))
        elif filename is None:
            self._actions = [
                picking_cans_board.ACTION_UP
                for _ in range(self._agent_state_class.NumberOfStates())]
            if randomize:
                self.Randomize()
        else:
            self.LoadFromFile(filename)

    def Randomize(self):
        for i in range(self._agent_state_class.NumberOfStates()):
            self._actions[i] = random.choice(picking_cans_board.ACTIONS)[0]

    def __str__(self):
        return str(self._actions)

    def SaveToFile(self, filename):
        model_file = open(filename, "w")
        pickle.dump(self._actions, model_file)
        model_file.close()

    def LoadFromFile(self, filename):
        model_file = open(filename, "r")
        self._actions = pickle.load(model_file)
        model_file.close()

    def ActionForState(self, state):
        return self._actions[int(state)]

    def Update(self, initial_state, action, final_state, reward):
        # Genetic algorithms do not learn in an online fashion.
        return

def Train(rows=10, columns=10, generations=500, population_size=200, games=200,
          actions_per_game=200, mutation_rate=0.005, model_file_prefix=None,
          agent_state_class=default_agent_state.DefaultAgentState,
          verbose=False):
    board = picking_cans_board.Board(
        rows, columns, agent_state_class=agent_state_class)
    population = [
        GeneticAlgorithmModel(randomize=True, mutation_rate=mutation_rate,
                              agent_state_class=agent_state_class)
        for _ in range(population_size)]
    fittest = None
    for g in range(generations):
        scores = [0.0 for _ in range(population_size)]
        for p in range(population_size):
            for i in range(games):
                board.Randomize()
                board.RandomizeCurrentPosition()
                score = board.PickCansWithModel(
                    population[p], actions_per_game=actions_per_game)
                scores[p] += score
            scores[p] /= games

        average_score = list_util.Mean(scores)
        max_index = list_util.MaxIndex(scores)
        max_score = scores[max_index]
        scores[max_index] = float("-inf")
        second_max_index = list_util.MaxIndex(scores)
        second_max_score = scores[second_max_index]

        fittest = (population[max_index], population[second_max_index])
        population = [
            GeneticAlgorithmModel(parents=fittest, mutation_rate=mutation_rate,
                                  agent_state_class=agent_state_class)
            for _ in range(len(population))]
        if verbose:
            print "generation: %d" % (g,)
            print "average score: %0.02f" % (average_score,)
            print "top performers: %0.02f, %0.02f" % (
                max_score, second_max_score)

        fittest[0].SaveToFile("%s-%d-%d.txt" % (model_file_prefix, g, 0))
        fittest[1].SaveToFile("%s-%d-%d.txt" % (model_file_prefix, g, 1))
    return fittest
