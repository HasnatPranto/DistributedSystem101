import json
import flask
import mysql.connector
from flask import Flask, request, Response
from flask_socketio import SocketIO

app = Flask(__name__)
socket = SocketIO(app)

@app.route('/rating', methods=['POST'])
def rating():
    print('Rating Server Ok')
    connection = mysql.connector.connect(user='root', password='',host='127.0.0.1', database='mysql')
    data = request.json
    cursor = connection.cursor()
    query = "INSERT INTO Driver_rating (id,rider_id,rider_name,driver_id,driver_name,rating) VALUES (%s,%s,%s,%s,%s,%s)"
    qdata = (None,data['r_id'],data['rider_name'],data['d_id'],data['driver_name'],data['rating'])

    try:
        cursor.execute(query, qdata)
        connection.commit()
        print("success")
        return flask.Response(status=201)

    except:
        print("lost")
        return flask.Response(status=400)

if __name__ == '__main__':
    app.run(port= 8015)