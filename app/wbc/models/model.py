class Model(object):

    def __init__(self, **values):
        self._values = values

    def __getitem__(self, item):
        return self._values.get(item)
