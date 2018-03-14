FROM python:2 

WORKDIR /sensor-module/test/

ADD /shared ./shared
COPY /shared ./shared
ADD /sensorapp ./sensorapp

RUN pip install requests
CMD python sensorapp/start.py