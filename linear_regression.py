import math_util
import random

class LinearRegression:
    def __init__(self, n):
        self._inputs = n + 1
        self._weights = [0.0 for _ in range(self._inputs)]

    def __str__(self):
        return "[%s]" % (", ".join("%.3f" % (w) for w in self._weights))

    def RandomizeWeights(self, random_range=(-1.0, 1.0)):
        self._weights = [random.uniform(random_range[0], random_range[1])
                         for _ in self._weights]

    def Infer(self, inputs):
        return self._Infer([-1.0] + inputs)

    def _Infer(self, inputs):
        return math_util.VectorDotProduct(self._weights, inputs)

    def Fitness(self, training_data):
        return sum(-0.5 * (t[1] - self._Infer(t[0]))**2 for t in training_data)

    def _WeightsGradient(self, t, learning_rate):
        return math_util.VectorScalarProduct(
            learning_rate * (t[1] - self._Infer(t[0])), t[0])

    def _RegularizationGradient(self, regularization_rate):
        return math_util.VectorScalarProduct(
            2 * regularization_rate, self._weights)

    def Train(self, training_data, learning_rate=1.0, learning_iterations=1,
              regularization_rate=1.0, verbose=False):
        return self._Train([([-1.0] + t[0], t[1]) for t in training_data],
                           learning_rate=learning_rate,
                           learning_iterations=learning_iterations,
                           regularization_rate=regularization_rate,
                           verbose=verbose)

    def _Train(self, training_data, learning_rate=1.0, learning_iterations=1,
               regularization_rate=0.0, verbose=False):
        for k in range(learning_iterations):
            random.shuffle(training_data)
            if verbose:
                current_fitness = self.Fitness(training_data)
                print "fitness(%4d): %s" % (k, "{:,.8f}".format(current_fitness))
                print "model(%4d): %s" % (k, self)

            for t in training_data:
                self._weights = math_util.VectorSum(
                    self._weights, self._WeightsGradient(t, learning_rate))

            self._weights = math_util.VectorDifference(
                self._weights,
                self._RegularizationGradient(regularization_rate))
