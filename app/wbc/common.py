import logging
from os import environ


def get_app_version():
    """
    Get the short (7 chars) git commit hash of the current code version

    :rtype: str
    """
    return environ.get('GIT_HASH', 'dev')[0:7]


class LoggableMixin(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
