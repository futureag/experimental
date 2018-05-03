# Based upon code originally witten by Howard Webb on 7/25/2017.
# Fan actuator controlled by thermometer

from thermostat import adjustThermostat
from si7021 import *
from logData import logData
from time import sleep
from datetime import datetime
import sys

sys.path.append('/opt/mvp/config')
from config import max_air_temperature 

def get_target_temp():
   return max_air_temperature


# TBD: Need to add an initializer that turns the fan off when the system powers up or reads it's state and updates the
# the thermostat state with it.
#
def start_fan_controller(mqtt_client):  

  thermostat_state = {'fan_on':False, 'target_temp':None}

  while True:

      #update target temp
      thermostat_state['target_temp'] = get_target_temp() 

      try:
          si=si7021()
          current_temp = si.getTempC()
          thermostat_state = adjustThermostat(thermostat_state, current_temp)  

      except IOError as e:
          print("Failure to get temperature, no sensor found; check pins and sensor")
          logData('si7021-top', 'Failure', 'temperature', 'air', '', 'celsius', str(e))
    
      sleep(5)
