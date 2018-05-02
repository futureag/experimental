import sys
import threading
from subprocess import * 
from mqtt_client import start_mqtt_client_thread
from light_controller import start_light_controller
from logSensors import start_sensor_data_logger
from sys import *
import getpass
from adjustThermostat import start_fan_controller
from camera_controller import start_camera_controller

sys.path.append('/opt/mvp/config')
from config import *

def get_passphrase():

   # If mqtt is enabled in mvp_configuration then ask the user for the passphrase.
   if enable_mqtt == True:
      #- aes_passphrase = getpass.getpass("Enter your passphrase: ")
      return getpass.getpass("Enter your passphrase: ")
   else:
      return None


config_file_passphrase = get_passphrase()

# Start the MQTT client thread if so configured.
if enable_mqtt == True:
   result = start_mqtt_client_thread(config_file_passphrase, encrypted_mqtt_password)
   if result[0] == True:
      mqtt_client = result[1]
      t1 = result[2]
   else:
      print('ERROR. Unable to start an MQTT client.')
      exit()

# Start the fan controller

# Start the light controller 
t2 = threading.Thread(target=start_light_controller, name="light_controller", args=(mqtt_client,))

# Start the sensor data logger
t3 = threading.Thread(target=start_sensor_data_logger, name="sensor_logger", args=(mqtt_client,))

# Start the fan controller (aka thermostat)
t4 = threading.Thread(target=start_fan_controller, name="fan_controller", args=(mqtt_client,))

# Start the camera controller
t5 = threading.Thread(target=start_camera_controller, name="camera_controller", args=(mqtt_client,))

# Start the website chart geneator

t2.start()
t3.start()
t4.start()
t5.start()

# Wait till all the threads finish
if enable_mqtt == True:
   t1.join()

t2.join()
t3.join()
t4.join()
t5.join()
