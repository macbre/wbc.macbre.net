from . import Model, DocumentModel

from wbc.sphinx import get_sphinx


class IssuesModel(Model):
    @staticmethod
    def get_documents(issue_id):
        """
        :type issue_id int
        :rtype: DocumentModel[]
        """
        res = get_sphinx().query(
                'SELECT id, title AS issue_name, document_id AS issue_id, published_year, publication_id, chapter ' +
                'FROM wbc WHERE issue_id = {}'.
                format(int(issue_id))
        )

        if len(res) == 0:
            return None

        return [DocumentModel(**row) for row in res]

    def to_json(self):
        raise NotImplementedError()
