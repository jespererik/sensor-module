from sensorhandler import sensorhandler
from ConfigParser import ConfigParser
from Queue import Queue
import json
import threading
import requests
import sys
import logging
import time

FORMAT = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = "/sensor-module/test/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG
)

NODE_LOGGER = logging.getLogger(__name__)

packet_queue = Queue()

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
    
    for sensor in sensors:
        pins = config.get("SENSOR_PINS", sensor)
        reading_type = config.get("READING_TYPES", sensor)
        sensor_thread = threading.Thread(target = sensorhandler.start_sensor, args = (sensor, pins, reading_type, packet_queue), name = sensor)
        sensor_thread.start()
    
    NODE_LOGGER.debug("EXIT")


def register_node(config):

    url = "http://{ip}:{port}/api/nodes".format(
            ip = config.get("NETWORK", "SERVER_IP"), 
            port = config.get("NETWORK", "SERVER_PORT")
        )
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
            node_name = config.get("NODE", "NAME")
        )
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

def get_route_for_sensor(config, sensor_id):
    url = "http://{ip}:{port}/api/nodes/{node_name}/sensors/{sensor_name}/readings".format(
            ip = config.get("NETWORK", "SERVER_IP"), 
            port = config.get("NETWORK", "SERVER_PORT"), 
            node_name = config.get("NODE", "NAME"), 
            sensor_name = sensor_id
        )
    return url

def post_reading_packet(json_packet, url, authorization):
    NODE_LOGGER.debug("ENTER")
    NODE_LOGGER.info("Sending reading packet to: {} content: {}".format(url, json_packet))
    requests.post(url, json = json_packet, auth = authorization)
    NODE_LOGGER.debug("EXIT")


def post_handler(config):
    NODE_LOGGER.debug("ENTER")
    NODE_LOGGER.debug("%s", packet_queue)
    auth = (config.get("AUTHORIZATION", "username"),config.get("AUTHORIZATION", "password"))

    while True:
        packet = packet_queue.get()
        NODE_LOGGER.debug("Fetched packet %s from packet_queue", packet)
        url = get_route_for_sensor(config, packet["SENSOR_ID"])
        try:
            post_reading_packet(packet, url, auth)
        except requests.exceptions.ConnectionError as err:
            NODE_LOGGER.error("Host unreachable url: {} error: {}".format(url, err))
            time.sleep(10)
            continue
    NODE_LOGGER.debug("EXIT")


def node_init():
    config = ConfigParser()
    config.read("/sensor-module/test/shared/node.conf")

    if config.get("NODE", "NAME") == "":
        config.set("NODE", "init", True)

    if config.getboolean("NODE", "init"):
        register_node(config)
        register_sensor(config)

    start_threads(config.get("NODE", "sensors").split(","), config)
    post_handler(config)  

if __name__ == '__main__':
    node_init()