from flask import render_template
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.models import DocumentModel


class DocumentHTML(MethodView):
    @staticmethod
    def get(document_id, name=None):
        """
        :type document_id int
        :type name str
        """
        try:
            document = DocumentModel.new_from_id(document_id)
        except Exception as e:
            raise WBCApiError('Internal error: ' + str(e), 500)

        # handle missing documents
        if document is None:
            raise WBCApiError('Document not found', 404)

        kwargs = {
            'issue_name': document['issue_name'],
            'title': document['chapter'],
            'content': document.get_html_content(),
        }

        return render_template('document.html', **kwargs)
