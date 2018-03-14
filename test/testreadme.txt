docker build -t dummy-sensor . 
sudo docker run -v $(pwd)/shared:/sensor-module/test/shared --privileged --net=host -ti -d dummy-sensor:latest
