import logging
import os
import time

from socket import gethostname

from flask import g, Flask, jsonify, request, send_from_directory, render_template
from werkzeug.contrib.fixers import ProxyFix

from wbc.exceptions import WBCApiError, WBCHtmlError

from wbc.views.healthcheck import Healthcheck
from wbc.views.api import Document, Issue, Search, Suggest
from wbc.views.html import DocumentHTML, HomeHTML, SearchHTML

from .assets import register_assets
from .common import get_app_version

app = Flask(import_name=__name__)

# config
# @see http://stackoverflow.com/a/37331139/5446110
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 365 * 86400  # a year

# healthcheck
app.add_url_rule('/healthcheck', view_func=Healthcheck.as_view('healthcheck'))

# API
app.add_url_rule('/api/v1/documents/<int:document_id>', view_func=Document.as_view('documents'))
app.add_url_rule('/api/v1/documents/<int:document_id>.txt', view_func=Document.as_view('documents.txt'))
app.add_url_rule('/api/v1/issues/<int:issue_id>', view_func=Issue.as_view('issues'))
app.add_url_rule('/api/v1/search', view_func=Search.as_view('search'))
app.add_url_rule('/api/v1/suggest', view_func=Suggest.as_view('suggest'))

# HTML
app.add_url_rule('/', view_func=HomeHTML.as_view('home.html'))

app.add_url_rule('/document/<int:document_id>.html', view_func=DocumentHTML.as_view('documents-short.html'))
app.add_url_rule('/document/<int:document_id>/<string:name>.html', view_func=DocumentHTML.as_view('documents.html'))

app.add_url_rule('/search', view_func=SearchHTML.as_view('search.html'))


# favicon
root_path = app.root_path


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(root_path, 'static'),
                               filename='img/favicon.ico', mimetype='image/vnd.microsoft.icon')


# robots.txt and sitemaps
@app.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(root_path, 'static'),
                               filename='robots.txt', mimetype='text/plain', cache_timeout=86400)


# @see http://flask.pocoo.org/snippets/57/
@app.route('/sitemap.xml', defaults={'sitemap_id': 'index'})
@app.route('/sitemap-<string:sitemap_id>.xml')
def sitemap(sitemap_id):
    """
    :type sitemap_id str
    :rtype: flask.wrappers.ResponseBase
    """
    return send_from_directory(os.path.join(root_path, 'sitemap'),
                               filename='sitemap-{}.xml'.format(sitemap_id),
                               mimetype='text/xml', cache_timeout=86400, add_etags=False)


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


# errors handling
@app.errorhandler(WBCHtmlError)
def handle_bad_html_request(e):
    """
    :type e WBCHtmlError
    """
    return render_template('error.html', message=e.get_message(), code=e.get_response_code()), e.get_response_code()


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


hostname = gethostname()  # cache to avoid uname syscall on each request


@app.after_request
def app_after_request(response):
    """
    :type response flask.wrappers.ResponseBase
    :rtype: flask.wrappers.ResponseBase
    """
    response.headers.set('X-Backend-Response-Time', '{:.4f}'.format(time.time() - g.start))
    response.headers.set('X-Served-By', hostname)

    return response

# setup logging
is_debug = os.environ.get('DEBUG')
logging.basicConfig(
    level=logging.DEBUG if is_debug else logging.INFO,
    format='%(asctime)s %(name)-25s %(levelname)-8s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

# emit git hash and register a helper function for templates
app.logger.info('{} is now running using code {}'.format(app.name, get_app_version()))
app.jinja_env.globals.update(get_app_version=get_app_version)

# register assets
register_assets(app)

# ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
