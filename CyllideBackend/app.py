from flask import Flask,jsonify,make_response,render_template,redirect,url_for,Markup
from flask_restful import Resource,Api,request
from yahoo_fin.stock_info import get_quote_table
from keys import secretKey
import json

app=Flask(__name__)
api=Api(app)

class TestConnection(Resource):

api.add_resource()



if __name__=="__main__":
    app.run(port=5000,debug=True)