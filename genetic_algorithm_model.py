import model
import picking_cans_board
import pickle
import random

class GeneticAlgorithmModel(model.Model):
    def __init__(self, filename=None, randomize=False, parents=None,
                 mutation_rate=0.005):
        self._mutation_rate = mutation_rate

        if parents is not None:
            self._actions = [
                picking_cans_board.ACTION_UP
                for _ in range(len(picking_cans_board.CELLS) ** 5)]
            for i in range(len(self._actions)):
                self._actions[i] = (
                    parents[random.randint(0, len(parents) - 1)]._actions[i])
                self._actions[i] = (
                    (self._actions[i] +
                     ((1 if random.random() < self._mutation_rate else 0) *
                       random.randint(1, len(picking_cans_board.ACTIONS)))) %
                    len(picking_cans_board.ACTIONS))
        elif filename is None:
            self._actions = [
                picking_cans_board.ACTION_UP
                for _ in range(len(picking_cans_board.CELLS) ** 5)]
            if randomize:
                self.Randomize()
        else:
            self.LoadFromFile(filename)

    def Randomize(self):
        for i in range(len(picking_cans_board.CELLS) ** 5):
            self._actions[i] = picking_cans_board.ACTIONS[
                random.randint(0, len(picking_cans_board.ACTIONS) - 1)][0]

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

    def ActionForPosition(self, position):
        return self._actions[position]

    def Update(self, initial_position, action, final_position, reward, score):
        # Genetic algorithms do not learn in an online fashion.
        return

def Train(rows=10, columns=10, generations=500, population_size=200, games=200,
          actions_per_game=200, mutation_rate=0.005, model_file_prefix=None,
          verbose=False):
    board = picking_cans_board.Board(rows, columns)
    population = [
        GeneticAlgorithmModel(randomize=True, mutation_rate=mutation_rate)
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

        average_score = sum(scores) / population_size
        max_index = MaxIndex(scores)
        max_score = scores[max_index]
        scores[max_index] = float("-inf")
        second_max_index = MaxIndex(scores)
        second_max_score = scores[second_max_index]

        fittest = (population[max_index], population[second_max_index])
        population = [
            GeneticAlgorithmModel(parents=fittest, mutation_rate=mutation_rate)
            for _ in range(len(population))]
        if verbose:
            print "generation: %d" % (g,)
            print "average score: %0.02f" % (average_score,)
            print "top performers: %0.02f, %0.02f" % (
                max_score, second_max_score)

        fittest[0].SaveToFile("%s-%d-%d.txt" % (model_file_prefix, g, 0))
        fittest[1].SaveToFile("%s-%d-%d.txt" % (model_file_prefix, g, 1))
    return fittest

def MaxIndex(L):
    max_index = 0
    for i in range(len(L)):
        if L[i] > L[max_index]:
            max_index = i
    return max_index
