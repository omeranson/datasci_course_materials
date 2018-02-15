import collections
import itertools
import sys

import MapReduce

"""
join
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # table_name = record[0]  # But we don't really need it
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_values):
    # key: order_id
    # value: record
    records = collections.defaultdict(list)
    for value in list_of_values:
        table_name = value[0]
        records[table_name].append(value)
    for o, li in itertools.product(records['order'], records['line_item']):
        mr.emit(o+li)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
