import math
import random

class LinearRegression:
    def __init__(self, n):
        self._inputs = n + 1
        self._weights = [0.0 for _ in range(self._inputs)]

    def __str__(self):
        return "[%s]" % (", ".join("%.3f" % (w) for w in self._weights))

    def RandomizeSynapticWeights(self, random_range=(-1.0, 1.0)):
        for i in range(self._inputs):
            self._weights[i] = random.uniform(
                random_range[0], random_range[1])

    def Infer(self, inputs):
        return self._Infer([-1.0] + inputs)

    def _Infer(self, inputs):
        return VectorDotProduct(self._weights, inputs)

    def Fitness(self, training_data, classifications):
        output = 0.0
        for t, c in zip(training_data, classifications):
            output += (-0.5 * (t[1] - c)**2)
        return output

    def _PartialDerivative(self, training_data, classifications, i, verbose=False):
        weight_partial_derivative = 0.0
        for t, c in zip(training_data, classifications):
            weight_partial_derivative += (t[1] - c) * t[0][i]
            if verbose:
                print (i, t[1], c, t[1] - c, t[0][i])
        return weight_partial_derivative

    def _WeightsGradient(self, training_data, classifications, verbose=False):
        weights_gradient = [0.0 for _ in self._weights]
        for i in range(len(weights_gradient)):
            weights_gradient[i] = self._PartialDerivative(
                training_data, classifications, i, verbose=verbose)

        if verbose:
            print weights_gradient

        return weights_gradient

    def Train(self, training_data, learning_rate=1.0, learning_iterations=1,
              verbose=False):
        return self._Train([([-1.0] + t[0], t[1]) for t in training_data],
                           learning_rate, learning_iterations, verbose)

    def _Train(self, training_data, learning_rate=1.0, learning_iterations=1,
               verbose=False):
        for k in range(learning_iterations):
            random.shuffle(training_data)
            current_classifications = [self._Infer(t[0]) for t in training_data]
            current_fitness = self.Fitness(training_data,
                                           current_classifications)
            if verbose:
                print "fitness(%4d): %0.3f" % (k, current_fitness)
                print "model(%4d): %s" % (k, self)

            for t, c in zip(training_data, current_classifications):
                weights_gradient = self._WeightsGradient(
                    [t], [c], verbose=False)
                self._weights = VectorSum(
                    self._weights,
                    VectorScalarProduct(learning_rate, weights_gradient))


def VectorDotProduct(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return sum(A[i] * B[i] for i in range(len(A)))

def VectorScalarProduct(c, A):
    return [c * A[i] for i in range(len(A))]

def VectorDifference(A, B):
    return VectorSum(A, VectorScalarProduct(-1.0, B))

def VectorSum(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return [A[i] + B[i] for i in range(len(A))]

def VectorMagnitude(A):
    return math.sqrt(sum(a**2 for a in A))
