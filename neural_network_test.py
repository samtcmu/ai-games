import linear_regression
import list_util
import math
import math_util
import mnist_data_loader
import neural_network
import pickle
import random
import sys
import termcolor

def InverseSigmoid(x):
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
        actual = InverseSigmoid(model.Infer(t[0])[0])
        expected = InverseSigmoid(t[1][0])
        difference = abs(actual - expected)
        print "%s %s %s" % ("{0:9,.4f}".format(actual),
                            "{0:9,.4f}".format(expected),
                            "{0:9,.4f}".format(difference))
        total_difference += difference
    print "average absolute difference on test data: %.3f" % (
        total_difference / len(test_data),)
    print "noise standard deviation around linear data: %.3f" % (noise_stdev,)

def MnistTest(verbose=False):
    training_data, test_data = mnist_data_loader.MnistData(verbose=verbose)

    validation_data = training_data[-len(training_data) / 6:]
    training_data = training_data[:-len(training_data) / 6]

    transformed_training_data = TransformMnistData(
        training_data, description="training-data", verbose=verbose)
    transformed_validation_data = TransformMnistData(
        validation_data, description="validation-data", verbose=verbose)
    transformed_test_data = TransformMnistData(
        test_data, description="test-data", verbose=verbose)

    model = neural_network.NeuralNetwork(
        input_width=len(transformed_training_data[0][0]),
        output_width=len(transformed_training_data[0][1]),
        hidden_layer_widths=[15])
    model.RandomizeWeights(random_range=(-1.0, 1.0))
    model.Train(transformed_training_data,
                learning_rate=0.00001,
                learning_iterations=100,
                regularization_rate=0.001,
                verbose=True)

def EvaluateNeuralNetowrk(model_file_path, verbose=False):
    training_data, test_data = mnist_data_loader.MnistData(verbose=verbose)

    validation_data = training_data[-len(training_data) / 6:]
    training_data = training_data[:-len(training_data) / 6]

    transformed_training_data = TransformMnistData(
        training_data, description="training-data", verbose=verbose)
    transformed_validation_data = TransformMnistData(
        validation_data, description="validation-data", verbose=verbose)
    transformed_test_data = TransformMnistData(
        test_data, description="test-data", verbose=verbose)

    model = None
    with open(model_file_path, "r") as model_file:
        model = pickle.load(model_file)

    if verbose:
        print "evaluating model: %s" % (model_file_path,)
        print "progress: start" + (" " * 50) + "end"
        print "              [",

    correct_classifications = 0
    for i in range(len(transformed_validation_data)):
        [t, c] = transformed_validation_data[i]

        classification = model.Infer(t)
        label = list_util.MaxIndex(classification)
        if label == list_util.MaxIndex(c):
            correct_classifications += 1

        if verbose and (i % (len(transformed_validation_data)/ 50) == 0):
            sys.stdout.write(termcolor.colored("=", color="yellow"))
            sys.stdout.flush()

    if verbose:
        print "]\n"

    print "performance on training data: %d / %d (%3.2f %%)" % (
        correct_classifications, len(transformed_validation_data),
        100.0 * (float(correct_classifications) / len(transformed_validation_data)))

def TransformMnistData(mnist_data, description="mnist-data", verbose=False):
    if verbose:
        print "transforming: %s" % (description,)
        print "progress: start" + (" " * 50) + "end"
        print "              [",

    transformed_mnist_data = []
    for i in range(len(mnist_data)):
        image, label = mnist_data[i]

        transformed_label = [0.0 for _ in range(10)]
        transformed_label[label] = 1.0

        transformed_image = [x / 255.0 for x in image]

        transformed_mnist_data.append([transformed_image, transformed_label])

        if verbose and (i % (len(mnist_data)/ 50) == 0):
            sys.stdout.write(termcolor.colored("=", color="yellow"))
            sys.stdout.flush()

    if verbose:
        print "]\n"

    return transformed_mnist_data

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
