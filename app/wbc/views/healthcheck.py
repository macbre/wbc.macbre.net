from flask import jsonify
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.sphinx import get_sphinx


class Healthcheck(MethodView):
    def get(self):
        try:
            self._check_sphinx()
        except Exception as e:
            raise WBCApiError(str(e), 500)

        return jsonify({'ok': True})

    @staticmethod
    def _check_sphinx():
        # check Sphinx connection
        sphinx = get_sphinx()
        sphinx.get_indices()
