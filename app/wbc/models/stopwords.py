import re
import logging
import time

from io import StringIO

from wbc.redis import get_redis


class StopWords(object):
    SET_NAME = 'stopwords'

    LINE_REGEXP = re.compile(r'^(\w+) (\d+)$')  # line needs to end with a number

    WORD_MIN_LENGTH = 3
    WORD_MIN_FREQ = 5

    WORDS_IN_BATCH = 50

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.redis = get_redis()

    def suggest(self, query, limit=20):
        """
        :type query str
        :type limit int
        :rtype: list
        """
        # @see http://redis.io/commands/zrangebylex
        r = self.redis.zrangebylex(
            name=self.SET_NAME,
            min='[{}'.format(query),
            max='[{}\xff'.format(query),
            start=0,
            num=limit
        )

        return [item.decode('utf-8') for item in r]

    def index(self, stream):
        """
        Index stopwords from given stream

        :type stream StringIO
        """
        count = 0
        then = time.time()
        self.logger.info('Indexing stopwords...')

        for batch in self._words(stream):
            self._index_batch(batch)
            count += len(batch)

        self.logger.info('Indexed {} stopwords in {:.2f} sec'.format(count, time.time() - then))

    def _index_batch(self, batch):
        # @see http://redis.io/commands/ZADD
        kwargs = {name: 0 for name, _ in batch}

        self.redis.zadd(name=self.SET_NAME, **kwargs)

    def _words(self, stream):
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
