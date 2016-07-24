from flask import Flask, jsonify, request

from wbc.exceptions import WBCApiError

from wbc.views.healthcheck import Healthcheck

from wbc.views.api.documents import Document
from wbc.views.api.search import Search

app = Flask(import_name=__name__)

# healthcheck
app.add_url_rule('/healthcheck', view_func=Healthcheck.as_view('healthcheck'))

# API
app.add_url_rule('/api/v1/documents/<int:document_id>', view_func=Document.as_view('documents'))
app.add_url_rule('/api/v1/documents/<int:document_id>.txt', view_func=Document.as_view('documents.txt'))
app.add_url_rule('/api/v1/search', view_func=Search.as_view('search'))


# errors handling
@app.errorhandler(WBCApiError)
def handle_bad_api_request(e):
    """
    :type e WBCApiError
    """
    return jsonify(
            error=True,
            details=e.get_message()
    ), e.get_response_code()


@app.errorhandler(404)
def handle_not_found(e):
    if request.path.startswith('/api'):
        return handle_bad_api_request(WBCApiError('API end-point not found', 404))
