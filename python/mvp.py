import logging
import sys
import threading
from subprocess import * 
from mqtt_client import start_mqtt_client
from light_controller import start_light_controller
from logSensors import start_sensor_data_logger
from sys import *
import getpass
from adjustThermostat import start_fan_controller
from camera_controller import start_camera_controller
from web_chart_controller import start_web_chart_controller

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

# Move the logging configuration to a dictionary stored in a configuration file.
logging.basicConfig(filename='mvp.log', filemode='w', level=logging.INFO, format='%(asctime)s %(name)s  %(levelname)s %(message)s')

app_state = {'stop': False}

# Create and start the MQTT client thread if so configured.
# Note that the paho mqtt client has the ability to spawn it's own thread.
# Communication with this thread is done via the the mqtt_client object.
if enable_mqtt == True:
   result = start_mqtt_client(config_file_passphrase, encrypted_mqtt_password)
   if result[0] == True:
      mqtt_client = result[1]
   else:
      #- print('ERROR. Unable to start an MQTT client.')
      logging.error('Unable to start an MQTT client.')
      exit()

# Create the light controller 
t2 = threading.Thread(target=start_light_controller, name="light_controller", args=(mqtt_client, app_state))

# Create the sensor data logger
t3 = threading.Thread(target=start_sensor_data_logger, name="sensor_logger", args=(mqtt_client, app_state))

# Create the fan controller (aka thermostat)
t4 = threading.Thread(target=start_fan_controller, name="fan_controller", args=(mqtt_client, app_state))

# Create the camera controller
t5 = threading.Thread(target=start_camera_controller, name="camera_controller", args=(mqtt_client, app_state))

# Create the website chart geneator
t6 = threading.Thread(target=start_web_chart_controller, name="web_chart_controller", args=(app_state,))

# Start threads t2 - t6
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()

while True:
   try:
      pass
   except:
      app_state['stop'] = True
      break

# Wait for threads to complete.
#
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
