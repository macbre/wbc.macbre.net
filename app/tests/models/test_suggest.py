# -*- coding: utf-8 -*-
import unittest

from wbc.views.api.suggest import Suggest


class SuggestTest(unittest.TestCase):
    @staticmethod
    def test_trim_query():
        assert Suggest.trim_query('') == ''
        assert Suggest.trim_query('s') == 's'
        assert Suggest.trim_query('sp') == 'sp'
        assert Suggest.trim_query('spr') == 'spr'

        assert Suggest.trim_query('sprawa') == 'sprawa'
        assert Suggest.trim_query('sprawa ') == 'sprawa'
        assert Suggest.trim_query('sprawa p') == 'sprawa'
        assert Suggest.trim_query('sprawa pa') == 'sprawa'

        assert Suggest.trim_query('sprawa pau') == 'sprawa pau'

        assert Suggest.trim_query('sprawa paula von hi') == 'sprawa paula von'
