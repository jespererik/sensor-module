from flask import Flask, jsonify, make_response, request
import threading
from DHT11Handler import *
from datetime import datetime
import requests

#app = Flask(__name__)

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
    tryFileOpen("/storage/log/errorLog.log")
    logfile = open("/storage/log/errorLog.log", "a")
    logfile.write("Failed to connect to {0}: {1}\n".format(str(url), str(err)))
    logfile.close()

def postTemp():
    tryFileOpen("/storage/nodeID.txt")
    fopen = open("/storage/nodeID.txt", "r")   
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
'''
@app.route('/Temp', methods=['GET'])
def getTemp(): 
    sensorData['data'] = getTemperature()
    sensorData['dataType'] = "Temperature"
    sensorData['timestamp'] = str(datetime.now())
    return jsonify(sensorData)


@app.route('/Humidity', methods=['GET'])
def getHumi(): 
    sensorData['data'] = getHumidity()
    sensorData['dataType'] = "Humidity"
    sensorData['timestamp'] = str(datetime.now())
    return jsonify(sensorData)

@app.route('/Test', methods=['GET'])
def getTest(): 
    return jsonify(sensorData)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
'''
def runRest(): 
    #app.run(port = 5005)    
    postTemp()
