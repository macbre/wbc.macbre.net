from os import environ

from . import app, is_debug


def start():
    app.run(
        debug=is_debug,
        host='0.0.0.0',
        port=environ.get('SERVER_PORT', 8080)
    )
