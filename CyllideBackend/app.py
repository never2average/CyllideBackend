from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, request
from yahoo_fin.stock_info import get_quote_table
from keys import secretKey
import json


app = Flask(__name__)
api = Api(app)


class TestConnection(Resource):
    def get(self):
        return jsonify({
            "message": "APIS working"
            })

api.add_resource("/testconn", TestConnection)


if __name__ == "__main__":
    app.run(port=5000, debug=True)