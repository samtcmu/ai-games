import linear_regression
import math
import math_util
import neural_network
import random

def f(x):
    try:
        return -1.0 * (2000.0) * math.log((1.0 / x) - 1.0)
    except ZeroDivisionError:
        # x == 0.0
        return -2000.0
    except ValueError:
        # (1.0 / x) - 1.0 == 0.0
        return 2000.0

def NeuralNetworkTest():
    noise_stdev = 5.0
    inputs = 6
    weights = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    training_data = CreateLinearTrainingData(
        weights, 1000, -100.0, 100.0, noise_stdev=noise_stdev)
    test_data = CreateLinearTrainingData(
        weights, 500, -100.0, 100.0, noise_stdev=noise_stdev)

    model = neural_network.NeuralNetwork(input_width=len(weights) - 1,
                                         output_width=1,
                                         hidden_layer_widths=[])
    model.RandomizeWeights(random_range=(-1.0, 1.0))
    model.Train(training_data,
                learning_rate=0.000001,
                learning_iterations=3000,
                regularization_rate=0.001,
                verbose=True)

    total_difference = 0
    for t in test_data:
        actual = f(model.Infer(t[0])[0])
        expected = f(t[1][0])
        difference = abs(actual - expected)
        print "%s %s %s" % ("{0:9,.4f}".format(actual),
                            "{0:9,.4f}".format(expected),
                            "{0:9,.4f}".format(difference))
        total_difference += difference
    print "average absolute difference on test data: %.3f" % (
        total_difference / len(test_data),)
    print "noise standard deviation around linear data: %.3f" % (noise_stdev,)

def CreateTrainingData(inputs, num_training_examples, low, high,
                       noise_stdev=5.0):
    training_data = []
    for i in range(num_training_examples):
        input_data = RandomVector(inputs, low, high)
        expected_output = (
            math_util.VectorDotProduct(input_data, input_data) +
            random.gauss(0.0, noise_stdev))
        training_data.append([input_data, [expected_output]])
    return training_data

def CreateLinearTrainingData(weights, num_training_examples, low, high,
                             noise_stdev=5.0):
    training_data = []
    for i in range(num_training_examples):
        input_data = [-1.0] + RandomVector(len(weights) - 1, low, high)
        expected_output = math_util.Sigmoid(
            (math_util.VectorDotProduct(input_data, weights) +
            random.gauss(0.0, noise_stdev)) / 2000.0)
        training_data.append([input_data[1:], [expected_output]])
    return training_data

def RandomVector(size, low, high):
    return [random.uniform(low, high) for _ in range(size)]
