from time import sleep
from datetime import datetime
from readinghandler import get_reading
from ConfigParser import ConfigParser
import thread
import json
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

def auth():
    data = {
        "username": "test",
        "password": "python"
    }
    return data

def post_data(reading_type, sensor_pins, json_packet, url):
    json_packet['DATA'] = "%.2f" % get_reading(
        json_packet["SENSOR"],
        json_packet["READING_TYPE"],
        sensor_pins
        )
    json_packet['TIMESTAMP'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    REST_LOGGER.info("Sending reading packet to: {} content: {}".format(url, json_packet))
    response = requests.post(url, json = json_packet, data = auth())
    print(json.loads(response.content))
    return



def post_handler(config, sensor_id):
    sensor_data = {
        "NODE_NAME": config.get("NODE", "NAME"),
        "SENSOR": sensor_id,
        "LOCATION": config.get("NODE", "LOCATION"),
        "READING_TYPE": None,
        "DATA": None,
        "TIMESTAMP": None
    }
    #('/api/nodes/<string:node_name>/sensors/<string:sensor_name>/readings'
    url = "http://{ip}:{port}/api/nodes/{node_name}/sensors/{sensor_name}/readings".format(
            ip = config.get("NETWORK", "SERVER_IP"), 
            port = config.get("NETWORK", "SERVER_PORT"), 
            node_name = config.get("NODE", "NAME"), 
            sensor_name = sensor_id
            )
    while True:
        try:
            for reading_type in config.get("READING_TYPES", sensor_id).split(","):
                sensor_data["READING_TYPE"] = reading_type
                pins = config.get("SENSOR_PINS", sensor_id).split(",")
                thread.start_new_thread(post_data, (reading_type, pins, sensor_data, url))
        except requests.exceptions.ConnectionError as err:
            REST_LOGGER.error("Host unreachable url: {} error: {}".format(url, err))
            time.sleep(10)
            continue

def run_sensor(sensor_id):
    config = ConfigParser()
    config.read("sensor-module/test/shared/node.conf")
    post_handler(config, sensor_id)

  


'''if __name__ == "__main__":
 
    my_thread = threading.Thread(target = sensor_data_stream)
    my_thread.start()
'''
