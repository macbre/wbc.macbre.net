from os import environ

from . import app, is_debug
from .common import get_app_version

# emit git hash and register a helper function for templates
app.logger.info('{} is now running using code {}'.format(app.name, get_app_version()))
app.jinja_env.globals.update(get_app_version=get_app_version)

app.run(
    debug=is_debug,
    host='0.0.0.0',
    port=environ.get('SERVER_PORT', 8080)
)
