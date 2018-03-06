FROM python:2 

WORKDIR /sensor-module

ADD /shared ./shared
COPY /shared ./shared
ADD /sensorapp ./sensorapp

RUN cd sensorapp/Adafruit_Python_DHT && python setup.py install
RUN pip install requests
RUN mv Adafruit_Python_DHT/ sensorapp/
CMD ["python"]
