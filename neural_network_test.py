import linear_regression
import neural_network
import random

def NeuralNetworkTest():
    model = neural_network.NeuralNetwork(input_width=2,
                                         output_width=1,
                                         hidden_layer_widths=[3, 2])
    model.RandomizeWeights(random_range=(-100.0, 100.0))
    print model
