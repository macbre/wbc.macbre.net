# -*- coding: utf-8 -*-
import unittest

from wbc import app
from wbc.models import DocumentModel

from ..helpers import get_sphinx_mock


class DocumentModelTest(unittest.TestCase):
    def setUp(self):
        chapter = u'POWSTANIE WIELKOPOLSKIE NA POCZTÓWKACH, PLAKATACH, DYPLOMACH I ULOTKACH (DO 1921 R.)'

        self.model = DocumentModel(**{
            'id': 6224,
            'issue_id': 123,
            'chapter': chapter,
            'content': chapter + 'foo\n\n\n\n<bar>'
        })

    def test_accessor(self):
        assert self.model['id'] == 6224
        assert self.model['chapter'] == \
            u'POWSTANIE WIELKOPOLSKIE NA POCZTÓWKACH, PLAKATACH, DYPLOMACH I ULOTKACH (DO 1921 R.)'

    def test_urls(self):
        with app.test_request_context():
            assert self.model.get_full_url() == \
                '/document/6224/powstanie-wielkopolskie-na-pocztowkach-plakatach-dyplomach-i-ulotkach-do-1921-r.html'

            assert self.model.get_djvu_url() == \
                'http://www.wbc.poznan.pl/dlibra/doccontent?id=123'

            assert self.model.get_json_url() == \
                '/api/v1/documents/6224'

            assert self.model.get_txt_url() == \
                '/api/v1/documents/6224.txt'

    def test_get_html_content(self):
        assert self.model.get_html_content() == \
                '<p>foo</p>\n\n<p>&lt;bar&gt;</p>'

    @staticmethod
    def test_new_from_id():
        with app.test_request_context():
            query = """
SELECT id, title AS issue_name, document_id AS issue_id, published_year, chapter, content FROM wbc WHERE id = 453
            """.strip()

            get_sphinx_mock(query, [{
                'id': 453,
                'issue_id': 123
            }])
            assert DocumentModel.new_from_id(453)['issue_id'] == 123

            get_sphinx_mock(query, [])
            assert DocumentModel.new_from_id(453) is None
