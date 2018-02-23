import json
import threading
import requests
import sys
from sensorhandler import *
from restfulapi  import *

nodeInfo = {
   'nodeID': '',
}

def tryFileOpen(filepath):
    try: 
        open(filepath)
    except IOError:
        print "Error: file does not appear to exist."
        sys.exit(1)

def readNodeID():
    tryFileOpen("/shared/sensor.conf")
    fopen = open("/shared/sensor.conf", "r")
    nodeInfo['nodeID'] = fopen.readline()
    print nodeInfo['nodeID']
    fopen.close()

def writeNodeID(nodeID):
    tryFileOpen("/shared/sensor.conf")
    fopen = open("/shared/sensor.conf", "w")
    fopen.write(nodeID)
    fopen.close()


def startThreads():
    restThread = threading.Thread(target = runRest)
    DHT11Thread = threading.Thread(target = DHT11DataStream)
    
    restThread.start()
    DHT11Thread.start()

def errorLog(url, err):
    tryFileOpen("/shared/log/errorLog.log")
    logfile = open("/shared/log/errorLog.log", "a")
    logfile.write("Failed to connect to {0}: {1}\n".format(str(url), str(err)))
    logfile.close()

def __init():
    url = 'http://127.0.0.1:5000/init'
    while True:
        try:
            readNodeID()
            response = requests.post(url, json=nodeInfo)
            response.raise_for_status()
            print 'Server Init Complete'
            responseData = json.loads(response.content)
            if (responseData['nodeID'] !=  nodeInfo['nodeID']):
                writeNodeID(responseData['nodeID'])
                print('Aquired nodeID: {}').format(responseData['nodeID'])
            else:
                pass
        except requests.exceptions.ConnectionError as err:
            errorLog(url, err)
            print 'Retry'
            sleep(10)
            continue
            #sys.exit(1)
        break
    startThreads()   
    
__init()