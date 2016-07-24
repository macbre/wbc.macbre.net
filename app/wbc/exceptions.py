class WBCError(Exception):
    def __init__(self, message, resp_code=500):
        self._message = message
        self._resp_code = resp_code

    def get_message(self):
        return self._message

    def get_response_code(self):
        return self._resp_code


class WBCApiError(WBCError):
    pass
