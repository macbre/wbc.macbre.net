from . import Model

from wbc.sphinx import get_sphinx


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

    def to_json(self):
        return {
            'id': int(self['id']),
            'name': self['chapter'],
            'content': self['content'],
        }
