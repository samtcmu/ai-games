import math

def MaxIndex(L):
    max_index = 0
    for i in range(len(L)):
        if L[i] > L[max_index]:
            max_index = i
    return max_index

def MaxIndices(L):
    max_indices = [0]
    for i in range(1, len(L)):
        if L[i] > L[max_indices[0]]:
            max_indices = [i]
        elif L[i] == L[max_indices[0]]:
            # TODO(samt): Since we are comparing floating point numbers we
            # might want a better comparison method.
            max_indices.append(i)
    return max_indices

def Mean(L):
    return sum(L) / float(len(L))

def StandardDeviation(L):
    mean = Mean(L)
    return math.sqrt(sum((x - mean)**2 for x in L) / float(len(L)))
