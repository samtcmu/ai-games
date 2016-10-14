import itertools
import math_util
import pickle
import progress_bar
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
                    output += "{0:8.5f}".format(self._weights[l][j][i],) + " "
                output += "\n"
        return output

    def Weight(self, l, i, j):
        assert 1 <= l <= len(self._layer_widths) - 1
        assert 1 <= i <= self._layer_widths[l]
        assert 0 <= j <= self._layer_widths[l - 1]
        return self._weights[l - 1][i - 1][j]

    def RandomizeWeights(self, random_range=(-1.0, 1.0)):
        for l in range(len(self._weights)):
            for i in range(len(self._weights[l])):
                for j in range(len(self._weights[l][i])):
                    self._weights[l][i][j] = random.uniform(
                        random_range[0], random_range[1])

    def Infer(self, inputs):
        return self._Infer(inputs)[-1][1:]

    def _Infer(self, inputs):
        # TODO(samt): Cache the result of this call as an instance variable.
        depth = len(self._weights)
        current_layer_inputs = [-1.0] + inputs
        outputs = [current_layer_inputs]
        for l in xrange(depth):
            current_layer_ouputs = [
                math_util.Sigmoid(x)
                for x in math_util.MatrixVectorMult(self._weights[l],
                                                    current_layer_inputs)]
            current_layer_inputs = [-1.0] + current_layer_ouputs
            outputs.append(current_layer_inputs)
        return outputs

    def Fitness(self, training_data, k, verbose=False):
        magnitude = math_util.VectorMagnitude
        diff = math_util.VectorDifference
        message = "training iteration %d: computing model fitness" % (k,)
        with progress_bar.ProgressBar(
            len(training_data), start_message=message, bar_color="yellow",
            verbose=verbose) as bar:
            return sum(
                [-0.5 * magnitude(diff(t[1], self.Infer(t[0])))**2,
                 bar.Increment()][0]
                for t in training_data)

    def _WeightsGradient(self, t, learning_rate):
        last_layer_index = len(self._layer_widths) - 1
        weights_gradient = [None for l in xrange(1, len(self._layer_widths))]

        c = self._Infer(t[0])
        for l in xrange(last_layer_index, 0, -1):
            delta = None
            if l == last_layer_index:
                delta = [learning_rate * (1.0 - x) * x * (y - x)
                         for x, y in itertools.izip(c[l][1:], t[1])]
            else:
                W = math_util.MatrixHadamardProductSumRows(
                    self._weights[l], weights_gradient[l])
                delta = [(1.0 - x) * y
                         for x, y in itertools.izip(c[l][1:], W[1:])]

            weights_gradient[l - 1] = math_util.MatrixMult(
                math_util.MatrixTranspose([delta]), [c[l - 1]])

        return weights_gradient

    def _RegularizationGradient(self, regularization_rate):
        return math_util.TensorScalarProduct(
            2 * regularization_rate, self._weights)

    def Train(self, training_data, learning_rate=1.0, learning_iterations=10,
              regularization_rate=0.0, model_path_prefix=None, verbose=False,
              show_progress_bars=False):
        for k in xrange(learning_iterations):
            random.shuffle(training_data)

            if verbose:
                current_fitness = self.Fitness(
                    training_data, k, verbose=show_progress_bars)
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
                len(training_data),
                start_message="training iteration %d: running gradient descent" % (k,),
                bar_color="cyan", verbose=show_progress_bars) as bar:
                for t in training_data:
                    math_util.TensorSum(
                        self._weights,
                        self._WeightsGradient(t, learning_rate))
                    bar.Increment()

            # Apply L2 Regularization to self._weights.
            math_util.TensorDifference(
                self._weights,
                self._RegularizationGradient(regularization_rate))
