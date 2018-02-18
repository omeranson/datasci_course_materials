import collections
import json
import sys

import join
import MapReduce

"""
Matrix Multiplication
"""

# =============================
# Do not modify above this line

def sizeof(matrix):
    return (5,5)  # Both matrices are 5 x 5.

def mapper(mr, record):
    # record: 'a', idx1, idx2, value_a, 'b', idx2, idx3, value_b
    # return: key: idx1,idx3, value: value_a * value_b
    #
    # key: document identifier
    # value: document contents
    value = record[3]*record[7]
    key = (record[1], record[6])
    mr.emit_intermediate(key, value)

def reducer(mr, key, list_of_values):
    cell_value = sum(list_of_values)
    idx1, idx2 = key
    mr.emit((idx1, idx2, cell_value))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  jsonned_inputdata = (json.loads(line) for line in inputdata)
  class Join2(join.Join):
    def join_params(self):
        return (('a', 'b'), ((2,),(1,)))

  j = Join2()
  mr0 = MapReduce.MapReduceBase()
  mr0.execute(jsonned_inputdata, j)
  wrapper = MapReduce.FunctionWrapper(mapper, reducer)
  mr1 = MapReduce.MapReduceBase()
  mr1.execute(mr0.result, wrapper)
  jenc = json.JSONEncoder()
  for item in mr1.result:
      print jenc.encode(item)
