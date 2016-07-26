class Model(object):

    def __init__(self, **values):
        self._values = values

    def __getitem__(self, item):
        return self._values.get(item)

    def to_json(self):
        """
        Returns JSON-izable object for API representation

        :rtype dict
        """
        raise NotImplementedError('{}.to_json needs to be implemented'.format(self.__class__.__name__))
