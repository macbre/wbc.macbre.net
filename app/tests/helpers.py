from flask import g


def get_sphinx_mock(query, res):

    class SphinxMock(object):
        @staticmethod
        def query(_query):
            assert _query == query, 'Sphinx mock got different query than expected'
            return res

    g.__sphinx = SphinxMock()
    return g.__sphinx
