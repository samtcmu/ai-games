import list_util
import math
import math_util
import mnist_data_loader
import neural_network
import numpy
import pickle
import progress_bar
import random

def NeuralNetworkTest(learning_iterations=10000, verbose=True):
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
                learning_iterations=learning_iterations,
                regularization_rate=0.0,
                verbose=verbose)
    # scaling_factor = 4.0
    # model._weights = [
    #     numpy.array([weights]) / (2000.0 * scaling_factor),
    #     numpy.array([[2.0, 4.0]]) * scaling_factor,
    # ]

    print model
    total_difference = 0
    for t in test_data:
        actual = math_util.InverseSigmoid(
            model.Infer(t[0])[0], max_value=2000.0)
        expected = math_util.InverseSigmoid(t[1][0], max_value=2000.0)
        difference = abs(actual - expected)
        if verbose and False:
            print "%s %s %s" % ("{0:9,.4f}".format(actual),
                                "{0:9,.4f}".format(expected),
                                "{0:9,.4f}".format(difference))
        total_difference += difference
    print "average absolute difference on test data: %.3f" % (
        total_difference / len(test_data),)
    print "noise standard deviation around linear data: %.3f" % (noise_stdev,)

def MnistTest(model_path_prefix="output/mnist/nn-model",
              hidden_layer_widths=[30], learning_iterations=100, verbose=False,
              show_progress_bars=True):
    training_data, test_data = mnist_data_loader.MnistData(
        verbose=show_progress_bars)

    validation_data = training_data[-len(training_data) / 6:]
    training_data = training_data[:-len(training_data) / 6]

    transformed_training_data = TransformMnistData(
        training_data, description="training-data", verbose=show_progress_bars)
    transformed_validation_data = TransformMnistData(
        validation_data, description="validation-data",
        verbose=show_progress_bars)
    transformed_test_data = TransformMnistData(
        test_data, description="test-data", verbose=show_progress_bars)

    model = neural_network.NeuralNetwork(
        input_width=len(transformed_training_data[0][0]),
        output_width=len(transformed_training_data[0][1]),
        hidden_layer_widths=hidden_layer_widths)
    model.RandomizeWeights(random_range=(-1.0, 1.0))
    model.Train(transformed_training_data,
                learning_rate=0.05,
                learning_iterations=learning_iterations,
                regularization_rate=0.001,
                model_path_prefix=model_path_prefix,
                verbose=verbose,
                show_progress_bars=show_progress_bars)

def EvaluateNeuralNetworkOnMnist(model_file_path, verbose=False):
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

    EvaluateMnistDataWithModel(transformed_validation_data,
                               model,
                               data_name="validation data",
                               model_name=model_file_path,
                               verbose=verbose)
    EvaluateMnistDataWithModel(transformed_training_data,
                               model,
                               data_name="training data",
                               model_name=model_file_path,
                               verbose=verbose)
    print "model fitness: {:12,.4f}".format(
        model.Fitness(transformed_training_data, 0, verbose=verbose))

def EvaluateMnistDataWithModel(mnist_data, model, data_name="mnist-data",
                               model_name="model", verbose=False):
    with progress_bar.ProgressBar(
        len(mnist_data),
        start_message="evaluating %s with model: %s" % (
            data_name, model_name),
        bar_color="cyan", verbose=verbose) as bar:
        correct_classifications = 0
        for i in range(len(mnist_data)):
            [t, c] = mnist_data[i]

            classification = model.Infer(t)
            label = list_util.MaxIndex(classification)
            if label == list_util.MaxIndex(c):
                correct_classifications += 1

            bar.Increment()

    print "performance on %s: %d / %d (%3.2f %%)\n" % (
        data_name, correct_classifications, len(mnist_data),
        100.0 * (float(correct_classifications) / len(mnist_data)))

def TransformMnistData(mnist_data, description="mnist-data", verbose=False):
    with progress_bar.ProgressBar(
        len(mnist_data),
        start_message="transforming: %s" % (description,),
        bar_color="green", verbose=verbose) as bar:
        transformed_mnist_data = []
        for i in range(len(mnist_data)):
            image, label = mnist_data[i]

            transformed_label = [0.0 for _ in range(10)]
            transformed_label[label] = 1.0

            transformed_image = [x / 255.0 for x in image]

            transformed_mnist_data.append([transformed_image, transformed_label])

            bar.Increment()

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
