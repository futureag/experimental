import paho.mqtt.client
import threading
from mqtt_client import start_mqtt_client 
from logSensors import start_sensor_data_logger

# Setup global variables.
#
# Need a UUID value for this publishing client.  Will need to store this in some sort of local store.
#
mqtt_client_id = "germ"
mqtt_client = paho.mqtt.client.Client(mqtt_client_id)

# Create the MQTT client thread 
#
t1 = threading.Thread(target=start_mqtt_client, name="mqtt_client", args=(mqtt_client,))

# TBD - add code here to wait for the mqtt connection to complete before proceeding.

# Start the fan controller

# Start the light controller 

# Start the sensor data logger
t2 = threading.Thread(target=start_sensor_data_logger, name="sensor_logger", args=(mqtt_client,))

# Start the camera controller

# Start the website chart geneator

# Get em up Legalos!
t1.start()
t2.start()

# Wait till all the threads finish
t1.join()
t2.join()
