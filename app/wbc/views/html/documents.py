# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
from flask.views import MethodView

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
            'content': document.get_html_content(),
            'djvu_url': document.get_djvu_url(),
            'full_url': document.get_full_url(),
            'txt_url': document.get_txt_url(),
            'json_url': document.get_json_url(),
        }

        return render_template('document.html', **kwargs)
