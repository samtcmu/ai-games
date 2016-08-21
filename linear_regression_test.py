import linear_regression
import random

def LinearRegressionTest():
    expected_weights = [1.0, 2.0, 3.0]
    training_data = CreateTrainingData(expected_weights, 1000, -100.0, 100.0)
    test_data = CreateTrainingData(expected_weights, 500, -100.0, 100.0)

    model = linear_regression.LinearRegression(len(expected_weights))
    model.RandomizeSynapticWeights(random_range=(-1.0, 1.0))
    model.Train(training_data,
                learning_rate=0.00000001,
                learning_iterations=200,
                verbose=True)

    total_difference = 0
    for t in test_data:
        total_difference += abs(model.Infer(t[0]) - t[1])
    print "average absolute difference on test data: %.3f" % (total_difference / len(test_data),)
    
def CreateTrainingData(weights, num_training_examples, low, high):
    training_data = []
    for i in range(num_training_examples):
        input_data = RandomVector(len(weights), low, high)
        expected_output = (
            linear_regression.VectorDotProduct(input_data, weights) + 
            random.gauss(0.0, 5.0))
        training_data.append([input_data, expected_output])
    return training_data
        
def RandomVector(size, low, high):
    return [random.uniform(low, high) for _ in range(size)] 
