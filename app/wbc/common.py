import logging
from os import environ

try:
    from html import escape  # python 3.x
except ImportError:
    from cgi import escape  # python 2.x


def get_app_version():
    """
    Get the short (7 chars) git commit hash of the current code version

    :rtype: str
    """
    return environ.get('GIT_HASH', 'dev')[0:7]


def encode_html(s):
    """
    Encode given string to be safely embedded in the code

    @see https://stackoverflow.com/a/7088472/5446110

    :type s str
    :rtype: str
    """
    return escape(s)


class LoggableMixin(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
