from flask import Flask, jsonify
#from DHT11Handler import *
import threading
from datetime import datetime

app = Flask(__name__)

#TODO 
#Create dictionary 

sensorData = {
        'nodeID'    :1,
        'sensorID'  :1,
        'dataType'  :1,
        'timestamp' :1,
        'data'      :1

    }

'''
@app.route('/Temp', methods=['GET'])
def getTemp(): 
    sensorData['data'] = getTemperature()
    sensorData['dataType'] = "Temperature"
    sensorData['timestamp'] = str(datetime.now())
    return jsonify(sensorData)
    #return "Temp => " + str(getTemperature())
'''

@app.route('/test', methods=['GET'])
def getTemp(): 
    return jsonify(sensorData)
    #return "Temp => " + str(getTemperature())

@app.route('/Humidity')
def getHumi(): return "Humidity => " + str(getHumidity())


@app.route('/All')
def getData(): return "Humidity & Temperature => " + str(getAll())


def runRest(): app.run(port = 5005)    
    
