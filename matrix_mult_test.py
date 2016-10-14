import numpy as np;
import random

def MatrixMult(A, B):
    output = [[0.0 for j in range(len(B[0]))] for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[i])):
                output[i][j] += A[i][k] * B[k][j]
    return output

def CustomTest(n=10, verbose=False):
    F = [[0.0, 1.0], [1.0, 1.0]]
    f = [[0.0], [1.0]]
    for i in range(n):
        f = MatrixMult(F, f)
        if verbose:
            print f

def NumpyTest(n=10, verbose=False):
    F = np.array([[0.0, 1.0], [1.0, 1.0]])
    f = np.array([[0.0], [1.0]])
    for i in range(n):
        f = np.dot(F, f)
        if verbose:
            print f

def NumpyRandomTest(n=10, k=1, verbose=False):
    F = np.array([[random.uniform(-1.0, 1.0) for _ in xrange(n)]
                                             for _ in xrange(n)])
    f = np.array([[random.uniform(-1.0, 1.0)] for _ in xrange(n)])
    for i in range(k):
        f = np.dot(F, f)
        if verbose:
            print f

def CustomRandomTest(n=10, k=1, verbose=False):
    F = [[random.uniform(-1.0, 1.0) for _ in xrange(n)]
                                    for _ in xrange(n)]
    f = [[random.uniform(-1.0, 1.0)] for _ in xrange(n)]
    for i in range(k):
        f = MatrixMult(F, f)
        if verbose:
            print f

def NumpyRandomColumnRowTest(n=10, k=1, verbose=False):
    for i in range(k):
        a = np.array([[random.uniform(-1.0, 1.0)] for _ in xrange(n)])
        b = np.array([[random.uniform(-1.0, 1.0) for _ in xrange(n)]])
        c = np.dot(a, b)
        if verbose:
            print c

def CustomRandomColumnRowTest(n=10, k=1, verbose=False):
    for i in range(k):
        a = [[random.uniform(-1.0, 1.0)] for _ in xrange(n)]
        b = [[random.uniform(-1.0, 1.0) for _ in xrange(n)]]
        c = MatrixMult(a, b)
        if verbose:
            print c
