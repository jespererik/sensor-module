import threading
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

def postTemp():
    try:
        fopen = open("/sensor-module/shared/sensor.conf", "r")
    except IOError as err:
        print(err)
        sys.exit(1)
           
    sensorData['NODE_NAME'] = fopen.readline()
    sensorData['DATATYPE'] = "Temperature"
    sensorData['SENSOR_NAME'] = "DHT11"
    fopen.close()
    url = 'http://192.168.0.121:5000/Temp'
    while True:
        try:
            sensorData['DATA'] = getTemperature()
            sensorData['TIMESTAMP'] = str(datetime.now())
            requests.post(url, json=sensorData)
        except requests.exceptions.ConnectionError as err:
            errorLog(url, err)
            print 'Retry'
            sleep(10)
            continue
        sleep(5)

def runRest():    
    postTemp()
