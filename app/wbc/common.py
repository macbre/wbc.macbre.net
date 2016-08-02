import logging


class LoggableMixin(object):
    def __init__(self):
        self._logging = logging.getLogger(self.__class__.__name__)
