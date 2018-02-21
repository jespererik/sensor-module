from itertools import cycle
from time import sleep
import threading
import Adafruit_DHT

SIZE = 10
indices = cycle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
humidity_array      = [0] * SIZE
temperature_array   = [0] * SIZE

def mean(iterable):
   return sum(iterable) / len(iterable)

def DHT11DataStream():
   while True:
      i = next(indices)
      humidity, temp = Adafruit_DHT.read_retry(11, 4)
      humidity_array[i]    = humidity
      temperature_array[i] = temp

def getTemperature():
   return mean(temperature_array)

def getHumidity():
   return mean(humidity_array)

def getAll():
   return (mean(temperature_array), mean(humidity_array))


if __name__ == "__main__":
 
    myThread = threading.Thread(target = DHT11DataStream)
    myThread.start()

