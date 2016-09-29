import gzip
import pickle
import struct
import sys
import termcolor

MNIST_TRAINING_FILES = [
    "data/mnist/train-images-idx3-ubyte.gz",
    "data/mnist/train-labels-idx1-ubyte.gz",
]

MNIST_TEST_FILES = [
    "data/mnist/t10k-images-idx3-ubyte.gz",
    "data/mnist/t10k-labels-idx1-ubyte.gz",
]

def ProcessMnistData(training_data_path="output/mnist/training-data.dat",
                     test_data_path="output/mnist/test-data.dat",
                     verbose=False):
    training_data = ReadMnistData(
        MNIST_TRAINING_FILES[0], MNIST_TRAINING_FILES[1], verbose=verbose)
    test_data = ReadMnistData(
        MNIST_TEST_FILES[0], MNIST_TEST_FILES[1], verbose=verbose)

    with open(training_data_path, "w") as training_data_file:
        print "Saving training data to: %s" % (training_data_path,)
        pickle.dump(training_data, training_data_file)

    with open(test_data_path, "w") as test_data_file:
        print "Saving test data to: %s" % (test_data_path,)
        pickle.dump(test_data, test_data_file)

def ProcessedMnistData(training_data_path="output/mnist/training-data.dat",
                       test_data_path="output/mnist/test-data.dat"):
    training_data = None
    with open(training_data_path, "w") as training_data_file:
        training_data = pickle.load(training_data_file)

    test_data = None
    with open(test_data_path, "w") as test_data_file:
        test_data = pickle.load(test_data_file)

    return (training_data, test_data)

def PrintMnistImage(image):
    output = ""
    for r in range(len(image)):
        for c in range(len(image[r])):
            color = None
            if 0 <= image[r][c] < 64:
                color = "on_white"
            elif 64 <= image[r][c] < 192:
                color = "on_yellow"
            else:
                color = "on_red"
            output += termcolor.colored("  ", on_color=color)
        output += "\n"
    return output

def ReadMnistData(image_file_path, label_file_path, verbose=False):
    data = []

    if verbose:
        print "loading: %s" % (image_file_path,)
        print "progress: start" + (" " * 50) + "end"
        print "              [",

    with gzip.open(image_file_path, "rb") as image_file:
        # MNIST image files should have a magic number equal to 2051 in Big
        # Endian notation in the first 4 bytes of the file.
        magic_number = struct.unpack(">I", image_file.read(4))[0]
        assert magic_number == 2051, "magic number: %s" % (magic_number,)

        number_of_examples = struct.unpack(">I", image_file.read(4))[0]
        rows = struct.unpack(">I", image_file.read(4))[0]
        columns = struct.unpack(">I", image_file.read(4))[0]

        for i in range(number_of_examples):
            current_image = []
            for r in range(rows):
                current_image.append([])
                for c in range(columns):
                    current_image[-1].append(
                        struct.unpack("B", image_file.read(1))[0])
            data.append([current_image])

            if verbose and (i % (number_of_examples / 50) == 0):
                sys.stdout.write(termcolor.colored("=", color="yellow"))
                sys.stdout.flush()
    if verbose:
        print "]\n"
            
    if verbose:
        print "loading: %s" % (label_file_path,)
        print "progress: start" + (" " * 50) + "end"
        print "              [",

    with gzip.open(label_file_path, "rb") as label_file:
        # MNIST label files should have a magic number equal to 2049 in Big
        # Endian notation in the first 4 bytes of the file.
        magic_number = struct.unpack(">I", label_file.read(4))[0]
        assert magic_number == 2049

        number_of_examples = struct.unpack(">I", label_file.read(4))[0]
        for i in range(number_of_examples):
            data[i].append(struct.unpack("B", label_file.read(1))[0])

            if verbose and (i % (number_of_examples / 50) == 0):
                sys.stdout.write(termcolor.colored("=", color="yellow"))
                sys.stdout.flush()

    if verbose:
        print "]\n"

    return data
