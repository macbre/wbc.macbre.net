import logging
import os

from flask import Flask, jsonify, request, send_from_directory

from wbc.exceptions import WBCApiError

from wbc.views.healthcheck import Healthcheck
from wbc.views.api import Document, Issue, Search

app = Flask(import_name=__name__)

# healthcheck
app.add_url_rule('/healthcheck', view_func=Healthcheck.as_view('healthcheck'))

# API
app.add_url_rule('/api/v1/documents/<int:document_id>', view_func=Document.as_view('documents'))
app.add_url_rule('/api/v1/documents/<int:document_id>.txt', view_func=Document.as_view('documents.txt'))
app.add_url_rule('/api/v1/issues/<int:issue_id>', view_func=Issue.as_view('issues'))
app.add_url_rule('/api/v1/search', view_func=Search.as_view('search'))


# favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


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
    # API requests - return error messages as JSON
    if request.path.startswith('/api'):
        return handle_bad_api_request(WBCApiError('API end-point not found', 404))
    # emit HTML
    else:
        return '<strong>HTTP 404</strong> not found', 404


# setup logging
is_debug = os.environ.get('DEBUG')
logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO)
