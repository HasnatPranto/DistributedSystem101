FROM python:3.9-slim-buster

RUN mkdir /communication_service
WORKDIR /communication_service

ADD requirements.txt /communication_service/requirements.txt
RUN pip install -r /communication_service/requirements.txt

ADD . /communication_service

CMD ["python","/communication_service/commService.py"]