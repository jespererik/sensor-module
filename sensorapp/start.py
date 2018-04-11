from ConfigParser import ConfigParser
import httphandler
import json
import thread
import requests
import sys
import logging
import time
import base64


logging.basicConfig(
    filename = "/sensor-module/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG
)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
NODE_LOGGER = logging.getLogger(__name__)

def auth(config):
    data = {
        "Authorization": 'Basic '+base64.b64encode(bytes(config.get("AUTHORIZATION", "username")+":"+config.get("AUTHORIZATION", "password"))).decode("utf-8")
    }
    return data

def node_json(config):
    config_data = {
        "NODE_NAME": config.get("NODE", "NAME"),
        "LOCATION": config.get("NODE", "LOCATION")
    }
    return config_data

def sensor_json(config, sensor_id):
    json_data = {
        "NODE_NAME": config.get("NODE", "NAME"),
        "SENSOR": sensor_id,
        "LOCATION": config.get("NODE", "LOCATION")
    }
    return json_data

def start_threads():
    for sensor in config.get("NODE", "SENSORS").split(","):
        try:
            thread.start_new_thread(httphandler.run_sensor, (sensor,))
        except:
            NODE_LOGGER.error("Failed to Spawn thread for %s", sensor)
def register_node(config):

    url = "http://{ip}:{port}/api/nodes".format(
            ip = config.get("NETWORK", "SERVER_IP"), 
            port = config.get("NETWORK", "SERVER_PORT")
        )
    #register node
    while True:
        try:
            response = requests.post(url, json = node_json(config), Authorization = auth(config))
            response.raise_for_status()
            response_data = json.loads(response.content)
            NODE_LOGGER.info('init complete')
            
            if (response_data['NODE_NAME'] !=  config.get("NODE", "NAME")):
                config.set("NODE", "NAME", response_data["NODE_NAME"])
                with open("sensor-module/shared/node.conf", "w") as configfile:
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
                response = requests.post(url, json = sensor_json(config, sensor), Authorization = auth(config))
                response.raise_for_status()
            break
        except requests.exceptions.ConnectionError as err:
            NODE_LOGGER.error("Host unreachable, retrying connection in 10s\nerror: {}".format(err))
            time.sleep(10)
            continue

def node_init():
    config = ConfigParser()
    config.read("/sensor-module/shared/node.conf")
    register_node(config)
    register_sensor(config)
    start_threads()   

if __name__ == '__main__':
    node_init()