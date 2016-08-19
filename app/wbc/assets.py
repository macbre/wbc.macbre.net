"""
Define concatenated and minified assets

If you set ASSETS_DEBUG = True in your config,
Flask-Assets will output each source file individually instead of merging them.
"""
# @see http://exploreflask.com/en/latest/static.html
from flask_assets import Bundle, Environment

bundles = {

    'js': Bundle(
        'js/jquery.auto-complete.min.js',
        'js/wbc.js',
        'js/back-to-top.js',
        output='wbc.%(version)s.min.js',
        filters='jsmin'
    ),

    'css': Bundle(
        'css/normalize.css',
        'css/skeleton.css',
        'css/wbc.css',
        output='wbc.%(version)s.min.css',
        filters='cssmin'
    ),
}


def register_assets(app):
    """
    :type app flask.Flask
    """
    assets = Environment(app)
    assets.register(bundles)
