import gzip
import math
import progress_bar
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

def MnistData(verbose=False):
    training_data = ReadMnistData(
        MNIST_TRAINING_FILES[0], MNIST_TRAINING_FILES[1], verbose=verbose)
    test_data = ReadMnistData(
        MNIST_TEST_FILES[0], MNIST_TEST_FILES[1], verbose=verbose)

    return (training_data, test_data)

def ReadMnistData(image_file_path, label_file_path, verbose=False):
    data = []

    message = "loading: %s" % (image_file_path,)
    with gzip.open(image_file_path, "rb") as image_file:
        # MNIST image files should have a magic number equal to 2051 in Big
        # Endian notation in the first 4 bytes of the file.
        magic_number = struct.unpack(">I", image_file.read(4))[0]
        assert magic_number == 2051, "magic number: %s" % (magic_number,)

        number_of_examples = struct.unpack(">I", image_file.read(4))[0]
        rows = struct.unpack(">I", image_file.read(4))[0]
        columns = struct.unpack(">I", image_file.read(4))[0]

        with progress_bar.ProgressBar(
            number_of_examples, start_message=message, bar_color="red",
            verbose=verbose) as bar:
            cells_per_image = rows * columns
            fmt = "B" * (cells_per_image)
            for i in range(number_of_examples):
                current_image = list(
                    struct.unpack(fmt, image_file.read(cells_per_image)))
                data.append([current_image])
                bar.Increment()

    message = "loading: %s" % (label_file_path,)
    with gzip.open(label_file_path, "rb") as label_file:
        # MNIST label files should have a magic number equal to 2049 in Big
        # Endian notation in the first 4 bytes of the file.
        magic_number = struct.unpack(">I", label_file.read(4))[0]
        assert magic_number == 2049

        number_of_examples = struct.unpack(">I", label_file.read(4))[0]

        with progress_bar.ProgressBar(
            number_of_examples, start_message=message, bar_color="red",
            verbose=verbose) as bar:
            for i in range(number_of_examples):
                data[i].append(struct.unpack("B", label_file.read(1))[0])
                bar.Increment()

    return data

def PrintTrainingData(indices, verbose=False):
    training_data, test_data = MnistData(verbose=verbose)

    for i in indices:
        print "training example %d:\n%s" % (i, MnistImageAsString(training_data[i][0]))
        print "excpeted label: %d" % (training_data[i][1],)

def MnistImageAsString(image):
    # The input image is a single dimensional array with the cells of row 1,
    # then the cells of row 2, etc.
    output = ""
    side_length = int(math.sqrt(len(image)))
    for r in range(side_length):
        for c in range(side_length):
            color = None
            if 0 <= image[(r * side_length) + c] < 64:
                color = "on_white"
            elif 64 <= image[(r * side_length) + c] < 192:
                color = "on_yellow"
            else:
                color = "on_red"
            output += termcolor.colored("  ", on_color=color)
        output += "\n"
    return output
