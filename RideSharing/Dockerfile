FROM python:3.9-slim-buster

RUN mkdir /ride_service
WORKDIR /ride_service

ADD requirements.txt /ride_service/requirements.txt
RUN pip install -r /ride_service/requirements.txt

ADD . /ride_service

EXPOSE 6060

CMD ["python","/ride_service/rideService.py"]