from itertools import cycle
from time import sleep
import threading
import random

SIZE = 10
indices = cycle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
humidity_array      = [0] * SIZE
temperature_array   = [0] * SIZE


def sensor_data_stream():
   while True:
      i = next(indices)
      humidity = 0
      temp = random.uniform(12.0, 26.0)
      humidity_array[i]    = humidity
      temperature_array[i] = round(temp, 2)
    

def mean(iterable):
       return sum(iterable) / len(iterable)


def get_temperature():
   return mean(temperature_array)


def get_humidity():
   return mean(humidity_array)


def get_all():
   return (mean(temperature_array), mean(humidity_array))


'''if __name__ == "__main__":
 
    my_thread = threading.Thread(target = sensor_data_stream)
    my_thread.start()
'''
