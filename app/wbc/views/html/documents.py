# -*- coding: utf-8 -*-
from math import ceil

from flask import render_template, redirect, make_response, request
from flask.views import MethodView

from wbc.common import get_app_version
from wbc.exceptions import WBCHtmlError
from wbc.models import DocumentModel


class DocumentHTML(MethodView):
    @staticmethod
    def get(document_id, name=None):
        """
        :type document_id int
        :type name str
        """
        try:
            document = DocumentModel.new_from_id(document_id)
        except Exception as e:
            raise WBCHtmlError(u'Wystąpił błąd wewnętrzny: ' + str(e), 500)

        # handle missing documents
        if document is None:
            raise WBCHtmlError(u'Podany dokument nie został znaleziony', 404)

        # redirect to a canonical URL
        if name is None:
            return redirect(document.get_full_url(), code=301)  # 301 Moved Permanently

        kwargs = {
            'issue_name': document['issue_name'],
            'title': document['chapter'],
            'published_year': document['published_year'],
            'read_time': ceil(document.get_read_time() / 60),  # minutes
            'intro': document.get_intro(),
            'content': document.get_html_content(),
            'cite': document.get_cite(),
            'djvu_url': document.get_djvu_url(),
            'full_url': document.get_full_url(),
            'txt_url': document.get_txt_url(),
            'json_url': document.get_json_url(),
        }

        resp = make_response(render_template('document.html', **kwargs))

        resp.set_etag('{}-{}-{}'.format(document_id, document['published_year'], get_app_version()), weak=True)
        resp.headers['Cache-Control'] = 'public, max-age=0'

        resp.make_conditional(request)
        return resp
