from flask import jsonify, request
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.sphinx import get_sphinx


class Search(MethodView):
    def get(self):
        query = request.args.get('q', '').strip()

        # validate queries
        if query == '':
            raise WBCApiError('Query string is empty, "q" URL parameter is missing', 400)

        return jsonify({
            'query': query,
            'results': []
        })
