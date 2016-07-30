import logging
import re

from sys import stdin
from io import StringIO


class StopWords(object):
    LINE_REGEXP = re.compile(r'^(\w+) (\d+)$')  # line needs to end with a number

    WORD_MIN_LENGTH = 3
    WORD_MIN_FREQ = 5

    WORDS_IN_BATCH = 50

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def index(self, stream):
        """
        :type stream StringIO
        """
        count = 0
        self.logger.info('Indexing stopwords...')

        for batch in self.words(stream):
            # print(batch)
            count += len(batch)

        self.logger.info('Indexed {} stopwords'.format(count))

    def words(self, stream):
        """
        :type stream StringIO
        """
        batch = []

        for line in stream.readlines():
            matches = re.match(self.LINE_REGEXP, line)
            if matches is None:
                continue

            word = matches.group(1)
            freq = int(matches.group(2))

            # skip too short words and not frequent enough
            if len(word) < self.WORD_MIN_LENGTH or freq < self.WORD_MIN_FREQ:
                continue

            # skip words like "1957"
            if word.isnumeric():
                continue

            batch.append((word, freq))

            # emit words in batches
            if len(batch) == self.WORDS_IN_BATCH:
                yield(batch)
                batch = []

        # not emitted batch left
        if len(batch) > 0:
            yield(batch)


def build():
    StopWords().index(stdin)
