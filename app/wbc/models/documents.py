import re
import unicodedata

from flask import url_for
from . import Model

from wbc.connectors import get_sphinx


def remove_accents(input_str):
    """
    :type input_str str
    :rtype: str
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')


class DocumentModel(Model):
    @classmethod
    def new_from_id(cls, document_id):
        """
        :type document_id int
        :rtype: Document
        """
        res = get_sphinx().query(
                'SELECT id, title AS issue_name, document_id AS issue_id, published_year, chapter, content ' +
                'FROM wbc WHERE id = {}'.
                format(int(document_id))
        )

        if len(res) != 1:
            return None

        return cls(**res[0])

    def get_full_url(self):
        """
        :rtype: str
        """
        name = self['chapter'].lower()

        name = remove_accents(name)
        name = re.sub(r'[^a-z0-9]+', '-', name).strip('-')

        return url_for('documents.html', document_id=self['id'], name=name)

    def get_djvu_url(self):
        """
        :rtype: str
        """
        return 'http://www.wbc.poznan.pl/dlibra/doccontent?id={}'.format(self['issue_id'])

    def get_html_content(self):
        """
        :rtype: str
        """
        title = self['chapter']
        content = self['content']

        # remove repeated title in the content
        if content.startswith(title):
            content = content[len(title):]

        parts = []

        for line in content.split('\n'):
            line = line.strip()

            if line == '':
                continue

            parts.append(line)

        # return HTML-formatted content
        return '<p>{}</p>'.format('</p>\n\n<p>'.join(parts))
