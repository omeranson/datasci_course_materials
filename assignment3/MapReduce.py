import json

class FunctionWrapper(object):
    def __init__(self, mapper, reducer):
        self._mapper = mapper
        self._reducer = reducer

    def mapper(self, mr, record):
        self._mapper(mr, record)

    def reducer(self, mr, key, iterator):
        self._reducer(mr, key, iterator)

class MapReduceBase(object):
    def __init__(self):
        self.intermediate = {}
        self.result = []

    def emit_intermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)

    def emit(self, value):
        self.result.append(value) 

    def execute(self, data, impl):
        for record in data:
            impl.mapper(self, record)
        for key in self.intermediate:
            impl.reducer(self, key, self.intermediate[key])


class MapReduce(MapReduceBase):
    def execute(self, data, impl):
        jsonned_data = (json.loads(line) for line in data)
        super(MapReduce, self).execute(jsonned_data, impl)

        #jenc = json.JSONEncoder(encoding='latin-1')
        jenc = json.JSONEncoder()
        for item in self.result:
            print jenc.encode(item)
