from flask import jsonify, request, make_response
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.models import DocumentModel


class Document(MethodView):
    @staticmethod
    def get(document_id):
        """
        :type document_id int
        """
        try:
            document = DocumentModel.new_from_id(document_id)
        except Exception as e:
            raise WBCApiError('Internal error: ' + str(e), 500)

        # handle missing documents
        if document is None:
            raise WBCApiError('Document not found', 404)

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
