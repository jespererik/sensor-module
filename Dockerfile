FROM python:2 

WORKDIR /sensor-module

ADD . .

RUN pip install --upgrade pip
RUN cd sensorapp/sensorhandler/Adafruit_Python_DHT && python setup.py install
RUN pip install requests
CMD python sensorapp/start.py
