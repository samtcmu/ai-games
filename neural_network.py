import itertools
import math_util
import numpy
import pickle
import progress_bar
import random

class NeuralNetwork:
    def __init__(self, input_width, output_width, hidden_layer_widths=[]):
        self._input_width = input_width
        self._output_width = output_width
        self._layer_widths = (
            [self._input_width] + hidden_layer_widths + [self._output_width])

        self._weights = [
            numpy.array([[0.0 for j in xrange(self._layer_widths[l - 1] + 1)]
                              for i in xrange(self._layer_widths[l])])
            for l in xrange(1, len(self._layer_widths))]

    def __str__(self):
        output = ""
        for l in xrange(len(self._weights)):
            output += "layer %d:\n" % (l + 1,)
            for i in xrange(len(self._weights[l])):
                output += "  neuron %d: " % (i + 1,)
                for j in xrange(len(self._weights[l][i])):
                    # TODO(samt): Adjust the width based on the maximum weight.
                    output += "{:4.2f}".format(self._weights[l][i][j],) + " "
                output += "\n"
        return output

    def Weight(self, l, i, j):
        assert 1 <= l <= len(self._layer_widths) - 1
        assert 1 <= i <= self._layer_widths[l]
        assert 0 <= j <= self._layer_widths[l - 1]
        return self._weights[l - 1][i - 1][j]

    def RandomizeWeights(self, random_range=(-1.0, 1.0)):
        for l in xrange(len(self._weights)):
            for i in xrange(len(self._weights[l])):
                for j in xrange(len(self._weights[l][i])):
                    self._weights[l][i][j] = random.uniform(
                        random_range[0], random_range[1])

    def Infer(self, inputs):
        return self._Infer(inputs)[-1][1:]

    def _Infer(self, inputs):
        depth = len(self._weights)
        current_layer_inputs = numpy.append([-1.0], inputs)
        outputs = [current_layer_inputs]
        for l in xrange(depth):
            current_layer_ouputs = math_util.Sigmoid(
                numpy.dot(self._weights[l], current_layer_inputs))
            current_layer_inputs = numpy.append([-1.0], current_layer_ouputs)
            outputs.append(current_layer_inputs)
        return outputs

    def Fitness(self, training_data, k, verbose=False):
        message = "training iteration %d: computing model fitness" % (k,)
        with progress_bar.ProgressBar(
            len(training_data), start_message=message, bar_color="yellow",
            verbose=verbose) as bar:
            x = numpy.array([
                [numpy.linalg.norm(t[1] - self.Infer(t[0])), bar.Increment()][0]
                for t in training_data])
            return -0.5 * numpy.dot(x, x)

    def _WeightsGradient(self, t, learning_rate):
        last_layer_index = len(self._layer_widths) - 1
        weights_gradient = [None for l in xrange(1, len(self._layer_widths))]

        c = self._Infer(t[0])
        for l in xrange(last_layer_index, 0, -1):
            delta = None
            ones = numpy.ones(len(c[l]) - 1)
            c_l = c[l][1:]
            if l == last_layer_index:
                delta = learning_rate * ((ones - c_l) * c_l * (t[1] - c_l))
            else:
                W = numpy.sum(self._weights[l] * weights_gradient[l], axis=0)
                delta = (ones - c_l) * W[1:]

            weights_gradient[l - 1] = numpy.dot(
                numpy.transpose(numpy.array([delta])),
                numpy.array([c[l - 1]]))

        return weights_gradient

    def _RegularizationGradient(self, regularization_rate):
        return [(2 * regularization_rate) * w for w in self._weights]

    def Train(self, training_data, learning_rate=1.0, learning_iterations=10,
              regularization_rate=0.0, model_path_prefix=None, verbose=False,
              show_progress_bars=False):
        T = [(numpy.array(t[0]), numpy.array(t[1])) for t in training_data]
        for k in xrange(learning_iterations):
            random.shuffle(T)

            if verbose:
                current_fitness = self.Fitness(
                    T, k, verbose=show_progress_bars)
                print "training iteration %d: model fitness = %s" % (
                    k, "{:,.8f}".format(current_fitness))
                # print "model(%4d): \n%s" % (k, self)

            if model_path_prefix:
                model_file_path = "%s-%d.txt" % (model_path_prefix, k)
                if verbose:
                    print "training iteration %d: saving current model to %s" % (
                        k, model_file_path)
                with open(model_file_path, "w") as model_file:
                    pickle.dump(self, model_file)

            with progress_bar.ProgressBar(
                len(T),
                start_message="training iteration %d: running gradient descent" % (k,),
                bar_color="cyan", verbose=show_progress_bars) as bar:
                for t in T:
                    weights_gradient = self._WeightsGradient(t, learning_rate)
                    for l in xrange(len(self._weights)):
                        self._weights[l] += weights_gradient[l]
                    bar.Increment()

            # Apply L2 Regularization to self._weights.
            regularization_gradient = self._RegularizationGradient(
                regularization_rate)
            for l in xrange(len(self._weights)):
                self._weights[l] -= regularization_gradient[l]
