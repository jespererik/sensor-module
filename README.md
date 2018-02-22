# sensor-module
The sensor module runs in a docker container. 
To create the image run:

docker build -t sensor-module .

docker run --privileged --net=host -ti sensor-module:latest python RestfulNode.py

docker run -v ~/sensor-module/storage/log:/storage/log --privileged --net=host -ti sensor-module:latest bash

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)
