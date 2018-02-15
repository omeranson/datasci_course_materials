import collections
import MapReduce
import sys

"""
Matrix Multiplication
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def sizeof(matrix):
    return (5,5)  # Both matrices are 5 x 5.

def mapper(record):
    # key: document identifier
    # value: document contents
    matrix, idx1, idx2, value = tuple(record)
    size = sizeof('a')[1]
    if matrix == 'a':
        for k in range(size):
            mr.emit_intermediate((idx1, k), record)
    elif matrix == 'b':
        for k in range(size):
            mr.emit_intermediate((k, idx2), record)

def reducer(key, list_of_values):
    running_count = sizeof('a')[1]
    a = [0] * running_count
    b = [0] * running_count
    for record in list_of_values:
        matrix, idx1, idx2, value = tuple(record)
        if matrix == 'a':
            a[idx2] = value
        elif matrix == 'b':
            b[idx1] = value
    cell_value = sum((e_a*e_b for e_a, e_b in zip(a,b)))
    idx1, idx2 = key
    mr.emit((idx1, idx2, cell_value))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
