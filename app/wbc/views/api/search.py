from math import ceil

from flask import jsonify, request, url_for
from flask.views import MethodView

from wbc.common import LoggableMixin, encode_html
from wbc.connectors import get_sphinx
from wbc.exceptions import WBCApiError
from wbc.models import DocumentModel


class SearchableMixin(LoggableMixin):
    # @see http://sphinxsearch.com/docs/current/sphinxql-select.html
    # @see http://sphinxsearch.com/docs/current/api-func-buildexcerpts.html
    # @see http://sphinxsearch.com/docs/current/sphinxql-call-snippets.html
    QUERY = """
SELECT
    id,
    SNIPPET(title, '{query}', 'limit=150', 'around=15','before_match=<mark>', 'after_match=</mark>') as document_name,
    chapter,
    SNIPPET(content, '{query}', 'limit=300', 'around=85', 'before_match=[mark]', 'after_match=[/mark]') as snippet,
    read_time,
    published_year,
    publication_id,
    document_id AS issue_id
FROM wbc
WHERE match('{query}*'){where}
ORDER BY published_year ASC
LIMIT 150
"""
    INDEX = 'wbc'

    def search(self, issue_id=None):
        """
        Perform a search and format the results

        :type issue_id int
        """
        query = self._get_search_query()

        try:
            results, stats = self._get_results(self._get_search_query(), issue_id=issue_id)
        except Exception as e:
            raise WBCApiError('Error while searching: {} {}'.format(e.__class__, str(e)))

        return jsonify({
            'query': query,
            'results': results,
            'stats': stats
        })

    def _format_results(self, res):

        results = []

        for row in res:
            document = DocumentModel(**row)

            snippet = encode_html(document['snippet'])
            snippet = snippet.\
                replace('[mark]', '<mark>').\
                replace('[/mark]', '</mark>')

            results.append({
                'id': int(document['id']),
                'name': document['chapter'],
                '_links': {
                    'self': {'href': url_for('documents', document_id=document['id'])},
                    'html': {'href': document.get_full_url()},
                },
                # the issue where this document is in
                'issue': {
                    'id': int(document['issue_id']),
                    'name': document['document_name'],
                    'published_year': int(document['published_year']),
                    '_links': {
                        'self': {'href': url_for('issues', issue_id=document['issue_id'])}
                    },
                },
                # the publication where this issue is in
                'publication': {
                    'id': int(document['publication_id']),
                    '_links': {
                        'self': {'href': '/publications/{}'.format(document['publication_id'])}  # TODO - app.get_url
                    },
                },
                # the document details
                'snippet': snippet,
                # read time
                'read_time': ceil(document.get_read_time() / 60)
            })

        return results

    def _get_results(self, query, issue_id=None):
        """
        :type query str
        :type issue_id int
        :rtype: list
        """
        sphinx = get_sphinx()

        conditions = list(filter(None, [
            'issue_id={}'.format(int(issue_id)) if issue_id is not None else ''
        ]))

        self._logger.debug("Searching for '{}' ({})".format(query, conditions))

        query_escaped = sphinx.connection.escape_string(query)
        res = sphinx.query(self.QUERY.format(
            query=query_escaped.replace("\n", ' '),
            where=' AND '.join([''] + conditions)
        ))

        results = self._format_results(res)

        meta = sphinx.get_meta()
        stats = {
            'total': int(meta['total']),
            'took': float(meta['time']),
            'powered_by': sphinx.get_sphinx_version(),
        }

        return results, stats

    def is_searchable(self):
        """
        Checks if the current request has a proper "q" parameter

        :rtype: bool
        """
        return self._get_search_query() != ''

    @staticmethod
    def _get_search_query():
        """
        Returns "q" parameter

        :rtype: str
        """
        query = request.args.get('q', '').strip()
        return query


class Search(MethodView, SearchableMixin):
    def get(self):
        # validate queries
        if not self.is_searchable():
            raise WBCApiError('Query string is empty, "q" URL parameter is missing', 400)

        return self.search()
