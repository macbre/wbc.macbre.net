from flask import jsonify, request
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.sphinx import get_sphinx


class Search(MethodView):
    QUERY = """
SELECT
    id,
    SNIPPET(title, '{query}', 'limit=75') as name,
    chapter,
    SNIPPET(content, '{query}', 'limit=500') as snippet,
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
                'id': int(row['document_id']),
                'publication': row['name'],
                'chapter': row['chapter'],
                'snippet': row['snippet'],
                'published_year': int(row['published_year']),
            })

        meta = sphinx.get_meta()
        stats = {
            'total': int(meta['total']),
            'took': float(meta['time']),
            'powered_by': sphinx.get_sphinx_version(),
        }

        return results, stats
