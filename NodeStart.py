from RestfulNode  import *
import json
import threading
import requests
import sys
from DHT11Handler import *

nodeInfo = {
   'NODE_ID': '',
   'NODE_IP': '192.168.0.1',
   'NODE_PORT': '5005', 
}

def startThreads():
    restThread = threading.Thread(target = runRest)
    DHT11Thread = threading.Thread(target = DHT11DataStream)
    
    restThread.start()
    DHT11Thread.start()

def __init():
    url = 'http://127.0.0.1:5000/init'
    try:
        response = requests.post(url, json=nodeInfo)
        response.raise_for_status()
        print 'Server Init Complete'
        respData = json.loads(response.content)
        print('Aquired NODE_ID: {}').format(respData['NODE_ID'])
    except requests.exceptions.ConnectionError as err:
        print err
        print 'what do'
        #sys.exit(1)
    startThreads()   
    
__init()