from flask import Flask, jsonify
import threading
from datetime import datetime

app = Flask(__name__)

sensorData = {
        'nodeID'    :1,
        'sensorID'  :1,
        'dataType'  :1,
        'timestamp' :1,
        'data'      :1

    }

@app.route('/Temp', methods=['GET'])
def getTemp(): 
    sensorData['data'] = getTemperature()
    sensorData['dataType'] = "Temperature"
    sensorData['timestamp'] = str(datetime.now())
    return jsonify(sensorData)


@app.route('/Humidity', methods=['GET'])
def getHumi(): 
    sensorData['data'] = getTemperature()
    sensorData['dataType'] = "Humidity"
    sensorData['timestamp'] = str(datetime.now())
    return jsonify(sensorData)

@app.route('/test', methods=['GET'])
def getTemp(): 
    return jsonify(sensorData)

def runRest(): app.run(port = 5005)    
    
