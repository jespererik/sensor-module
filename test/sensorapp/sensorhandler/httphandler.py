from time import sleep
from datetime import datetime
from readinghandler import get_reading
from ConfigParser import ConfigParser
import json
import requests
import logging
import time
import sys

FORMAT = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = "/sensor-module/test/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG
)

HTTP_LOGGER = logging.getLogger(__name__)

def post_data(json_packet, url, authorization):
    HTTP_LOGGER.debug("ENTER")
    HTTP_LOGGER.info("Sending reading packet to: {} content: {}".format(url, json_packet))
    requests.post(url, json = json_packet, auth = authorization)
    HTTP_LOGGER.debug("EXIT")

def create_json_packet(httpconfig, sensor_id, reading_type):
    HTTP_LOGGER.debug("ENTER")
    reading = get_reading(sensor_id, reading_type, httpconfig.get("SENSOR_PINS", sensor_id).split(","))
    json_packet = {
        "TYPE": reading_type,
        "DATA": float("%.2f" % reading),
        "TIMESTAMP": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    HTTP_LOGGER.debug("EXIT")
    return json_packet



def post_handler(httpconfig, sensor_id):
    HTTP_LOGGER.debug("ENTER")

    #('/api/nodes/<string:node_name>/sensors/<string:sensor_name>/readings'
    url = "http://{ip}:{port}/api/nodes/{node_name}/sensors/{sensor_name}/readings".format(
            ip = httpconfig.get("NETWORK", "SERVER_IP"), 
            port = httpconfig.get("NETWORK", "SERVER_PORT"), 
            node_name = httpconfig.get("NODE", "NAME"), 
            sensor_name = sensor_id
            )
    while True:
        try:
            packet = create_json_packet(httpconfig, sensor_id, httpconfig.get("READING_TYPES", sensor_id))
            post_data(packet, url, (httpconfig.get("AUTHORIZATION", "username"),httpconfig.get("AUTHORIZATION", "password")))
        except requests.exceptions.ConnectionError as err:
            HTTP_LOGGER.error("Host unreachable url: {} error: {}".format(url, err))
            time.sleep(10)
            continue
    HTTP_LOGGER.debug("EXIT")

def run_sensor(sensor_id, httpconfig):
    HTTP_LOGGER.debug("ENTER")
    post_handler(httpconfig, sensor_id)
    HTTP_LOGGER.debug("EXIT")

  


'''if __name__ == "__main__":
 
    my_thread = threading.Thread(target = sensor_data_stream)
    my_thread.start()
'''
