# sensor-module
The sensor module runs in a docker container. 
To create the image run:

docker build -t sensor-module .

docker run -v ~/sensor-module/shared/:/sensor-module/shared/ --privileged --net=host -ti sensor-module:latest bash

From bash run:

python sensorapp/start.py

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)
