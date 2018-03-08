from sensorhandler import *
from restfulapi  import *
import json
import threading
import requests
import sys
import logging
import time

#Add errorhandling to all functions which have a request to the server
#Where they could get a invalid packet structure response

logging.basicConfig(
    filename = "/sensor-module/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG

)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
NODE_LOGGER = logging.getLogger(__name__)

def try_file_open(filepath):
    try: 
        open(filepath)
    except IOError:
        NODE_LOGGER.error("File does not appear to exist: {}".format(filepath))
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


def write_config_file(filepath, config, new_key, new_value):
    try_file_open(filepath)
    with open(filepath, "w") as conf_file:
        for key, value in config.iteritems():
            if new_key == key:
                conf_file.write(key + ':' + new_value + '\n')
            else:
                conf_file.write(key + ':' + value + '\n')
    NODE_LOGGER.info('Wrote to new values to {}: keys: {} values: {}'.format(filepath, new_key, new_value))
    conf_file.close()


def Start_Threads():
    restThread = threading.Thread(target = runRest)
    DHT11Thread = threading.Thread(target = DHT11DataStream)
    
    restThread.start()
    DHT11Thread.start()


def node_init():
    config = read_config_file("/sensor-module/shared/node.conf")
    url = "http://{ip}:{port}/init".format(ip = config["SERVER_IP"], port = config["SERVER_PORT"])

    while True:
        try:
            response = requests.post(url, json = config)
            response.raise_for_status()
            response_data = json.loads(response.content)
            NODE_LOGGER.info('init complete')
            
            if (response_data['NODE_NAME'] !=  config['NODE_NAME']):
                write_config_file("/sensor-module/shared/node.conf", config, 'NODE_NAME', response_data['NODE_NAME'])
                NODE_LOGGER.info("Fresh init: NODE_NAME: {}".format(response_data["NODE_NAME"]))
            else:
                pass
            break
        except requests.exceptions.ConnectionError as err:
            NODE_LOGGER.error("Host unreachable, retyring connection in 10s\nerror: {}".format(err))
            time.sleep(10)
            continue
    
    Start_Threads()   

if __name__ == '__main__':
    node_init()