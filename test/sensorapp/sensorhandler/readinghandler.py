import random

ARRAY_SIZE = 10

def __mean(iterable):
    return sum(iterable) / len(iterable)

def __process_DHT11(pins, sensor_index = None):
    reading_array = [] * ARRAY_SIZE
    for i in range(0, 10):
        reading_array[i] = "%.2f" % random.uniform(-15, 40)
    return reading_array


def get_reading(sensor_id, reading_type, pins):
    """[Fetches the readings of a sensor]
    
    Arguments:
        sensor_id {[string]} -- [The name of the sensor]
        reading_type {[type]} -- [The type that is to be gathered]
        pin1 {[type]} -- [description]
        pin2 {[type]} -- [description]
    
    Returns:
        [array or bool] --  if the sensor outputs values such as temperature it will return the mean
                            of 10 values gathered and if its something static like if something is on
                            or of it will return a bool.
    """

    if sensor_id == "DHT11":
        if reading_type == "temperature":
            return __mean(__process_DHT11(pins, 1))
        elif reading_type == "humidity":
            return __mean(__process_DHT11(pins, 0))

    
