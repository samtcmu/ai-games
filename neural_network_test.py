import linear_regression
import math_util
import neural_network
import random

def NeuralNetworkTest():
    expected_weights = [200.0, 10.0, 200.0]
    noise_stdev = 5.0
    training_data = CreateTrainingData(
        expected_weights, 1000, -100.0, 100.0, noise_stdev=noise_stdev)
    test_data = CreateTrainingData(
        expected_weights, 500, -100.0, 100.0, noise_stdev=noise_stdev)

    model = neural_network.NeuralNetwork(input_width=len(expected_weights) - 1,
                                         output_width=1,
                                         hidden_layer_widths=[4, 2])
    model.RandomizeWeights(random_range=(-1.0, 1.0))
    model.Train(training_data,
                learning_rate=0.0000005,
                learning_iterations=10000,
                regularization_rate=0.0,
                verbose=True)

    total_difference = 0
    for t in test_data:
        total_difference += abs(model.Infer(t[0])[0] - t[1][0])
    print "average absolute difference on test data: %.3f" % (
        total_difference / len(test_data),)
    print "noise standard deviation around linear data: %.3f" % (noise_stdev,)

def CreateTrainingData(weights, num_training_examples, low, high,
                       noise_stdev=5.0):
    training_data = []
    for i in range(num_training_examples):
        input_data = [-1.0] + RandomVector(len(weights) - 1, low, high)
        expected_output = (
            math_util.VectorDotProduct(input_data, weights) +
            random.gauss(0.0, noise_stdev))
        training_data.append([input_data[1:], [expected_output]])
    return training_data

def RandomVector(size, low, high):
    return [random.uniform(low, high) for _ in range(size)]
