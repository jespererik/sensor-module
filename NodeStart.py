from RestfulNode  import *
import json
import threading
import requests
import sys
import netifaces
from DHT11Handler import *

nodeInfo = {
   'NODE_ID': '',
   'NODE_IP': '0.0.0.0',
}

def startThreads():
    restThread = threading.Thread(target = runRest)
    DHT11Thread = threading.Thread(target = DHT11DataStream)
    
    restThread.start()
    DHT11Thread.start()

def __init():
    url = 'http://127.0.0.1:5000/init'
    #get IP-address
    netifaces.ifaddresses('eth0')
    ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
    nodeInfo['NODE_IP'] = ip
    while True:
        try:
            response = requests.post(url, json=nodeInfo)
            response.raise_for_status()
            print 'Server Init Complete'
            respData = json.loads(response.content)
            print('Aquired NODE_ID: {}').format(respData['NODE_ID'])
        except requests.exceptions.ConnectionError as err:
            print err
            print 'Retry'
            sleep(10)
            continue
            #sys.exit(1)
        break
    startThreads()   
    
__init()