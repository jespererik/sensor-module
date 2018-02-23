FROM python:2 

WORKDIR /sensor-module

ADD shared /shared
COPY shared /shared
ADD sensorapp /sensorapp
ADD sensorapp ./sensorapp/start.py
ADD sensorapp ./sensorapp/restfulapi.py
ADD sensorapp ./sensorapp/sensorhandler.py

RUN apt-get install git-core
RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git
RUN cd Adafruit_Python_DHT && python setup.py install
RUN pip install requests
RUN mv Adafruit_Python_DHT/ sensorapp/
CMD ["python"]
