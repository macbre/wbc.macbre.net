from flask import jsonify, request, url_for
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.sphinx import get_sphinx


class Search(MethodView):
    # @see http://sphinxsearch.com/docs/current/api-func-buildexcerpts.html
    # @see http://sphinxsearch.com/docs/current/sphinxql-call-snippets.html
    QUERY = """
SELECT
    id,
    SNIPPET(title, '{query}', 'limit=150', 'around=15','before_match=<mark>', 'after_match=</mark>') as document_name,
    chapter,
    SNIPPET(content, '{query}', 'around=500', 'before_match=<mark>', 'after_match=</mark>') as snippet,
    published_year,
    publication_id,
    document_id
FROM wbc
WHERE match('{query}*')
ORDER BY published_year ASC
LIMIT 150
"""

    def get(self):
        query = request.args.get('q', '').strip()

        # validate queries
        if query == '':
            raise WBCApiError('Query string is empty, "q" URL parameter is missing', 400)

        try:
            results, stats = self._get_results(query)
        except Exception as e:
            raise WBCApiError('Error while searching: {} {}'.format(e.__class__, str(e)))

        return jsonify({
            'query': query,
            'results': results,
            'stats': stats
        })

    def _get_results(self, query):
        """
        :type query str
        """
        sphinx = get_sphinx()

        query_escaped = sphinx.connection.escape_string(query)
        res = sphinx.query(self.QUERY.format(query=query_escaped).replace("\n", ' '))

        results = []

        for row in res:
            results.append({
                'id': int(row['id']),
                'name': row['chapter'],
                '_links': {
                    'self': {'href': url_for('documents', document_id=row['id'])}
                },
                # the issue where this document is in
                'issue': {
                    'id': int(row['document_id']),
                    'name': row['document_name'],
                    'published_year': int(row['published_year']),
                    '_links': {
                        'self': {'href': '/issues/{}'.format(row['document_id'])}  # TODO - app.get_url
                    },
                },
                # the publication where this issue is in
                'publication': {
                    'id': int(row['publication_id']),
                    '_links': {
                        'self': {'href': '/publications/{}'.format(row['publication_id'])}  # TODO - app.get_url
                    },
                },
                # the document details
                'snippet': row['snippet'],
            })

        meta = sphinx.get_meta()
        stats = {
            'total': int(meta['total']),
            'took': float(meta['time']),
            'powered_by': sphinx.get_sphinx_version(),
        }

        return results, stats
