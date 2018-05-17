from ConfigParser import RawConfigParser

"""
Example structure of the config file

#General information about the node 
[NODE]
NAME = RaspberryPi3
SENSORS  = DHT11-Temperature,DHT11-Humidity
LOCATION = Pannrum

#Defines the IP and port the server is hosted on
[NETWORK]
SERVER_IP = 192.168.0.121
SERVER_PORT = 3000

#Defines which pins a specific sensor is connected to
#The following two fields are bound to the name you give the sensors under the [NODE] tag
[SENSOR_PINS]
DHT11-Temperature = 11,4
DHT11-Humidity = 11,4

#Defines which types a specifik sensor supports
[READING_TYPES]
DHT11-Temperature = temperature
DHT11-Humidity = humidity

[AUTHORIZATION]
username = test
password = python
"""


def make_config_file():

    config_init = RawConfigParser()

    config_init.read("shared/node.conf")

    config_init.add_section("NODE")
    config_init.add_section("NETWORK")
    config_init.add_section("SENSOR_PINS")
    config_init.add_section("READING_TYPES")
    config_init.add_section("AUTHORIZATION")

    return config_init

def main():
    sensor_pins = []
    reading_types = []

    config = make_config_file()

    print "Welcome to the initial configuration of your sensor network"
    node_name = raw_input("Enter the name you wish to use for the sensor node: ")
    sensor_names = raw_input("Enter the names of the sensors you have connected: ")
    node_location = raw_input("Enter the symbolic/physical location of your node: ")

    server_ip = raw_input("Enter the ip your server module with be located at: ")
    server_port = raw_input("Enter the port your server module will be located at:")

    for sensor in sensor_names.split(","):
        sensor_pins.append(raw_input("Enter the GPIO pins for {}:".format(sensor)))
        reading_types.append(raw_input("Enter the type of reading for {}:".format(sensor)))
    
    username = raw_input("Enter the username used for authorization to the server:")
    password = raw_input("Enter the password used for authorization to the server:")


    print "Generating config file with fields and values:"
    print "[NODE] NAME = {}".format(node_name)
    print "[NODE] SENSORS = {}".format(sensor_names)
    print "[NODE] LOCATION = {}".format(node_location)

    print "[NETWORK] SERVER_IP = {}".format(server_ip)
    print "[NETWORK] SERVER PORT = {}".format(server_port)

    for sensor, pins, reading_type in zip(sensor_names.split(","), sensor_pins, reading_types):
        print "[SENSOR_PINS] {} = {}".format(sensor, pins)
        print "[READING_TYPES] {} = {}".format(sensor, reading_type)

    print "[AUTHORIZATION] USERNAME = {}".format(username)
    print "[AUTHORIZATION] PASSWORD = {}".format(password)

    config.set("NODE", "NAME", node_name)
    config.set("NODE", "SENSORS", sensor_names)
    config.set("NODE", "LOCATION", node_location)

    config.set("NETWORK", "SERVER_IP", server_ip)
    config.set("NETWORK", "SERVER_PORT", server_port)

    for sensor, pins, reading_type in zip(sensor_names.split(","), sensor_pins, reading_types):
        config.set("SENSOR_PINS", sensor, pins)
        config.set("READING_TYPES", sensor, reading_type)
    
    config.set("AUTHORIZATION", "USERNAME", username)
    config.set("AUTHORIZATION", "PASSWORD", password)

    with open("shared/node.conf", "w") as config_file:
        config.write(config_file)


if __name__ == "__main__": 
    main()
