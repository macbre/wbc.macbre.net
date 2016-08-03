import logging

from flask import g
from redis import StrictRedis

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


def get_redis():
    """
    :rtype: StrictRedis
    """
    # @see https://pypi.python.org/pypi/redis
    from os import environ

    if not hasattr(g, '__redis'):
        g.__redis = StrictRedis(
            host=environ.get('REDIS_HOST', 'redis'),
            port=6379,
            db=0
        )

        logger = logging.getLogger('get_redis')
        logger.info('Connected to {}'.format(g.__redis))

    return g.__redis
