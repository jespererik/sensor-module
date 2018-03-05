import threading
import json
from sensorhandler import *
from datetime import datetime
import requests

sensorData = {
        'NODE_NAME'     :'',
        'SENSOR_NAME'   :'',
        'TYPE'          :'',
        'TIMESTAMP'     :'',
        'DATA'          :''

    }

def errorLog(url, err):
    logfile = open("/sensor-module/shared/error.log", "a")
    logfile.write("Failed to connect to {0}: {1}\n".format(str(url), str(err)))
    logfile.close()


def postTemp(node_name):
    sensorData['NODE_NAME'] = node_name
    sensorData['TYPE'] = "Temperature"
    sensorData['SENSOR_NAME'] = "DHT11"
    url = 'http://192.168.0.121:5000/Temp'
    while True:
        try:
            sensorData['DATA'] = getTemperature()
            sensorData['TIMESTAMP'] = str(datetime.now())
            response = requests.post(url, json=sensorData)
            print(json.loads(response.content))
        except requests.exceptions.ConnectionError as err:
            errorLog(url, err)
            print 'Retry'
            sleep(10)
            continue
        sleep(5)

def runRest(node_name):    
    postTemp(node_name)
