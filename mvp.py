# This module is main program.
#
# Run this program with the following command: python3 mvp.py
#
# It spawns the following threads:
# MQTT Client
# Light Controller
# Sensor Data Logger
# Fan Controller
# Camera Controller
# Website Chart Controller 
#
# It is assumed that mvp.py is located in a directory that contains code and data organized identical to the way
# it is stored in github (https://github.com/ferguman/openag-mvp)
# 
# Tell the python interpretter where to look for various files relative to the current working directory.
import os
import sys

# All the applications python code is located in the python directory.
sys.path.append(os.getcwd() + '/python')
sys.path.append(os.getcwd() + '/python/devices')

# The applications configuration file is located here.
sys.path.append(os.getcwd() + '/config')           

# Ok let's get started!
#
import logging
from logging.handlers import RotatingFileHandler
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

from config import device_name, enable_mqtt, encrypted_mqtt_password

def get_passphrase():

   # If mqtt is enabled in mvp_configuration then ask the user for the passphrase.
   if enable_mqtt == True:
      return getpass.getpass("Enter your passphrase: ")
   else:
      return None

config_file_passphrase = get_passphrase()

# TBD:  Move the logging configuration to a dictionary stored in a configuration file.
# On linux use tail -F (translates as tail --follow=name --retry) to follow the 
# rotating log. tail -f stops following when the log gets rotated out from under it.
#
# This logger currenlty rotates based upon file size. Python also supports timed based 
# rotation.
#
logger = logging.getLogger('mvp')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(os.getcwd() + '/logs/mvp.log', maxBytes=10*1000*1000, backupCount=5)
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(name)s:%(message)s', 
                              datefmt='%Y-%m-%d %I:%M:%S %p %Z')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('############## starting mvp system ##############')

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
      logger.error('Unable to start an MQTT client.')
      exit()
else:
    mqtt_client = None

# Create the light controller 
t2 = threading.Thread(target=start_light_controller, name="light_controller", args=(app_state, ))

# Create the sensor data logger
t3 = threading.Thread(target=start_sensor_data_logger, name="sensor_logger", args=(mqtt_client, app_state))

# Create the fan controller (aka thermostat)
t4 = threading.Thread(target=start_fan_controller, name="fan_controller", args=(app_state, ))

# Create the camera controller
t5 = threading.Thread(target=start_camera_controller, name="camera_controller", args=(app_state, ))

# Create the website chart geneator
t6 = threading.Thread(target=start_web_chart_controller, name="web_chart_controller", args=(app_state,))

# Start threads t2 - t6
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()

print('Enter: (help) to see a list of available commands.')

while True:
   
   try:
      # TBD: Need to sanitize the name to guard against shell attack.
      cmd = input(device_name + ':')
      if cmd == '(help)':
         print('(help) -> display this help message.')
         print('(exit) -> exit this program.')
      elif cmd == '(exit)':
         app_state['stop'] = True
         logger.info('shutting down')
         print('shutting down, please wait a few seconds.')
         #- sleep(2)
         break
      else:
         print('unknown command. Enter: (help) to see a list of available commands.')
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
