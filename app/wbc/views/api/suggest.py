from flask import jsonify
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.views.api.search import SearchableMixin

from wbc.connectors import get_sphinx


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
            raise WBCApiError('Error while getting suggestions: {} {}'.format(e.__class__, str(e)))

    def get(self):
        # validate queries
        if not self.is_searchable():
            raise WBCApiError('Query string is empty, "q" URL parameter is missing', 400)

        query = self._get_search_query()

        # 1. suggest keywords
        suggestions = self.suggest_keyword(query)

        # 2. suggest the publication

        return jsonify([
            query,
            suggestions
        ])
