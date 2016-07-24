from flask import jsonify
from flask.views import MethodView


class Healthcheck(MethodView):

    @staticmethod
    def get():
        return jsonify({'ok': True})
