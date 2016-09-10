# -*- coding: utf-8 -*-
from flask import render_template
from flask.views import MethodView

from wbc.connectors import get_sphinx


class HomeHTML(MethodView):
    def get(self):
        return render_template('home.html', stats=self._get_stats())

    @staticmethod
    def _get_stats():
        """
        :rtype: object
        """
        sphinx = get_sphinx()
        stats = sphinx.get_index_meta(index_name='wbc')

        return {
            'documents': int(stats['indexed_documents']),
            'mbytes': int(int(stats['indexed_bytes']) / 1024 / 1024),
        }
