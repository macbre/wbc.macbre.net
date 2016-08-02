from sys import stdin

from wbc import app
from wbc.models import StopWords


def build():
    with app.app_context():
        StopWords().index(stdin)
