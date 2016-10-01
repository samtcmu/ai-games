import math_util
import random

class LinearRegression:
    def __init__(self, n):
        self._inputs = n + 1
        self._weights = [0.0 for _ in range(self._inputs)]

    def __str__(self):
        return "[%s]" % (", ".join("%.3f" % (w) for w in self._weights))

    def RandomizeWeights(self, random_range=(-1.0, 1.0)):
        for i in range(self._inputs):
            self._weights[i] = random.uniform(
                random_range[0], random_range[1])

    def Infer(self, inputs):
        return self._Infer([-1.0] + inputs)

    def _Infer(self, inputs):
        return math_util.VectorDotProduct(self._weights, inputs)

    def Fitness(self, training_data, classifications):
        output = 0.0
        for t, c in zip(training_data, classifications):
            output += (-0.5 * (t[1] - c)**2)
        return output

    def _PartialDerivative(self, training_data, classifications, i, verbose=False):
        weight_partial_derivative = 0.0
        for t, c in zip(training_data, classifications):
            weight_partial_derivative += (t[1] - c) * t[0][i]
        return weight_partial_derivative

    def _WeightsGradient(self, training_data, classifications, verbose=False):
        weights_gradient = [0.0 for _ in self._weights]
        for i in range(len(weights_gradient)):
            weights_gradient[i] = self._PartialDerivative(
                training_data, classifications, i, verbose=verbose)
        return weights_gradient

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
                current_classifications = [self._Infer(t[0]) for t in training_data]
                current_fitness = self.Fitness(training_data,
                                               current_classifications)
                print "fitness(%4d): %s" % (k, "{:,.8f}".format(current_fitness))
                print "model(%4d): %s" % (k, self)

            for t in training_data:
                weights_gradient = self._WeightsGradient(
                    [t], [self._Infer(t[0])], verbose=False)
                self._weights = math_util.VectorSum(
                    self._weights,
                    math_util.VectorScalarProduct(
                        learning_rate, weights_gradient))

            self._weights = math_util.VectorDifference(
                self._weights,
                self._RegularizationGradient(regularization_rate))
