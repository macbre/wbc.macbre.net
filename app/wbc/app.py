from os import environ
from . import app

app.run(
    debug=environ.get('DEBUG'),
    port=environ.get('SERVER_PORT', 8080)
)
