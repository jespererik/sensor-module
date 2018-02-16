from flask import Flask
from DHT11Handler import *
import threading


print "init: Begin"
data_thread = threading.Thread(target = DHT11DataStream)
data_thread.start()
app = Flask(__name__)
print "init: End"

@app.route('/Temp')
def getTemp(): return "Temp => " + str(getTemperature())


@app.route('/Humdidity')
def getHumi(): return "Humidity => " + str(getHumidity())


@app.route('/All')
def getData(): return "Humidity & Temperature => " + str(getAll())

if __name__ == '__main__':
    app.run(debug = True, port=5005, hose= "0.0.0.0")
    
