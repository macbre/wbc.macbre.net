import unittest

from wbc.models import StopWords


class StopWordsTest(unittest.TestCase):
    def setUp(self):
        self.stopwords = StopWords()

    def test_is_valid_word(self):
        cases = [
            ('foo', 12, True),
            ('foo', 1, False),
            ('123', 1, False),
            ('123', 12, False),
            ('problemowo-dydaktycznej', 12, False),
            ('102na', 12, True),
        ]

        for (word, freq, expected) in cases:
            assert self.stopwords.is_valid_word(word, freq) is expected, (word, freq)
