from sensorhandler import sensor_data_stream
from restfulapi  import run_rest
import json
import threading
import requests
import sys
import logging
import time

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
    config_data = {} 
    with open(filepath, "r") as config_file:
        for element in config_file:
            key, value = element.strip('\n').split(":")
            config_data[key] = value
    #NODE_LOGGER.info("Read from {}: keys: {} values: {}".format(filepath ,conf_file.iteritems()))
    config_file.close()
    return config_data

def write_config_file(filepath, config, new_key, new_value):
    try_file_open(filepath)
    with open(filepath, "w") as config_file:
        for key, value in config.iteritems():
            if new_key == key:
                config_file.write(key + ':' + new_value + '\n')
            else:
                config_file.write(key + ':' + value + '\n')
    NODE_LOGGER.info('Wrote to new values to {}: keys: {} values: {}'.format(filepath, new_key, new_value))
    config_file.close()

def start_threads():
    restful_thread = threading.Thread(target = run_rest)
    sensor_thread = threading.Thread(target = sensor_data_stream)
    
    restful_thread.start()
    sensor_thread.start()

def register_node():
    node_config = read_config_file("/sensor-module/shared/node.conf")
    network_config = read_config_file("/sensor-module/shared/network.conf")
    url = "http://{ip}:{port}/api/nodes".format(ip = network_config["SERVER_IP"], port = network_config["SERVER_PORT"])
    #register node
    while True:
        try:
            response = requests.post(url, json = node_config)
            response.raise_for_status()
            response_data = json.loads(response.content)
            NODE_LOGGER.info('init complete')
            
            if (response_data['NODE_NAME'] !=  node_config['NODE_NAME']):
                write_config_file("/sensor-module/shared/node.conf", node_config, 'NODE_NAME', response_data['NODE_NAME'])
                NODE_LOGGER.info("Fresh init: NODE_NAME: {}".format(response_data["NODE_NAME"]))
            else:
                pass
            break
        except requests.exceptions.ConnectionError as err:
            NODE_LOGGER.error("Host unreachable, retrying connection in 10s\nerror: {}".format(err))
            time.sleep(10)
            continue


def register_sensor():
    node_config = read_config_file("/sensor-module/shared/node.conf")
    network_config = read_config_file("/sensor-module/shared/network.conf")
    url = "http://{ip}:{port}/api/nodes/{node_name}/sensors".format(ip = network_config["SERVER_IP"], port = network_config["SERVER_PORT"], node_name = node_config['NODE_NAME'])
    while True:
        try:
            response = requests.post(url, json = node_config)
            response.raise_for_status()
            break
        except requests.exceptions.ConnectionError as err:
            NODE_LOGGER.error("Host unreachable, retrying connection in 10s\nerror: {}".format(err))
            time.sleep(10)
            continue

def node_init():
    register_node()
    register_sensor()
    start_threads()   

if __name__ == '__main__':
    node_init()