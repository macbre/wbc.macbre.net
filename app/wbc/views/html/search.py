# -*- coding: utf-8 -*-
from flask import render_template
from flask.views import MethodView

from wbc.exceptions import WBCHtmlError
from wbc.views.api.search import SearchableMixin


class SearchHTML(MethodView, SearchableMixin):
    def get(self):
        # validate queries
        if not self.is_searchable():
            raise WBCHtmlError(u'Podaj temat wyszukiwania', 400)

        try:
            results, stats = self._get_results(self._get_search_query())
        except:
            raise WBCHtmlError(u'Wystąpil błąd w trakcie wyszukiwania', 500)

        return render_template('search.html', results=results, stats=stats, query=self._get_search_query())
