from datetime import datetime
import random
import logging
import time
import requests
''' import libraries for sensors here '''
import Adafruit_DHT


FORMAT = '%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(
    format = FORMAT,
    filename = "/sensor-module/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG
)
SENSOR_LOGGER = logging.getLogger(__name__)

ARRAY_SIZE = 10


def mean(iterable):
    return sum(iterable) / len(iterable)


def start_DHT11_temp(sensor_id, reading_type, GPIO_pins, packet_queue):
    SENSOR_LOGGER.debug("ENTER")
    SENSOR_LOGGER.debug("Starting %s on pins %s", sensor_id, GPIO_pins)
    reading_array = [0] * ARRAY_SIZE

    while True:
        for i in range(0, ARRAY_SIZE):
            reading_array[i] = Adafruit_DHT.read_retry(11, 4)[1]
            time.sleep(0.5)
        reading_packet = create_packet(sensor_id, reading_type, mean(reading_array))
        packet_queue.put(reading_packet)
        SENSOR_LOGGER.debug("Added %s to packet queue", reading_packet)

    SENSOR_LOGGER.debug("EXIT")

def start_DHT11_humi(sensor_id, reading_type, GPIO_pins, packet_queue):
    SENSOR_LOGGER.debug("ENTER")
    SENSOR_LOGGER.debug("Starting %s on pins %s", sensor_id, GPIO_pins)

    reading_array = [0] * ARRAY_SIZE

    while True:
        for i in range(0, ARRAY_SIZE):
            reading_array[i] = Adafruit_DHT.read_retry(11, 4)[0]
            time.sleep(0.5)
        reading_packet = create_packet(sensor_id, reading_type, mean(reading_array))
        packet_queue.put(reading_packet)
        SENSOR_LOGGER.debug("Added %s to packet queue", reading_packet)

    SENSOR_LOGGER.debug("EXIT")
        

def create_packet(sensor_id, reading_type, reading):
    SENSOR_LOGGER.debug("ENTER")
    packet = {
        "SENSOR_ID": sensor_id,
        "TYPE": reading_type,
        "DATA": float("%.2f" % reading),
        "TIMESTAMP": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    SENSOR_LOGGER.debug("EXIT")

    return packet


def start_sensor(sensor_id, GPIO_pins, reading_type, packet_queue):
    SENSOR_LOGGER.debug("ENTER")
    SENSOR_LOGGER.debug("%s %s %s %s", sensor_id, GPIO_pins, reading_type, packet_queue)
    if sensor_id == "DHT11-Temperature":
        start_DHT11_temp(sensor_id, reading_type, GPIO_pins, packet_queue)
    elif sensor_id == "DHT11-Humidity":
        start_DHT11_humi(sensor_id, reading_type, GPIO_pins, packet_queue)

    SENSOR_LOGGER.debug("EXIT")
    

    
