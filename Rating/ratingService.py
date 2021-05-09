import json
import flask
import mysql.connector
from flask import Flask, request, Response
from flask_socketio import SocketIO

app = Flask(__name__)
socket = SocketIO(app)

@app.route('/myride/rating', methods=['POST'])
def rating():
    #print('Rating Server Ok')
    connection = mysql.connector.connect(user='admin', password='admin123',host='13.14.0.100', database='DbDs', port=3306)
    data = request.json
    cursor = connection.cursor()
    query = "INSERT INTO Driver_rating (id,rider_id,rider_name,driver_id,driver_name,rating) VALUES (%s,%s,%s,%s,%s,%s)"
    qdata = (None,data['r_id'],data['rider_name'],data['d_id'],data['driver_name'],data['rating'])

    try:
        cursor.execute(query, qdata)
        connection.commit()
        #print("success")
        return flask.Response(status=201)

    except:
        #print("lost")
        return flask.Response(status=400)

#@app.route('/getRatings',methods=['GET'])
def getRatings():
    connection = mysql.connector.connect(user='admin', password='admin123', host='http://database', database='DbDs', port=1314)

    if(connection.is_connected()):
       print('Ok')
    else:
        print("not ok")


@app.route('/rating/docker', methods =['GET'])
def check():
    return {
        "status": 'Fine'
    }
if __name__ == '__main__':
    #getRatings()
    app.run(host='0.0.0.0', port=6060)