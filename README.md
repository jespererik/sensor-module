# sensor-module
The sensor module runs in a docker container. 
To create the image run:

docker build -t sensor-module .

docker run --privileged --net=host -ti sensor-module:latest
