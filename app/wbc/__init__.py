from flask import Flask

from wbc.healthcheck import Healthcheck

app = Flask(import_name=__name__)

# add routes
app.add_url_rule('/healthcheck', view_func=Healthcheck.as_view('healthcheck'))
