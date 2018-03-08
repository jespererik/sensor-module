import threading
import json
from sensorhandler import *
from datetime import datetime
import requests
import logging
import sys

logging.basicConfig(
    filename = "/sensor-module/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG,

)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
REST_LOGGER = logging.getLogger(__name__)

sensorData = {
        'NODE_NAME'     :'',
        'SENSOR_NAME'   :'',
        'TYPE'          :'',
        'TIMESTAMP'     :'',
        'DATA'          :''

    }

def try_file_open(filepath):
    try: 
        open(filepath)
    except IOError:
        #NODE_LOGGER.error("File does not appear to exist: {}".format(filepath))
        sys.exit(1)


def read_config_file(filepath):
    try_file_open(filepath)
    node_config = {} 
    with open(filepath, "r") as conf_file:
        for element in conf_file:
            key, value = element.strip('\n').split(":")
            node_config[key] = value
    #NODE_LOGGER.info("Read from {}: keys: {} values: {}".format(filepath ,conf_file.iteritems()))
    conf_file.close()
    return node_config


def postTemp():
    node_conf = read_config_file("/sensor-module/shared/node.conf")
    sensorData['NODE_NAME'] = node_conf["NODE_NAME"]
    sensorData['TYPE'] = "Temperature"
    sensorData['SENSOR_NAME'] = "DHT11"
    url = "http://{ip}:{port}/Temp".format(ip = node_conf["SERVER_IP"], port = node_conf["SERVER_PORT"])
    while True:
        try:
            sensorData['DATA'] = get_temperature()
            sensorData['TIMESTAMP'] = str(datetime.now())
            REST_LOGGER.info("Sending reading packet to: {} content: {}".format(url, sensorData))
            response = requests.post(url, json=sensorData)
            print(json.loads(response.content))
        except requests.exceptions.ConnectionError as err:
            REST_LOGGER.error("Host unreachable url: {} error: {}".format(url, err))
            print('Retry')
            sleep(10)
            continue
        sleep(5)

def runRest():  
    postTemp()
