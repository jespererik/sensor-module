FROM python:2 

WORKDIR /sensor-module

ADD . /shared
COPY shared /shared
ADD sensorapp /sensorapp

RUN apt-get install git-core
RUN cd /sensorapp && git clone https://github.com/adafruit/Adafruit_Python_DHT.git
RUN cd Adafruit_Python_DHT && python setup.py install
RUN pip install flask
RUN pip install requests

CMD ["python"]
