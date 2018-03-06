import threading
import json
from sensorhandler import *
from datetime import datetime
import requests

logging.basicConfig(
    filename = "/sensor-module/shared/node.log",
    filemode = 'w',
    level = logging.DEBUG,

)
formatter = logging.formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
REST_LOGGER = logging.getLogger(__name__)

sensorData = {
        'NODE_NAME'     :'',
        'SENSOR_NAME'   :'',
        'TYPE'          :'',
        'TIMESTAMP'     :'',
        'DATA'          :''

    }


def postTemp(node_conf):
    sensorData['NODE_NAME'] = node_conf["NODE_NAME"]
    sensorData['TYPE'] = "Temperature"
    sensorData['SENSOR_NAME'] = "DHT11"
    url = "http://{ip}:{port}/Temp".format(node_conf["SERVER_IP"], node_conf["SERVER_PORT"])
    while True:
        try:
            sensorData['DATA'] = getTemperature()
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

def runRest(node_conf):
    print(node_conf)  
    postTemp(node_conf)
