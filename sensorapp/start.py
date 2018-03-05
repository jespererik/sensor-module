import json
import threading
import requests
import sys
from sensorhandler import *
from restfulapi  import *
import time

#Add errorhandling to all functions which have a request to the server
#Where they could get a invalid packet structure response

NODE_CONFIG = {
   'NODE_NAME': '',
   'LOCATION': ''
}

def Try_File_Open(filepath):
    try: 
        open(filepath)
    except IOError:
        print("File does not appear to exist {}".format(filepath))
        sys.exit(1)

def Read_Node_Config():
    Try_File_Open("/sensor-module/shared/sensor.conf")
    with open("/sensor-module/shared/sensor.conf", "r") as conf_file:
        for element in conf_file.readlines():
            key, value = element.strip('\n').split(":")
            NODE_CONFIG[key] = value
    conf_file.close()

def Write_Node_Config(new_key, new_value):
    Try_File_Open("/sensor-module/shared/sensor.conf")
    with open("/sensor-module/shared/sensor.conf", "w") as conf_file:
        for key, value in NODE_CONFIG.iteritems():
            if new_key == key:
                conf_file.write(key + ':' + new_value + '\n')
            else:
                conf_file.write(key + ':' + value + '\n')
    conf_file.close()

def Start_Threads():
    print(NODE_CONFIG["NODE_NAME"])
    restThread = threading.Thread(target = runRest, args = (NODE_CONFIG["NODE_NAME"],))
    DHT11Thread = threading.Thread(target = DHT11DataStream)
    
    restThread.start()
    DHT11Thread.start()


def __init():
    Read_Node_config()
    url = "http://192.168.0.121:5000/init"
    while True:
        try:
            response = requests.post(url, json = NODE_CONFIG)
            response.raise_for_status()
            response_data = json.loads(response.content)
            global NODE_CONFIG = response_data
            print(response_data)
            if (response_data['NODE_NAME'] !=  NODE_CONFIG['NODE_NAME']):
                Write_NODE_CONFIG('NODE_NAME', response_data['NODE_NAME'])
            else:
                pass
            break
        except requests.exceptions.ConnectionError as err:
            time.sleep(10)
            continue
    Start_Threads()   
    
__init()