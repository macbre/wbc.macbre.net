# -*- coding: utf-8 -*-
import re
import unicodedata

try:
    from html import escape  # Python 3.x
except ImportError:
    from cgi import escape  # Python 2.7

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
        :rtype: DocumentModel
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

    def get_txt_url(self):
        """
        :rtype: str
        """
        return url_for('documents.txt', document_id=self['id'])

    def get_json_url(self):
        """
        :rtype: str
        """
        return url_for('documents', document_id=self['id'])

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

            # be safe
            line = escape(line)

            parts.append(line)

        # return HTML-formatted content
        return '<p>{}</p>'.format('</p>\n\n<p>'.join(parts))

    def get_cite(self):
        """
        :rtype: str
        """
        # extract issue no
        # Kronika Miasta Poznania 2009 Nr2; Okupacja 1
        # ... Poznania 1960.01/06 R.28 Nr1/2
        m = re.search(r'\sNr([\d/]+)', self['issue_name'])
        issue_no = m.group(1).replace('/', '-') if m else None

        return u'{{{{KMP|{issue_no}/{year}|rozdział={chapter}}}}}'.\
            format(issue_no=issue_no, year=self['published_year'], chapter=self['chapter'].lower())
