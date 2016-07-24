import logging
from os import environ

from . import app

is_debug = environ.get('DEBUG')
logging.basicConfig(level=logging.DEBUG if is_debug else logging.WARN)

app.run(
    debug=is_debug,
    port=environ.get('SERVER_PORT', 8080)
)
