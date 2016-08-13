import logging

import pymysql


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
                charset='utf8',
                connect_timeout=3,
                read_timeout=3,
                write_timeout=3,
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
        self._logger.debug('Query: {}'.format(query.replace("\n", ' ')))

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

    def get_meta(self):
        """
        Return meta-data for the previous query
        :type: dict
        """
        # @see http://sphinxsearch.com/docs/current/sphinxql-show-meta.html
        res = self.query('SHOW META')

        return {row['Variable_name']: row['Value'] for row in res}

    def get_sphinx_version(self):
        """
        Return Sphinx version string
        :rtype: str
        """
        return 'Sphinx v{}'.format(self._connection.get_server_info())
