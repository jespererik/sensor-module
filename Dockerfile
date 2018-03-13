FROM python:2 

WORKDIR /sensor-module

ADD /shared ./shared
COPY /shared ./shared
ADD /sensorapp ./sensorapp

RUN cd sensorapp/Adafruit_Python_DHT && python setup.py install
RUN pip install requests
CMD python sensorapp/start.py
