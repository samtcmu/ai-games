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
            output += "layer %d:\n" % (l,)
            for i in range(len(self._weights[l])):
                output += "    "
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
