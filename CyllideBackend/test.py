from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource
from simplecrypt import encrypt, decrypt
from keys import data_encryption_key
import json

app = Flask(__name__)
api=Api(app)



class FK(Resource):
    def get(self):
        result = json.dumps({
            "name":"burjose"
        })
        result = encrypt(data_encryption_key,result.encode('utf-8'))
        return make_response(result,200)


api.add_resource(FK,"/fk")

if __name__=="__main__":
    app.run(debug=True)