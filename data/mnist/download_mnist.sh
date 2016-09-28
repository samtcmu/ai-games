mnist_files="\
    http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz \
    http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz \
    http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz \
    http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"
for file in ${mnist_files}; do
    if [ ! -e `basename ${file}` ]; then
        wget ${file}
    else
        printf "%s already downloaded.\n\n" ${file}
    fi
done
