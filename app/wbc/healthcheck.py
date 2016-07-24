from flask import jsonify
from flask.views import MethodView

from .sphinx import get_sphinx


class Healthcheck(MethodView):
    def get(self):
        try:
            self._check_sphinx()
        except Exception as e:
            return jsonify({'error': True, 'exception': str(e)}), 500

        return jsonify({'ok': True})

    @staticmethod
    def _check_sphinx():
        # check Sphinx connection
        sphinx = get_sphinx()
        sphinx.get_indices()
