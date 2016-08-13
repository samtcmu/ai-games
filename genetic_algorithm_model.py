import model
import picking_cans_board
import random

class GeneticAlgorithmModel(model.Model):
    def __init__(self, actions = None, randomize=False, parents=None):
        if parents is not None:
            self._actions = [ACTION_UP for _ in range(32)]
            for i in range(len(self._actions)):
                self._actions[i] = (
                    parents[random.randint(0, len(parents) - 1)]._actions[i])
                self._actions[i] = (
                    (self._actions[i] +
                     ((1 if random.random() < 0.005 else 0) *
                       random.randint(1, len(picking_cans_board.ACTIONS)))) %
                    len(picking_cans_board.ACTIONS))
        elif actions is None:
            self._actions = [ACTION_UP for _ in range(32)]
            if randomize:
                self.Randomize()
        else:
            self._actions = actions

    def __str__(self):
        return str(self._actions)

    def Randomize(self):
        for i in range(32):
            self._actions[i] = picking_cans_board.ACTIONS[
                random.randint(0, len(picking_cans_board.ACTIONS) - 1)][0]

    def ActionForCurrentPosition(self, board, r, c):
        # Exponent of 2 for each board position relative to current position
        # (where 4 is).
        #      | 0 |
        #  | 1 | 2 | 3 |
        #      | 4 |
        position = 0
        position += (1 << 0) * board.ContainsCan(r - 1, c)
        position += (1 << 1) * board.ContainsCan(r, c - 1)
        position += (1 << 2) * board.ContainsCan(r, c)
        position += (1 << 3) * board.ContainsCan(r, c + 1)
        position += (1 << 4) * board.ContainsCan(r + 1, c)
        return self._actions[position]

    def Train(rows=10, columns=10, generations=500, population_size=200, games=200,
              actions_per_game=200):
        board = picking_cans_board.Board(rows, columns)
        population = [Model(randomize=True) for _ in range(population_size)]
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
            print "generation: %d" % (g,)
            print "average score: %0.02f" % (average_score,)
            print "top performers: %0.02f, %0.02f" % (
                max_score, second_max_score)

            fittest = (population[max_index], population[second_max_index])
            population = [Model(parents=fittest) for _ in range(len(population))]
            print "1st place: %s" % (fittest[0],)
            print "2nd place: %s\n" % (fittest[1],)
        return fittest

def MaxIndex(L):
    max_index = 0
    for i in range(len(L)):
        if L[i] > L[max_index]:
            max_index = i
    return max_index
