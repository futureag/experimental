# Based upon code originally witten by Howard Webb on 7/25/2017.
# Fan actuator controlled by thermometer

from thermostat import adjustThermostat
# TBD - Factor out the reference to the si7021. The code should get it via the configuration file device list.
from devices.si7021 import *
from logData import logData
from time import sleep
from datetime import datetime
import sys
from logging import getLogger

from config import max_air_temperature 

logger = getLogger('mvp.' + __name__)

def get_target_temp():
   return max_air_temperature


# TBD: Need to add an initializer that turns the fan off when the system powers up or reads it's state and updates the
# the thermostat state with it.
#
def start_fan_controller(app_state): 

   logger.info('starting fan controller')

   thermostat_state = {'fan_on':False, 'target_temp':None}

   while not app_state['stop']:

      #update target temp
      thermostat_state['target_temp'] = get_target_temp() 

      try:
          si = si7021()
          current_temp = si.getTempC()
          thermostat_state = adjustThermostat(thermostat_state, current_temp)  

      except IOError as e:
          logger.error('Failure to get temperature, no sensor found; check pins and sensor')

      sleep(1)
