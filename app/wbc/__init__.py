import logging
import os
import time

from socket import gethostname

from flask import g, Flask, jsonify, request, send_from_directory

from wbc.exceptions import WBCApiError

from wbc.views.healthcheck import Healthcheck
from wbc.views.api import Document, Issue, Search, Suggest
from wbc.views.html import DocumentHTML

app = Flask(import_name=__name__)

# healthcheck
app.add_url_rule('/healthcheck', view_func=Healthcheck.as_view('healthcheck'))

# API
app.add_url_rule('/api/v1/documents/<int:document_id>', view_func=Document.as_view('documents'))
app.add_url_rule('/api/v1/documents/<int:document_id>.txt', view_func=Document.as_view('documents.txt'))
app.add_url_rule('/api/v1/issues/<int:issue_id>', view_func=Issue.as_view('issues'))
app.add_url_rule('/api/v1/search', view_func=Search.as_view('search'))
app.add_url_rule('/api/v1/suggest', view_func=Suggest.as_view('suggest'))

# HTML
app.add_url_rule('/document/<int:document_id>.html', view_func=DocumentHTML.as_view('documents-short.html'))
app.add_url_rule('/document/<int:document_id>/<string:name>.html', view_func=DocumentHTML.as_view('documents.html'))


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


# measure response time
@app.before_request
def app_before_request():
    g.start = time.time()


@app.after_request
def app_after_request(response):
    """
    :type response flask.wrappers.ResponseBase
    :rtype: flask.wrappers.ResponseBase
    """
    response.headers.set('X-Backend-Response-Time', '{:.4f}'.format(time.time() - g.start))
    response.headers.set('X-Served-By', gethostname())

    return response

# setup logging
is_debug = os.environ.get('DEBUG')
logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO)
