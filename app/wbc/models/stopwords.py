import re
import logging
import time

from io import StringIO

from wbc.connectors import get_redis


class StopWords(object):
    SET_NAME = 'stopwords'

    LINE_REGEXP = re.compile(r'^(\w+) (\d+)$')  # line needs to end with a number

    WORD_MIN_LENGTH = 3
    WORD_MIN_FREQ = 2

    WORDS_IN_BATCH = 50

    _redis = None

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def redis(self):
        """
        Lazy connect to Redis
        """
        if self._redis is None:
            self._redis = get_redis()

        return self._redis

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

        self.redis.delete(self.SET_NAME)

        for batch in self._words(stream):
            self._index_batch(batch)
            count += len(batch)

        self.logger.info('Indexed {} stopwords in {:.2f} sec'.format(count, time.time() - then))

    def _index_batch(self, batch):
        """
        :type batch list
        """
        # @see http://redis.io/commands/ZADD
        args = []

        # As *args, in the form of: score1, name1, score2, name2, ...
        for (word, _) in batch:
            args.append(0)
            args.append(word)

        self.redis.zadd(self.SET_NAME, *args)

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

            if not self.is_valid_word(word, freq):
                continue

            batch.append((word, freq))

            # emit words in batches
            if len(batch) == self.WORDS_IN_BATCH:
                yield(batch)
                batch = []

        # not emitted batch left
        if len(batch) > 0:
            yield(batch)

    def is_valid_word(self, word, freq):
        """
        :type word str
        :type freq int
        :rtype: bool
        """
        # skip too short words and not frequent enough
        if len(word) < self.WORD_MIN_LENGTH or freq < self.WORD_MIN_FREQ:
            return False

        # skip words like "1957"
        if word.isnumeric():
            return False

        # skip words like "problemowo-dydaktycznej"
        if '-' in word:
            return False

        return True
