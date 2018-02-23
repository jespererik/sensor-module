import threading
from sensorhandler import *
from datetime import datetime
import requests

sensorData = {
        'nodeID'    :'',
        'dataType'  :'',
        'timestamp' :'',
        'data'      :''

    }

def tryFileOpen(filepath):
    try: 
        open(filepath)
    except IOError:
        print "Error: file does not appear to exist."
        sys.exit(1)

def errorLog(url, err):
    tryFileOpen("/shared/log/errorlog.log")
    logfile = open("/shared/log/errorlog.log", "a")
    logfile.write("Failed to connect to {0}: {1}\n".format(str(url), str(err)))
    logfile.close()

def postTemp():
    tryFileOpen("/shared/sensor.conf")
    fopen = open("/shared/sensor.conf", "r")   
    sensorData['nodeID'] = fopen.readline()
    sensorData['dataType'] = "Temperature"
    fopen.close()
    url = 'http://127.0.0.1:5000/Temp'
    while True:
        try:
            sensorData['data'] = getTemperature()
            sensorData['timestamp'] = str(datetime.now())
            requests.post(url, json=sensorData)
        except requests.exceptions.ConnectionError as err:
            errorLog(url, err)
            print 'Retry'
            sleep(10)
            continue
        break
        sleep(5)

def runRest():    
    postTemp()