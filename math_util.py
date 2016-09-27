import math

def VectorDotProduct(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return sum(A[i] * B[i] for i in range(len(A)))

def VectorScalarProduct(c, A):
    return [c * A[i] for i in range(len(A))]

def VectorSum(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return [A[i] + B[i] for i in range(len(A))]

def VectorDifference(A, B):
    return VectorSum(A, VectorScalarProduct(-1.0, B))

def VectorMagnitude(A):
    return math.sqrt(sum(a**2 for a in A))

def MatrixTranspose(A):
    output = [[0.0 for j in range(len(A))] for i in range(len(A[0]))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            output[j][i] = A[i][j]
    return output

def MatrixMult(A, B):
    assert len(A[0]) == len(B), "len(A[0]) = %d, len(B) = %d" % (len(A[0]), len(B))
    output = [[0.0 for j in range(len(B[0]))] for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[i])):
                output[i][j] += A[i][k] * B[k][j]
    return output

def MatrixSum(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))]
                               for i in range(len(A))]

def MatrixDifference(A, B):
    return MatrixSum(A, MatrixScalarProduct(-1.0, B))

def MatrixScalarProduct(c, A):
    return [[c * A[i][j] for j in range(len(A[0]))]
                         for i in range(len(A))]

def Sigmoid(x):
    try:
        return (1.0 / (1.0 + math.exp(-1.0 * x)))
    except OverflowError:
        return 1.0 if x > 0 else 0.0
