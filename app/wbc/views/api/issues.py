from flask import jsonify, url_for
from flask.views import MethodView

from wbc.exceptions import WBCApiError
from wbc.models import IssuesModel


class Issue(MethodView):
    @staticmethod
    def get(issue_id):
        """
        :type issue_id int
        """
        try:
            documents = IssuesModel.get_documents(issue_id)
        except Exception as e:
            raise WBCApiError('Internal error: ' + str(e), 500)

        # handle missing documents
        if documents is None:
            raise WBCApiError('Issue not found', 404)

        issue = documents[0]

        return jsonify({
            'issue': {
                'id': int(issue['issue_id']),
                'name': issue['issue_name'],
                'published_year': int(issue['published_year']),
            },
            'publication': {
                'id': int(issue['publication_id']),
                '_links': {
                    'self': {'href': '/publications/{}'.format(issue['publication_id'])}  # TODO - app.get_url
                },
            },
            'documents': [
                {
                    'id': int(document['id']),
                    'name': document['chapter'],
                    '_links': {
                        'self': {'href': url_for('documents', document_id=document['id'])}
                    },
                }
                for document in documents
            ]
        })
