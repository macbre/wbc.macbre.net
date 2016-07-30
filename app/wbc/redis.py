# @see https://pypi.python.org/pypi/redis
import logging

from redis import StrictRedis
from flask import g


def get_redis():
    """
    :rtype: StrictRedis
    """
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
