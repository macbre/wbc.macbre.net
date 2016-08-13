import unittest

from wbc.views.api.search import SearchableMixin
from wbc import app


class SearchableMixinTest(unittest.TestCase):

    def setUp(self):
        self.mixin = SearchableMixin()

    def test_is_searchable(self):
        with app.test_request_context():
            assert self.mixin.is_searchable() is False

        with app.test_request_context('/search'):
            assert self.mixin.is_searchable() is False

        with app.test_request_context('/search?q='):
            assert self.mixin.is_searchable() is False

        with app.test_request_context('/search?q=foo'):
            assert self.mixin.is_searchable() is True
