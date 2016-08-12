from os import environ

from . import app, is_debug
from .assets import register_assets
from .common import get_app_version

# emit git hash and register a helper function for templates
app.logger.info('{} is now running using code {}'.format(app.name, get_app_version()))
app.jinja_env.globals.update(get_app_version=get_app_version)

register_assets(app)

app.run(
    debug=is_debug,
    host='0.0.0.0',
    port=environ.get('SERVER_PORT', 8080)
)
