import logging

import pymysql
from flask import g


class Sphinx(object):
    """
    @see https://github.com/PyMySQL/PyMySQL#example
    @see http://pymysql.readthedocs.io/en/latest/
    """
    def __init__(self, host, port):
        """
        :type host str
        :type port int
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._host = host
        self._port = port
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            self._logger.debug("Connecting to {}:{}".format(self._host, self._port))

            self._connection = pymysql.Connect(
                host=self._host,
                port=self._port,
                use_unicode=True,
                connect_timeout=3,
                cursorclass=pymysql.cursors.DictCursor,
            )

            self._logger.debug("Connected to {}:{}".format(self._host, self._port))

        return self._connection

    def query(self, query, args=None):
        """
        :type query str
        :type args list
        :rtype: list
        """
        self._logger.info('Query: {}'.format(query))

        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            res = cursor.fetchall()
            return res

    def get_indices(self):
        """
        :rtype: list
        """
        res = self.query('SHOW TABLES')
        return [row['Index'] for row in res]


def get_sphinx():
    if not hasattr(g, '__sphinx'):
        # TODO: customize values
        g.__sphinx = Sphinx(
            host='127.0.0.1',
            port=36307
        )

    return g.__sphinx
