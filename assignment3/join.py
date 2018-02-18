import collections
import itertools
import sys

import MapReduce

"""
join
"""

# =============================
# Do not modify above this line

class Join(object):
    def join_params(self):
        """
        Return dict: table name -> field indexes. All records must have the
        same length
        """
        return ('order', 'line_item'), ((1,), (1,))

    def mapper(self, mr, record):
        table_name = record[0]
        join_params_dict = dict(zip(*self.join_params()))
        key = tuple(record[field] for field in join_params_dict[table_name])
        mr.emit_intermediate(key, record)

    def reducer(self, mr, key, list_of_values):
        # key: order_id
        # value: record
        records = collections.defaultdict(list)
        for value in list_of_values:
            table_name = value[0]
            records[table_name].append(value)
        keys = self.join_params()[0]
        records_split = (records.get(key, []) for key in keys)
        for rows in itertools.product(*records_split):
            join = sum(rows, [])
            mr.emit(join)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  join = Join()
  mr = MapReduce.MapReduce()
  mr.execute(inputdata, join)
