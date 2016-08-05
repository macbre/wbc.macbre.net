import unittest

from wbc import app
from wbc.models import DocumentModel


class DocumentModelTest(unittest.TestCase):
    def setUp(self):
        self.model = DocumentModel(**{
            'id': 6224,
            'chapter': 'POWSTANIE WIELKOPOLSKIE NA POCZTÓWKACH, PLAKATACH, DYPLOMACH I ULOTKACH (DO 1921 R.)',
            'content': 'foo\n\n\n\nbar'
        })

    def test_accessor(self):
        assert self.model['id'] == 6224
        assert self.model['chapter'] == \
            'POWSTANIE WIELKOPOLSKIE NA POCZTÓWKACH, PLAKATACH, DYPLOMACH I ULOTKACH (DO 1921 R.)'

    def test_get_full_url(self):
        with app.test_request_context():
            assert self.model.get_full_url() == \
                '/document/6224/powstanie-wielkopolskie-na-pocztowkach-plakatach-dyplomach-i-ulotkach-do-1921-r.html'

    def test_get_html_content(self):
        assert self.model.get_html_content() == \
                '<p>foo</p>\n\n<p>bar</p>'
