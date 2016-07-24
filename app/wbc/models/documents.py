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
                'SELECT title, document_id AS issue_id, chapter, content FROM wbc WHERE id = {}'.
                format(int(document_id))
        )

        if len(res) != 1:
            return None

        return cls(**res[0])
