import logging


class WBCError(Exception):
    def __init__(self, message, resp_code=500):
        self._message = message
        self._resp_code = resp_code

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.error('HTTP {} - {}'.format(self._resp_code, self._message), exc_info=True)

    def get_message(self):
        return self._message

    def get_response_code(self):
        return self._resp_code


class WBCApiError(WBCError):
    pass


class WBCHtmlError(WBCError):
    pass
