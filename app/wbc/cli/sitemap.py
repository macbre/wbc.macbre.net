from xml.sax.saxutils import XMLGenerator

from wbc import app
from wbc.common import LoggableMixin
from wbc.connectors import get_sphinx
from wbc.models import DocumentModel


class SitemapGenerator(LoggableMixin):

    # You can provide multiple Sitemap files, but each Sitemap file that you provide must have no more
    # than 50,000 URLs and must be no larger than 10MB (10,485,760 bytes)
    URLS_PER_SITEMAP = 2500

    XML_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

    def __init__(self, directory, http_path, index_name='sitemap-index.xml'):
        super(SitemapGenerator, self).__init__()

        self._directory = directory
        self._http_path = http_path
        self._index_name = index_name

        # file handlers to the sitemap index and the current sub-sitemap XML
        self._index_generator = None
        self._sitemap_generator = None

        # item counters
        self._items_total = 0
        self._items_current = 0

        # ID of the current sub-sitemap
        self._sitemap_id = 0

    def add_item(self, location, lastmod=None, change_freq='monthly', priority='1.0'):
        """
        :type location str
        :type lastmod str
        :type change_freq str
        :type priority str
        """
        # @see http://www.sitemaps.org/protocol.html#xmlTagDefinitions
        self._logger.debug('Adding <{}>'.format(location))

        # open an new sub-sitemap, if there's no active one
        if self._sitemap_generator is None:
            self._sitemap_generator = self._get_next_sitemap()
            self._items_current = 0

        # add an item
        self._items_current += 1
        self._items_total += 1

        self._sitemap_generator.ignorableWhitespace("\n\t")
        self._sitemap_generator.startElement('url', attrs={})

        # <location>
        self._sitemap_generator.startElement('loc', attrs={})
        self._sitemap_generator.characters(location)
        self._sitemap_generator.endElement('loc')

        # <lastmod>
        if lastmod is not None:
            self._sitemap_generator.startElement('lastmod', attrs={})
            self._sitemap_generator.characters(lastmod)
            self._sitemap_generator.endElement('lastmod')

        self._sitemap_generator.endElement('url')

        # check if the sub-sitemap is not too big
        if self._items_current == self.URLS_PER_SITEMAP:
            self._items_current = 0
            self._close_sitemap()
            self._sitemap_generator = None

    # these calls are made automatically when using SitemapGenerator with "with"
    def init(self):
        self._logger.info('Generating XML sitemap in {} for <{}>'.format(self._directory, self._http_path))
        self._index_init()

    def close(self):
        self._logger.info('Closing XML sitemap, {} URLs added in {} sub-sitemaps'.
                          format(self._items_total, self._sitemap_id))

        if self._sitemap_generator is not None:
            self._close_sitemap()

        self._index_end()

    # private API follows
    def _open_xml_generator(self, filename):
        """
        :type filename str
        :rtype: xml.sax.saxutils.XMLGenerator
        """
        self._logger.info('Opening new XML sub-sitemap: {}'.format(filename))

        out = open(self._directory + '/' + filename, 'wt')
        return XMLGenerator(out, encoding='utf-8')

    # sub-sitemap handling
    def _get_next_sitemap(self):
        """
        :rtype: xml.sax.saxutils.XMLGenerator
        """
        self._sitemap_id += 1

        filename = 'sitemap-{:03}.xml'.format(self._sitemap_id)
        generator = self._open_xml_generator(filename)

        # store a link to a new sitemap in the index
        self._index_generator.ignorableWhitespace("\n\t")
        self._index_generator.startElement('sitemap', attrs={})
        self._index_generator.startElement('loc', attrs={})
        self._index_generator.characters('{}/{}'.format(self._http_path, filename))
        self._index_generator.endElement('loc')
        self._index_generator.endElement('sitemap')

        generator.startDocument()
        generator.startElement('urlset', attrs={'xmlns': self.XML_NS})

        return generator

    def _close_sitemap(self):
        self._sitemap_generator.ignorableWhitespace("\n")
        self._sitemap_generator.endElement('urlset')
        self._sitemap_generator._flush()

    # sitemapindex handling
    def _index_init(self):
        self._index_generator = self._open_xml_generator(self._index_name)
        self._index_generator.startDocument()
        self._index_generator.startElement('sitemapindex', attrs={'xmlns': self.XML_NS})

    def _index_end(self):
        self._index_generator.ignorableWhitespace("\n<!-- URLs: {} -->\n".format(self._items_total))
        self._index_generator.endElement('sitemapindex')
        self._index_generator._flush()

    # for "with" block
    def __enter__(self):
        self.init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.close()
        else:
            self._logger.error('Something went wrong - {}: {}'.format(exc_type, exc_val))


def get_urls(server_name):
    """
    :rtype: list
    """
    app.config['SERVER_NAME'] = server_name

    with app.app_context():
        sphinx = get_sphinx()

        # fetch results in smaller batches
        offset = 0
        batch = 100

        while True:
            rows = sphinx.query('SELECT id, chapter, published_year FROM wbc WHERE id BETWEEN {} AND {} LIMIT {}'
                                .format(offset, offset + batch - 1, batch))

            # there's not more results - end
            if len(rows) == 0:
                break

            for row in rows:
                document = DocumentModel(**row)
                yield document.get_full_url(), str(document['published_year'])  # YYYY

            # query for a next batch
            offset += batch


def build():
    with SitemapGenerator(directory=app.root_path + '/sitemap', http_path='http://wbc.macbre.net') as sitemap:
        for url, lastmod in get_urls(server_name='wbc.macbre.net'):
            sitemap.add_item(url, lastmod)
