from flask import jsonify, request, make_response
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.sphinx import get_sphinx


class Document(MethodView):
    def get(self, document_id):
        """
        :type document_id int
        """
        document = self._get_document(document_id)

        # handle text format
        txt_requested = request.path.endswith('.txt')
        if txt_requested:
            resp = make_response(document['content'])
            resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
            return resp

        return jsonify({
            'id': int(document_id),
            'name': document['chapter'],
            'content': document['content'],
        })

    @staticmethod
    def _get_document(document_id):
        sphinx = get_sphinx()

        res = sphinx.query('SELECT title, chapter, content FROM wbc WHERE id = {}'.format(int(document_id)))

        if len(res) != 1:
            raise WBCApiError('Document not found', 404)

        return res[0]
