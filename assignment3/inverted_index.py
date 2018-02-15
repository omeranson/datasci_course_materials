import MapReduce
import sys

"""
Inverted index
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    document_id = record[0]
    text = record[1]
    words = text.split()
    for w in words:
      mr.emit_intermediate(w, document_id)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    result = set(list_of_values)
    mr.emit((key, list(result)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
