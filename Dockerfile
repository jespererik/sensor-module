FROM python:2 

ADD temp-reading.py /

RUN apt-get install git-core
RUN    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
RUN    cd Adafruit_Python_DHT && python setup.py install

CMD [ "python", "./temp-readingt.py" ]
