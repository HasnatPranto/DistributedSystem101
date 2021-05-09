import json
import math
import flask
import requests
import socketio
from flask import Flask, request, Response
from flask_socketio import SocketIO, emit
from flask_apscheduler import APScheduler

avail_riders = []
avail_drivers = []
app = Flask(__name__)
socket = SocketIO(app)
scheduler = APScheduler()
scheduler.init_app(app)

def make_pair():

    def calculate_distance(rider, driver):
        rider_x, rider_y = [int(i) for i in rider['coordinates']]
        driver_x, driver_y = [int(i) for i in driver['coordinates']]
        return math.sqrt(pow(rider_x - driver_x, 2) + pow(rider_y - driver_y, 2))

    #print(avail_riders)
    for rider in avail_riders:
        distance_min = 10000000000000
        nearest_driver = None
        for driver in avail_drivers:
            distance = calculate_distance(rider, driver)
            if distance_min > distance:
                distance_min = distance
                nearest_driver = driver

        avail_riders.remove(rider)
        avail_drivers.remove(nearest_driver)

        data = {
            "rider": rider['name'],
            "rider_id": rider['id'],
            "driver": nearest_driver['name'],
            "driver_id": nearest_driver['id'],
            "fair": round(distance_min*2, 0)
        }
        #print(data)
        if rider['location'] == 13:
            requests.post("http://communication-service-dhaka:9090/comm", json=data)
        else:
            requests.post("http://communication-service-bhola:9090/comm", json=data)

@app.route('/ride/docker', methods=['GET'])
def checkStatus():
    return {
        'Status':"Fine"
    }

@app.route('/myride/api/rider', methods=['POST'])
def add_rider():
    data = request.json
    avail_riders.append(data)
    return flask.Response(status = 201)


@app.route('/myride/api/driver', methods=['POST'])
def add_driver():
    data = request.json
    avail_drivers.append(data)
    return flask.Response(status=201)

if __name__ == '__main__':
    scheduler.add_job(id='task', func= make_pair, trigger='interval', seconds=5)
    scheduler.start()
    app.run(host = '0.0.0.0', port= 6060)