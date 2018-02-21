from flask import Flask, jsonify, make_response
import threading
from DHT11Handler import *
from datetime import datetime

app = Flask(__name__)

sensorData = {
        'nodeID'    :"",
        'sensorID'  :"",
        'dataType'  :"",
        'timestamp' :"",
        'data'      :""

    }

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

def runRest(): app.run(port = 5005)    
    
