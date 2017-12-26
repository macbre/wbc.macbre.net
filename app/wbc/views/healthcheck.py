import sys

from flask import jsonify
from flask.views import MethodView

from wbc.common import get_app_version
from wbc.exceptions import WBCApiError
from wbc.connectors import get_sphinx


class Healthcheck(MethodView):
    def get(self):
        try:
            self._check_sphinx()
        except Exception as e:
            raise WBCApiError(str(e), 500)

        return jsonify({
            'ok': True,
            'git': get_app_version(),
            'sphinx': get_sphinx().get_sphinx_version(),
            'python': sys.version
        })

    @staticmethod
    def _check_sphinx():
        # check Sphinx connection
        sphinx = get_sphinx()
        sphinx.get_indices()
