from RestfulNode  import *
#from DHT11Handler import *
import json
import threading
import requests
import sys

DEBUG = sys.argv[1]

nodeInfo = {
   'NODE_ID': '',
   'NODE_IP': '192.168.0.1',
   'NODE_PORT': '5005', 
}

def startThreads():
   if DEBUG: print 'ENTER => startThreads()'
   restThread = threading.Thread(target = runRest)
   #DHT11Thread = threading.Thread(target = DHT11DataStream)
   
   restThread.start()
   #DHT11Thread.start()
   if DEBUG: print 'EXIT => startThreads()'

def __init():
   if DEBUG: print 'ENTER => __Init()'
   url = 'http://127.0.0.1:5000/init'

   response = requests.post(url, json=nodeInfo)
   if response.ok:
      print 'Server Init Complete'
      respData = json.loads(response.content)
      print('Aquired NODE_ID: {}').format(respData['NODE_ID'])

   else: 
      print 'Server Init Failed'


   startThreads()
   if DEBUG: print 'EXIT => __Init()'
   

__init()