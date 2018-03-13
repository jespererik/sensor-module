# sensor-module
The sensor module runs in a docker container. 
To create the image run:

docker build -t sensor-module .

docker run -v ~/sensor-module/shared/:/sensor-module/shared/ --privileged --net=host -ti -d sensor-module:latest

To check log run:

tail -f shared/node.log

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)
