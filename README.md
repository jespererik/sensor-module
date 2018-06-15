# sensor-module
The sensor module runs in a docker container. 

When first running the applicaton use the build script and specify the information about the setup (don't use spaces in the input, since this is not supported yet!). Check the example.conf for reference.

Alternatively edit the node.conf file manually, and build and run the image with the commands below:

docker build -t sensor-module .

docker run -v $(pwd)/shared:/sensor-module/shared --privileged --net=host -ti -d --restart unless-stopped -e TZ=Europe/Stockholm sensor-module:latest

To check log:

tail -f shared/node.log

Stop all containers:

docker stop $(docker ps -a -q)

Remove all containers:

docker rm $(docker ps -a -q)
