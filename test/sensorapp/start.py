from ConfigParser import ConfigParser
from sensorhandler import sensorhandler
import json
import threading
import requests
import sys
import logging
import time
import Queue

FORMAT = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = "/sensor-module/test/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG
)

NODE_LOGGER = logging.getLogger(__name__)

def node_json(config):
    config_data = {
        "NODE_NAME": config.get("NODE", "NAME"),
        "LOCATION": config.get("NODE", "LOCATION")
    }
    return config_data

def sensor_json(config, sensor_id):
    json_data = {
        "NODE_NAME": config.get("NODE", "NAME"),
        "SENSOR_NAME": sensor_id,
        "LOCATION": config.get("NODE", "LOCATION")
    }
    return json_data

def start_threads(sensors, config):
    NODE_LOGGER.debug("ENTER")
    sensor_thread = threading.Thread(target = sensorhandler.post_handler, args = (config, sensors[0]), name = sensors[0])
    sensor_thread.start()
    for sensor_thread in threading.enumerate():
        if sensor_thread != threading.current_thread():
            sensor_thread.join()
    NODE_LOGGER.debug("EXIT")


def register_node(config):

    url = "http://{ip}:{port}/api/nodes".format(
            ip = config.get("NETWORK", "SERVER_IP"), 
            port = config.get("NETWORK", "SERVER_PORT")
        )
    #register node
    while True:
        try:
            response = requests.post(url, json = node_json(config), auth = (config.get("AUTHORIZATION", "username"),config.get("AUTHORIZATION", "password")))
            response.raise_for_status()
            NODE_LOGGER.debug('init response %s', response.content)
            response_data = json.loads(response.content)
            NODE_LOGGER.info('init complete')
            
            if (response_data['NODE_NAME'] !=  config.get("NODE", "NAME")):
                config.set("NODE", "NAME", response_data["NODE_NAME"])
                config.set("NODE", "init", False)
                with open("/sensor-module/test/shared/node.conf", "w") as configfile:
                    config.write(configfile)
                NODE_LOGGER.info("Fresh init: NODE_NAME: {}".format(response_data["NODE_NAME"]))
            else:
                pass
            break
        except requests.exceptions.ConnectionError as err:
            NODE_LOGGER.error("Host unreachable, retrying connection in 10s\nerror: {}".format(err))
            time.sleep(10)
            continue
    

def register_sensor(config):
    url = "http://{ip}:{port}/api/nodes/{node_name}/sensors".format(
        ip = config.get("NETWORK", "SERVER_IP"), 
        port = config.get("NETWORK", "SERVER_PORT"), 
        node_name = config.get("NODE", "NAME"))
    while True:
        try:
            for sensor in config.get("NODE", "SENSORS").split(","):
                response = requests.post(url, json = sensor_json(config, sensor), auth = (config.get("AUTHORIZATION", "username"),config.get("AUTHORIZATION", "password")))
                response.raise_for_status()
            break
        except requests.exceptions.ConnectionError as err:
            NODE_LOGGER.error("Host unreachable, retrying connection in 10s\nerror: {}".format(err))
            time.sleep(10)
            continue


def node_init():
    config = ConfigParser()
    config.read("/sensor-module/test/shared/node.conf")

    if config.get("NODE", "NAME") == "":
        config.set("NODE", "init", True)

    if config.getboolean("NODE", "init"):
        register_node(config)
        register_sensor(config)

    start_threads(config.get("NODE", "sensors").split(","), config)   

if __name__ == '__main__':
    node_init()