from flask import jsonify
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.views.api.search import SearchableMixin

from wbc.connectors import get_sphinx
from wbc.models import DocumentModel


class PublicationSuggest(SearchableMixin):
    # @see https://github.com/macbre/wbc.macbre.net/issues/26
    # @see http://sphinxsearch.com/docs/current/sphinxql-select.html
    # SELECT * FROM test WHERE MATCH('@title hello @body world')
    QUERY = """
SELECT
    id,
    title as document_name,
    chapter,
    publication_id,
    document_id AS issue_id
FROM wbc
WHERE match('@chapter {query}*'){where}
ORDER BY published_year ASC
LIMIT 10
    """

    def __init__(self, query):
        super(PublicationSuggest, self).__init__()
        self._query = query

    def search(self, issue_id=None):
        """
        Perform a search and format the results

        :type issue_id int
        """
        try:
            results, _ = self._get_results(self._query)
        except Exception as e:
            raise WBCApiError('Error while searching: {} {}'.format(e.__class__, str(e)))

        return results

    def _format_results(self, res):
        results = []

        for row in res:
            # self._logger.info(row)
            doc = DocumentModel(**row)
            results.append({
                'id': row['id'],
                'name': row['chapter'],
                'info': row['document_name'],
                'url': doc.get_full_url(),
            })

        return results


class Suggest(MethodView, SearchableMixin):

    @staticmethod
    def suggest_keyword(query):
        """
        :type query str
        :rtype: list[str]
        """
        # http://sphinxsearch.com/blog/2016/10/03/2-3-2-feature-built-in-suggests/
        try:
            return get_sphinx().call_suggest(
                query=query,
                index=SearchableMixin.INDEX,
                limit=20,
                max_edits=15,
                delta_len=8,
            )
        except Exception as e:
            raise WBCApiError('Error while getting keyword suggestions: {} {}'.format(e.__class__, str(e)))

    @staticmethod
    def suggest_publication(query):
        """
        :type query str
        :rtype: list[str]
        """
        try:
            return PublicationSuggest(query).search()
        except Exception as e:
            raise WBCApiError('Error while getting publication suggestions: {} {}'.format(e.__class__, str(e)))

    def get(self):
        # validate queries
        if not self.is_searchable():
            raise WBCApiError('Query string is empty, "q" URL parameter is missing', 400)

        query = self._get_search_query()

        suggestions = self.suggest_keyword(query)
        publications = self.suggest_publication(query)

        return jsonify([
            query,
            suggestions,
            publications
        ])
