FROM python:2 

ADD DHT11Handler.py /
ADD NodeStart.py /
ADD RestfulNode.py /

RUN apt-get install git-core
RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git
RUN cd Adafruit_Python_DHT && python setup.py install
RUN pip install flask
RUN pip install requests

CMD ["/bin/bash"]
