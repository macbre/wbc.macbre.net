from flask import jsonify
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.models import StopWords
from wbc.views.api.search import SearchableMixin


class Suggest(MethodView, SearchableMixin):
    def get(self):
        # validate queries
        if not self.is_searchable():
            raise WBCApiError('Query string is empty, "q" URL parameter is missing', 400)

        query = self._get_search_query()

        try:
            suggestions = StopWords().suggest(query)
        except Exception as e:
            raise WBCApiError('Error while getting suggestions: {} {}'.format(e.__class__, str(e)))

        return jsonify([
            query,
            suggestions
        ])
