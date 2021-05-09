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

    socket_dh = socketio.Client()
    socket_dh.connect('http://13.14.0.51:9090', namespaces=['/confirmation']) #.51 communication server for dhaka
    socket_bh = socketio.Client()
    socket_bh.connect('http://13.14.0.52:9090', namespaces=['/confirmation'])

    @socket_dh.event(namespace='/confirmation')
    def message(data):
        print(f"***Dhaka***\nDriver {data['driver']} is en route to pick up rider {data['rider']}, Ride fair:{data['fair']}")
        rating = random.randint(1, 5)
        print(f"{data['rider']} gave driver {data['driver']} a rating of {rating}/5!")
        rate_info = {
            "rider_name": data['rider'],
            "r_id": data['rider_id'],
            "driver_name": data['driver'],
            "d_id": data['driver_id'],
            "rating": rating
        }
        requests.post("http://bhola.server.com:80/myride/rating", json=rate_info)


    @socket_bh.event(namespace='/confirmation')
    def message(data):

        print(f"**Bhola**\nDriver {data['driver']} is en route to pick up rider {data['rider']}, Ride fair:{data['fair']}")
        rating = random.randint(1, 5)
        print(f"{data['rider']} gave driver {data['driver']} a rating of {rating}/5!")
        rate_info = {
            "rider_name": data['rider'],
            "r_id": data['rider_id'],
            "driver_name": data['driver'],
            "d_id": data['driver_id'],
            "rating": rating
        }
        requests.post("http://bhola.server.com:80/myride/rating", json=rate_info)


    while True:
        r = random.choice(riders)
        d = random.choice(drivers)

        if random.randint(1,10)>5:
            geotag = 13
        else:
            geotag = 14

        rider = {
            "name": r[0],
            "id": r[1],
            "coordinates": [my_location(),my_location()],
            "destination": [my_location(),my_location()],
            "location": geotag
        }
        driver = {
            "name": d[0],
            "id": d[1],
            "coordinates": [my_location(), my_location()],
            "car_number": random.choice(cars),
            "location": geotag
        }
        if geotag == 13:
            requests.post(f"http://dhaka.server.com:80/myride/api/rider", json=rider)
            print(rider['name'], "is looking for a ride(Dhaka)")
            requests.post(f"http://dhaka.server.com:80/myride/api/driver", json=driver)
            print(driver['name'], "is looking for a trip(Dhaka)")
        else:
            requests.post(f"http://bhola.server.com:80/myride/api/rider", json=rider)
            print(rider['name'], "is looking for a ride(Bhola)")
            requests.post(f"http://bhola.server.com:80/myride/api/driver", json=driver)
            print(driver['name'], "is looking for a trip(Bhola)")

        time.sleep(2)
