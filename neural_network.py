import math_util
import random

class NeuralNetwork:
    def __init__(self, input_width, output_width, hidden_layer_widths=[]):
        self._input_width = input_width
        self._output_width = output_width
        self._layer_widths = (
            [self._input_width] + hidden_layer_widths + [self._output_width])

        self._weights = [[[0.0 for i in range(self._layer_widths[l])]
                               for j in range(self._layer_widths[l - 1] + 1)]
                               for l in range(1, len(self._layer_widths))]

    def __str__(self):
        output = ""
        for l in range(len(self._weights)):
            output += "layer %d:\n" % (l + 1,)
            for i in range(len(self._weights[l][0])):
                output += "  neuron %d: " % (i + 1,)
                for j in range(len(self._weights[l])):
                    # TODO(samt): Adjust the width based on the maximum weight.
                    output += "{0:8.5f}".format(self._weights[l][j][i],) + " "
                output += "\n"
        return output

    def Weight(self, l, i, j):
        assert 1 <= l <= len(self._layer_widths) - 1
        assert 1 <= i <= self._layer_widths[l]
        assert 0 <= j <= self._layer_widths[l - 1]
        return self._weights[l - 1][j][i - 1]

    def RandomizeWeights(self, random_range=(-1.0, 1.0)):
        for l in range(len(self._weights)):
            for j in range(len(self._weights[l])):
                for i in range(len(self._weights[l][j])):
                    self._weights[l][j][i] = random.uniform(
                        random_range[0], random_range[1])

    def Infer(self, inputs):
        return self._Infer(inputs)[-1][1:]

    @staticmethod
    def _Sigmoid(x, l, depth):
        # Applies the Sigmoid function at all layers of the neural network
        # besides the final layer which will simply be a linear layer (i.e.
        # this function will just be the identity function).
        # return math_util.Sigmoid(x) if l < (depth - 1) else x
        return math_util.Sigmoid(x)

    def _Infer(self, inputs):
        depth = len(self._weights)
        current_layer_inputs = [[-1.0] + inputs]
        outputs = [current_layer_inputs[0]]
        for l in range(depth):
            current_layer_ouputs = [
                [NeuralNetwork._Sigmoid(x, l, depth) for x in row]
                for row in math_util.MatrixMult(current_layer_inputs,
                                                self._weights[l])]
            outputs.append([-1.0] + current_layer_ouputs[0])
            current_layer_inputs = [[-1.0] + current_layer_ouputs[0]]
        return outputs

    def Fitness(self, training_data, classifications):
        output = 0.0
        for t, c in zip(training_data, classifications):
            output += (-0.5 * math_util.VectorMagnitude(
                       math_util.VectorDifference(t[1], c[-1][1:]))**2)
        return output

    def _WeightsGradientForSingleTrainingExample(self, t, c, verbose=False):
        weights_gradient = [[[0.0 for i in range(self._layer_widths[l])]
                                  for j in range(self._layer_widths[l - 1] + 1)]
                                  for l in range(1, len(self._layer_widths))]

        for l in range(len(self._layer_widths) - 1, 0, -1):
            for i in range(1, self._layer_widths[l] + 1):
                common_weight_gradient = 0.0
                if l == len(self._layer_widths) - 1:
                    common_weight_gradient = (
                        (t[1][i - 1] - c[l][i]) * c[l][i] * (1.0 - c[l][i]))
                if l < len(self._layer_widths) - 1:
                    common_weight_gradient = 0.0
                    for k in range(1, self._layer_widths[l + 1] + 1):
                        common_weight_gradient += (
                            self.Weight(l + 1, k, i) *
                            weights_gradient[l][i][k - 1])
                    common_weight_gradient *= (1.0 - c[l][i])

                for j in range(self._layer_widths[l - 1] + 1):
                    weights_gradient[l - 1][j][i - 1] = (
                        common_weight_gradient * c[l - 1][j])

        return weights_gradient

    def _WeightsGradient(self, training_data, classifications, verbose=False):
        weights_gradient = [[[0.0 for i in range(self._layer_widths[l])]
                                  for j in range(self._layer_widths[l - 1] + 1)]
                                  for l in range(1, len(self._layer_widths))]

        for t, c in zip(training_data, classifications):
            weights_gradient_for_training_example = (
                self._WeightsGradientForSingleTrainingExample(
                    t, c, verbose=verbose))
            for l in range(len(self._weights)):
                weights_gradient[l] = math_util.MatrixSum(
                    weights_gradient[l],
                    weights_gradient_for_training_example[l])

        return weights_gradient

    def _RegularizationGradient(self, l, regularization_rate):
        return math_util.MatrixScalarProduct(
            2 * regularization_rate, self._weights[l])

    def Train(self, training_data, learning_rate=1.0, learning_iterations=10,
              regularization_rate=0.0, verbose=False):
        for k in range(learning_iterations):
            random.shuffle(training_data)
            current_classifications = [self._Infer(t[0]) for t in training_data]
            current_fitness = self.Fitness(training_data,
                                           current_classifications)
            if verbose:
                current_fitness = self.Fitness(training_data,
                                               current_classifications)
                print "fitness(%4d): %s" % (k, "{:,.4f}".format(current_fitness))
                print "model(%4d): \n%s" % (k, self)

            for t, c in zip(training_data, current_classifications):
                # TODO(samt): Since we are running stochastic gradient descent
                # here we should call _WeightsGradientForSingleTrainingExample.
                weights_gradient = self._WeightsGradient(
                    [t], [c], verbose=False)

                for l in range(len(self._weights)):
                    regularization_gradient = self._RegularizationGradient(
                        l, regularization_rate)

                    weights_gradient[l] = math_util.MatrixScalarProduct(
                        learning_rate, weights_gradient[l])

                    weights_gradient[l] = math_util.MatrixDifference(
                        weights_gradient[l], regularization_gradient)

                    self._weights[l] = math_util.MatrixSum(
                        self._weights[l], weights_gradient[l])
