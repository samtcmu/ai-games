import math_util
import random

class NeuralNetwork:
    def __init__(self, input_width, output_width, hidden_layer_widths=[]):
        self._input_width = input_width
        self._output_width = output_width
        self._layer_widths = (
            [self._input_width] + hidden_layer_widths + [self._output_width])

        self._weights = [[[0.0 for j in range(self._layer_widths[l - 1] + 1)]
                               for i in range(self._layer_widths[l])]
                               for l in range(1, len(self._layer_widths))]

    def __str__(self):
        output = ""
        for l in range(len(self._weights)):
            output += "layer %d:\n" % (l + 1,)
            for i in range(len(self._weights[l])):
                output += "  neuron %d:" % (i + 1,)
                for j in range(len(self._weights[l][i])):
                    # TODO(samt): Adjust the width based on the maximum weight.
                    output += "{0:7.2f}".format(self._weights[l][i][j],) + " "
                output += "\n"
        return output

    def Weight(self, l, i, j):
        assert 1 <= l <= len(self._layer_widths)
        assert 1 <= i <= len(self._layer_widths[i])
        assert 0 <= j <= len(self._layer_widths[j])
        return self._weights[l - 1][i - 1][j]

    def RandomizeWeights(self, random_range=(-1.0, 1.0)):
        for l in range(len(self._weights)):
            for i in range(len(self._weights[l])):
                for j in range(len(self._weights[l][i])):
                    self._weights[l][i][j] = random.uniform(
                        random_range[0], random_range[1])

    def Infer(self, inputs):
        # TODO(samtet): Update the way we store the weights matrix so that no
        # MatrixTranspose operations are required in Infer and _Infer.
        # Right now we do:
        #   W * transpose(input)
        # Instead we want to do:
        #   input * W'
        # where W' = transpose(W) which will be the standard way we store the
        # weights matrix.
        return math_util.MatrixTranspose(self._Infer(inputs)[-1])[0]

    def _Infer(self, inputs):
        outputs = []
        current_layer_inputs = math_util.MatrixTranspose([[-1.0] + inputs])
        for l in range(len(self._weights)):
            current_layer_ouputs = [
                [math_util.Sigmoid(x) for x in row]
                for row in math_util.MatrixMult(self._weights[l],
                                                current_layer_inputs)]
            outputs.append(current_layer_ouputs)
            current_layer_inputs = [[-1.0]] + current_layer_ouputs
        return outputs

    def Fitness(self, training_data, classifications):
        output = 0.0
        for t, c in zip(training_data, classifications):
            output += (-0.5 * math_util.VectorMagnitude(
                       math_util.VectorDifference(t[1], c[-1][0]))**2)
        return output

    def _WeightsGradientForSingleTrainingExample(self, t, c, verbose=False):
        weights_gradient = [[[0.0 for j in range(self._layer_widths[l - 1] + 1)]
                                  for i in range(self._layer_widths[l])]
                                  for l in range(1, len(self._layer_widths))]
        return weights_gradient

    def _WeightsGradient(self, training_data, classifications, verbose=False):
        weights_gradient = [[[0.0 for j in range(self._layer_widths[l - 1] + 1)]
                                  for i in range(self._layer_widths[l])]
                                  for l in range(1, len(self._layer_widths))]
        return weights_gradient

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
                print "fitness(%4d): %0.3f" % (k, current_fitness)
                print "model(%4d): %s" % (k, self)

            for t, c in zip(training_data, current_classifications):
                weights_gradient = self._WeightsGradient(
                    [t], [c], verbose=False)
                print "training example:"
                for row in t:
                    print "  %s" % (row,)

                print "current classification:"
                for row in c:
                    print "  %s" % (row,)
                print
                for l in range(len(self._weights)):
                    self._weights[l] = math_util.MatrixSum(
                        self._weights[l],
                        math_util.MatrixScalarProduct(
                            learning_rate, weights_gradient[l]))
