# -*- coding: utf-8 -*-
import unittest

from wbc.models import DocumentModel


class DocumentCiteTest(unittest.TestCase):
    @staticmethod
    def test_cite():
        cases = {
            u'{{KMP|2/2009|rozdział=poznańskie budownictwo przeciwlotnicze w latach 30. i w czasie ii wojny światowej}}': {
                'chapter': u'POZNAŃSKIE BUDOWNICTWO PRZECIWLOTNICZE W LATACH 30. I W CZASIE II WOJNY ŚWIATOWEJ',
                'published_year': '2009',
                'issue_name': 'Kronika Miasta Poznania 2009 Nr2; Okupacja 1',
            },
            u'{{KMP|1-2/1960|rozdział=k}}': {
                'chapter': u'K',
                'published_year': '1960',
                'issue_name': u'Kronika Miasta Poznania: kwartalnik poświęcony problematyce współczesnego Poznania 1960.01/06 R.28 Nr1/2',
            },
            u'{{KMP|2-3/1933|rozdział=kronika miast a poznania}}': {
                'chapter': u'KRONIKA MIAST A POZNANIA',
                'published_year': '1933',
                'issue_name': u'Kronika Miasta Poznania: kwartalnik poświęcony sprawom kulturalnym stoł. m. Poznania: organ Towarzystwa Miłośników Miasta Poznania 1933 R.11 Nr2/3',
            },
        }

        for expected, data in cases.items():
            model = DocumentModel(**data)
            assert model.get_cite() == expected
