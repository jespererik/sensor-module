import threading
import json
from sensorhandler import get_temperature
from datetime import datetime
import requests
import logging
import time
import sys

logging.basicConfig(
    filename = "/sensor-module/test/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG,

)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
REST_LOGGER = logging.getLogger(__name__)

def try_file_open(filepath):
    try: 
        open(filepath)
    except IOError:
        REST_LOGGER.error("File does not appear to exist: {}".format(filepath))
        sys.exit(1)

def read_config_file(filepath):
    try_file_open(filepath)
    config_data = {} 
    with open(filepath, "r") as config_file:
        for element in config_file:
            key, value = element.strip('\n').split(":")
            config_data[key] = value
    #NODE_LOGGER.info("Read from {}: keys: {} values: {}".format(filepath ,conf_file.iteritems()))
    config_file.close()
    return config_data


def post_data():
    node_config = read_config_file("/sensor-module/test/shared/node.conf")
    network_config = read_config_file("/sensor-module/test/shared/network.conf")
    sensor_data = node_config
    #('/api/nodes/<string:node_name>/sensors/<string:sensor_name>/readings'
    url = "http://{ip}:{port}/api/nodes/{node_name}/sensors/{sensor_name}/readings"\
        .format(ip = network_config["SERVER_IP"], port = network_config["SERVER_PORT"], node_name = node_config['NODE_NAME'], sensor_name = node_config['SENSOR_NAME'])
    while True:
        try:
            sensor_data['DATA'] = get_temperature()
            sensor_data['TIMESTAMP'] = str(datetime.now())
            REST_LOGGER.info("Sending reading packet to: {} content: {}".format(url, sensor_data))
            response = requests.post(url, json = sensor_data)
            print(json.loads(response.content))
        except requests.exceptions.ConnectionError as err:
            REST_LOGGER.error("Host unreachable url: {} error: {}".format(url, err))
            time.sleep(10)
            continue
        time.sleep(5)

def run_rest():  
    post_data()
