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

    def escape_string(self, val):
        """
        :type val str
        :rtype: str
        """

        return self.connection.escape_string(val)

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

    def call_suggest(self, query, index, limit=20, **kwargs):
        """
        :type query str
        :type index str
        :type limit int
        :rtype: list
        """
        query = query.lower()

        # @see http://sphinxsearch.com/blog/2016/10/03/2-3-2-feature-built-in-suggests/
        parts = [
            "'{}'".format(self.escape_string(query)),
            "'{}'".format(self.escape_string(index)),
            '{} as limit'.format(int(limit)*10)
        ]

        for key, val in kwargs.items():
            parts.append('{} as {}'.format(int(val), key))  # e.g. limit, max_edits, delta_len

        res = self.query("CALL SUGGEST({})".format(', '.join(parts)))

        # sort by 'docs' ASC
        # {'suggest': 'marcinkowski', 'distance': '3', 'docs': '303'}
        res = sorted(res, reverse=True, key=lambda item: int(item['docs']))

        # all suggestions should start with a query phrase
        res = list(filter(lambda item: item['suggest'].startswith(query), res))

        # take the top "limit" items and then sort them alphabetically
        return sorted(item['suggest'] for item in res[:limit])

    def get_indices(self):
        """
        :rtype: list
        """
        res = self.query('SHOW TABLES')
        return [row['Table'] for row in res]

    def get_meta(self):
        """
        Return meta-data for the previous query
        :rtype: dict
        """
        # @see http://sphinxsearch.com/docs/current/sphinxql-show-meta.html
        res = self.query('SHOW META')

        return {row['Variable_name']: row['Value'] for row in res}

    def get_index_meta(self, index_name):
        """
        Return meta-data for a given index

mysql> show index wbc status;
+-------------------+-----------+
| Variable_name     | Value     |
+-------------------+-----------+
| index_type        | disk      |
| indexed_documents | 6965      |
| indexed_bytes     | 122364117 |
| ram_bytes         | 131733889 |
| disk_bytes        | 194437182 |
+-------------------+-----------+
5 rows in set (0.00 sec)

        :type index_name str
        :rtype: dict
        """
        res = self.query('SHOW INDEX {} STATUS'.format(index_name))
        return {row['Variable_name']: row['Value'] for row in res}

    def get_sphinx_version(self):
        """
        Return Sphinx version string
        :rtype: str
        """
        return 'Sphinx v{}'.format(self._connection.get_server_info())
