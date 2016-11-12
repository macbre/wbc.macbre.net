from flask import g

from .sphinx import Sphinx


def get_sphinx():
    """
    :rtype: Sphinx
    """
    from os import environ

    if not hasattr(g, '__sphinx'):
        g.__sphinx = Sphinx(
            host=environ.get('SPHINX_HOST', 'sphinx'),
            port=36307
        )

    return g.__sphinx
