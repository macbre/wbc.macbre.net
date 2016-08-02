from os import environ

from . import app
from . import is_debug


app.run(
    debug=is_debug,
    host='0.0.0.0',
    port=environ.get('SERVER_PORT', 8080)
)
