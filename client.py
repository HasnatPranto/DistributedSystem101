import random
import time
from flask import Flask, request
import socketio
import requests

def my_location():
    loc = random.randint(-100,100)
    return loc

if __name__ == '__main__':

    riders = [['Azim',1],['Farooq',2],['Muntasir',3],['Rifat',4],['Joy',5],['Al-amin',6],['Kamrul',7],
              ['Kiran',8],['Bashir',9],['Maliha',10],['Mithila',11],['Sourav',12]]

    drivers = [['Jahid',1],['Minan',2],['Khalek',3],['Khalil',4],['Hasnat',5],['Mohsin',6],['Miraj',7],['Manju',8]]

    cars = ['DS-98379','DS-12344','DS-45129','DS-31179','DS-41370','DS-18479','LL-124379','DL-12566',8]

    socket = socketio.Client()
    socket.connect('http://127.0.0.1:8014', namespaces=['/confirmation'])

    @socket.event(namespace='/confirmation')
    def message(data):
        print(f"Driver {data['driver']} is en route to pick up rider {data['rider']}, Ride fair:{data['fair']}")
        rating = random.randint(1, 5)
        print(f"{data['rider']} gave driver {data['driver']} a rating of {rating}/5!")
        rate_info = {
            "rider_name": data['rider'],
            "r_id": data['rider_id'],
            "driver_name": data['driver'],
            "d_id": data['driver_id'],
            "rating": rating
        }
        requests.post("http://127.0.0.1:8000/rating", json=rate_info)


    while True:
        r = random.choice(riders)
        d = random.choice(drivers)
        rider = {
            "name": r[0],
            "id": r[1],
            "coordinates": [my_location(),my_location()],
            "destination": [my_location(),my_location()]
        }
        driver = {
            "name": d[0],
            "id": d[1],
            "coordinates": [my_location(), my_location()],
            "car_number": random.choice(cars)
        }

        requests.post("http://127.0.0.1:8000/rider", json= rider)
        print(rider['name'], "is looking for a ride")
        requests.post("http://127.0.0.1:8000/driver", json= driver)
        print(driver['name'], "is looking for a trip")
        time.sleep(4)
