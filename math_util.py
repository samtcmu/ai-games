import math

def VectorDotProduct(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return sum(A[i] * B[i] for i in range(len(A)))

def VectorScalarProduct(c, A):
    return [c * A[i] for i in range(len(A))]

def VectorDifference(A, B):
    return VectorSum(A, VectorScalarProduct(-1.0, B))

def VectorSum(A, B):
    assert len(A) == len(B), "len(A) = %d, len(B) = %d" % (len(A), len(B))
    return [A[i] + B[i] for i in range(len(A))]

def VectorMagnitude(A):
    return math.sqrt(sum(a**2 for a in A))
