import math

def VectorDotProduct(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return sum(A[i] * B[i] for i in xrange(len(A)))

def VectorHadamardProduct(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return [A[i] * B[i] for i in xrange(len(A))]

def VectorHadamardProduct3(A, B, C):
    assert len(A) == len(B) == len(C), "len(A) = %d, len(B) = %d, len(C) = %d" % (
        len(A), len(B), len(C))
    return [A[i] * B[i] * C[i] for i in xrange(len(A))]

def VectorScalarProduct(c, A):
    return [c * A[i] for i in xrange(len(A))]

def VectorSum(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return [A[i] + B[i] for i in xrange(len(A))]

def VectorDifference(A, B):
    return VectorSum(A, VectorScalarProduct(-1.0, B))

def VectorMagnitude(A):
    return math.sqrt(sum(a**2 for a in A))

def MatrixTranspose(A):
    output = [[0.0 for j in xrange(len(A))] for i in xrange(len(A[0]))]
    for i in xrange(len(A)):
        for j in xrange(len(A[0])):
            output[j][i] = A[i][j]
    return output

def MatrixMult(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    assert cols_A == rows_B, "len(A[0]) = %d, len(B) = %d" % (cols_A, rows_B)
    output = [[0.0 for j in xrange(cols_B)] for i in xrange(rows_A)]
    for i in xrange(rows_A):
        for j in xrange(cols_B):
            for k in xrange(cols_A):
                output[i][j] += A[i][k] * B[k][j]
    return output

def MatrixVectorMult(A, b):
    rows_A, cols_A = len(A), len(A[0])
    rows_b = len(b)

    assert cols_A == rows_b, "len(A[0]) = %d, len(b) = %d" % (cols_A, rows_b)
    output = [0.0 for _ in xrange(rows_A)]
    for i in xrange(rows_A):
        for j in xrange(rows_b):
            output[i] += A[i][j] * b[j]

    return output

def MatrixHadamardProduct(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    assert (rows_A == rows_B) and (cols_A == cols_B), (
        "A = %d x %d, B = %d x %d" % (rows_A, cols_A, rows_B, cols_B))

    output = [[0.0 for _ in r] for r in A]
    for i in xrange(rows_A):
        for j in xrange(cols_A):
            output[i][j] = A[i][j] * B[i][j]
    return output

def MatrixSum(A, B):
    return [[A[i][j] + B[i][j] for j in xrange(len(A[0]))]
                               for i in xrange(len(A))]

def MatrixDifference(A, B):
    return MatrixSum(A, MatrixScalarProduct(-1.0, B))

def MatrixScalarProduct(c, A):
    return [[c * A[i][j] for j in xrange(len(A[0]))]
                         for i in xrange(len(A))]

def TensorSum(A, B):
    for i in xrange(len(A)):
        len_A_i_j = len(A[i][0])
        for j in xrange(len(A[i])):
            for k in xrange(len_A_i_j):
                A[i][j][k] += B[i][j][k]

def TensorDifference(A, B):
    for i in xrange(len(A)):
        len_A_i_j = len(A[i][0])
        for j in xrange(len(A[i])):
            for k in xrange(len_A_i_j):
                A[i][j][k] -= B[i][j][k]

def TensorScalarProduct(c, A):
    return [[[c * A[i][j][k] for k in xrange(len(A[i][j]))]
                             for j in xrange(len(A[i]))]
                             for i in xrange(len(A))]

def Sigmoid(x):
    try:
        y = math.exp(x)
        return y / (y + 1.0)
    except OverflowError:
        return 1.0 if x > 0 else 0.0

def MatrixAsString(A, fmt=None):
    output = ""
    for r in xrange(len(A)):
        for c in xrange(len(A[r])):
            output += fmt.format(A[r][c])
        output += "\n"
    return output
