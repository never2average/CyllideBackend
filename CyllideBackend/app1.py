from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, request
from keys import secretKey
import os
import json
import time
#from flask_socketio import SocketIO, emit
from flask_sockets import Sockets


def nextNum():
    y=0
    while True:
        y+=1
        yield y
        continue


a=nextNum()

app = Flask(__name__)
api = Api(app)
app.config['SECRET'] = os.urandom(24)
socket = Sockets(app)

@socket.route('/greetings')
def echo_socket(ws):
    # print("Inside echo_socket()")
    #message=None
    # while not ws.closed:
    message = ws.receive()
    ws.send("question No."+str(message))
    # while True:
    #     ws.emit('statusmessage')
    #     time.sleep(4)
        # message=ws.receive()
        # if(message!=None):
        #     print(message)
        #     if(message =="a"):
        #         ws.send("Correct!")
        #     else:
        #         ws.send("Wrong!")
        #     message =None
        #     break
        # ws.send("colsed")
    # print("outside echo_socket()")

@app.route('/')
def hello():
    print("Inside hello()")
    return 'Hello World!'






class TestConnection(Resource):
    def get(self):
        return jsonify({
            "message": "APIS working"
            })

api.add_resource(TestConnection, "/testconn")


#socketio.on('connect',test_message())

if __name__ == "__main__":
    # app.run(port=5000, debug=True)
    # socket.run(app, port=8080)
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print("Created!")
    server.serve_forever()
    






#implement using socketio
# @socket.on('message')
# def test_message(message):
#     print("message aaya"+message)
#     socket.emit('message',message)

# @socket.on('connect quiz session')
# def test_message():
#     socket.emit("Quiz started")