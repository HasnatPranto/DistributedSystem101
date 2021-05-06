import socketio
from flask_socketio import SocketIO, emit
from flask import Flask, request
import socketio
app = Flask(__name__)
socket = SocketIO(app)


@socket.on('message')
def connectClient(data):
    socket.emit('message', data, namespace='/confirmation')

@app.route('/comm', methods=['POST'])
def send_best_pair():
    data= request.json
    print(data)
    connectClient(data)
    return 'message sent'

@app.route('/comm/docker', methods=['GET'])
def checkStatus():
    print('Ok')
    return 'Ok'


if __name__ == '__main__':
    socket.run(app, host= '0.0.0.0', port=9090)