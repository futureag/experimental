import paho.mqtt.client
import threading
from mqtt_client import start_mqtt_client 
from logSensors import start_sensor_data_logger
from mvp_configuration import *

# if mqtt is enabled in mvp_configuration then ask the user for the passphrase and load the 
# mqtt credentials from secure_configuration.py
# Note: Need to create a python application that allows the user to add configuration
#       information to secure_configuration.py:w


# Setup global variables.
#
mqtt_client = paho.mqtt.client.Client(mqtt_client_id)

# Create the MQTT client thread 
#
t1 = threading.Thread(target=start_mqtt_client, name="mqtt_client", args=(mqtt_client, ))

# TBD - add code here to wait for the mqtt connection to complete before proceeding.

# Start the fan controller

# Start the light controller 

# Start the sensor data logger
t2 = threading.Thread(target=start_sensor_data_logger, name="sensor_logger", args=(mqtt_client, mqtt_sys_id))

# Start the camera controller

# Start the website chart geneator

# Get em up Legalos!
t1.start()
t2.start()

# Wait till all the threads finish
t1.join()
t2.join()
