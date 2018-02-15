import MapReduce
import sys

"""
Asymetric friendship
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    person = record[0]
    mr.emit_intermediate(person, record)
    friend = record[1]
    mr.emit_intermediate(friend, record)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    # Return following - followers
    # following = record[1] where record[0] == key
    # followers = record[0] where record[1] == key
    following = set()
    followers = set()
    for record in list_of_values:
        if record[0] == key:
            following.add(record[1])
        if record[1] == key:
            followers.add(record[0])
    asymetric = following - followers
    for asymetric_friend in asymetric:
        mr.emit((asymetric_friend, key))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
