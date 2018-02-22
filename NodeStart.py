import json
import threading
import requests
import sys
from DHT11Handler import *
from RestfulNode  import *

nodeInfo = {
   'NODE_ID': '',
}

def tryFileOpen(filepath):
    try: 
        open(filepath)
    except IOError:
        print "Error: file does not appear to exist."
        sys.exit(1)

def readNodeID():
    tryFileOpen("/storage/nodeID.txt")
    fopen = open("/storage/nodeID.txt", "r")
    nodeInfo['NODE_ID'] = fopen.readline()
    print nodeInfo['NODE_ID']
    fopen.close()

def writeNodeID(nodeID):
    tryFileOpen("/storage/nodeID.txt")
    fopen = open("/storage/nodeID.txt", "w")
    fopen.write(nodeID)
    fopen.close()


def startThreads():
    restThread = threading.Thread(target = runRest)
    DHT11Thread = threading.Thread(target = DHT11DataStream)
    
    restThread.start()
    DHT11Thread.start()

def errorLog(url, err):
    tryFileOpen("/storage/log/errorLog.log")
    logfile = open("/storage/log/errorLog.log", "a")
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
            if (responseData['NODE_ID'] !=  nodeInfo['NODE_ID']):
                writeNodeID(responseData['NODE_ID'])
                print('Aquired NODE_ID: {}').format(responseData['NODE_ID'])
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