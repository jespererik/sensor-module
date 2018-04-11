from datetime import datetime
import random
import logging
import time
import requests


FORMAT = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = "/sensor-module/test/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG
)

SENSOR_LOGGER = logging.getLogger(__name__)

ARRAY_SIZE = 10


def __mean(iterable):
    return sum(iterable) / len(iterable)

def __process_DHT11(pins, sensor_index = None):
    reading_array = [0] * ARRAY_SIZE
    for i in range(0, ARRAY_SIZE):
        reading_array[i] = random.uniform(-15, 40)
        time.sleep(0.5)
    return reading_array

def create_packet(httpconfig, sensor_id, reading_type):
    SENSOR_LOGGER.debug("ENTER")
    reading = get_reading(sensor_id, reading_type, httpconfig.get("SENSOR_PINS", sensor_id).split(","))
    packet = {
        "TYPE": reading_type,
        "DATA": float("%.2f" % reading),
        "TIMESTAMP": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    SENSOR_LOGGER.debug("EXIT")
    return packet

def post_data(json_packet, url, authorization):
    SENSOR_LOGGER.debug("ENTER")
    SENSOR_LOGGER.info("Sending reading packet to: {} content: {}".format(url, json_packet))
    requests.post(url, json = json_packet, auth = authorization)
    SENSOR_LOGGER.debug("EXIT")

def post_handler(httpconfig, sensor_id):
    SENSOR_LOGGER.debug("ENTER")
    url = "http://{ip}:{port}/api/nodes/{node_name}/sensors/{sensor_name}/readings".format(
            ip = httpconfig.get("NETWORK", "SERVER_IP"), 
            port = httpconfig.get("NETWORK", "SERVER_PORT"), 
            node_name = httpconfig.get("NODE", "NAME"), 
            sensor_name = sensor_id
            )
    while True:
        try:
            packet = create_packet(httpconfig, sensor_id, httpconfig.get("SENSOR_PINS", sensor_id))
            post_data(packet, url, (httpconfig.get("AUTHORIZATION", "username"),httpconfig.get("AUTHORIZATION", "password")))
        except requests.exceptions.ConnectionError as err:
            SENSOR_LOGGER.error("Host unreachable url: {} error: {}".format(url, err))
            time.sleep(10)
            continue
    SENSOR_LOGGER.debug("EXIT")


def get_reading(sensor_id, reading_type, pins):
    if sensor_id == "DHT11":
        if reading_type == "temperature":
            SENSOR_LOGGER.debug("EXIT")
            return __mean(__process_DHT11(pins, 1))
        elif reading_type == "humidity":
            SENSOR_LOGGER.debug("EXIT")
            return __mean(__process_DHT11(pins, 0))
    

    
