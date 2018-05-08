#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

import RPi.GPIO as GPIO
from logData import logData
from time import sleep 
from datetime import datetime
import sys
from logging import getLogger

sys.path.append('/opt/mvp/config')
from config import light_controller_program, log_light_state_to_local_couchdb, log_light_state_to_local_file

logger = getLogger('light_controller')

def log_lights(state: str):

   log_list = ['{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) , 'Light_Switch',
               'Success', 'light', None, {}.format(state), None, '']

   if log_light_state_to_local_couchdb:
      logDB(**log_list)

   if log_light_state_to_local_file:
      logFile(**log_list)

def setLightOff():

   "Check the time and determine if the lights need to be changed"
   lightPin = 29
   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(lightPin, GPIO.OUT)
   # For the relaly board, use the first line
   # For the Sparkfun PowerSwitch tail (https://www.sparkfun.com/products/10747)
   # Uncomment the second line, and comment out the first
   GPIO.output(lightPin, GPIO.LOW)
   #    GPIO.output(lightPin, GPIO.HIGH)
   logger.info('Turned light off')

   logData("Light_Switch", "Success", "light", None, "Off", None, '')


def setLightOn():

   "Check the time and determine if the lights need to be changed"
   lightPin = 29
   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(lightPin, GPIO.OUT)
   # For the relaly board, use the first line
   # For the Sparkfun PowerSwitch tail (https://www.sparkfun.com/products/10747)
   # Uncomment the second line, and comment out the first    
   GPIO.output(lightPin, GPIO.HIGH)
   #    GPIO.output(lightPin, GPIO.LOW)    
   logger.info('Turned light on')

   logData("Light_Switch", "Success", "light", None, "On", None, '')


def run_controller(light_state, program):

   this_update_time = datetime.now().time()

   # If we've wrapped around midnight then bring the last update time forward.
   # Set times are specified with a resolution of 1 minute so this "bring forward"
   # operation should not skip over any set times.
   # TBD Need to test this peice of code. Also we could skip exit the controller on all
   # calls other than those that cross a minute boundary.
   if this_update_time < light_state['last_update']:
      light_state['last_update'] = datetime.strptime('12:00 AM',  '%I:%M %p').time()

   for x in program:

      set_time = datetime.strptime(x[1], '%I:%M %p').time()

      if light_state['last_update'] <= set_time and this_update_time >= set_time:

         if x[0] == 'on':
            light_cmd = setLightOn
            light_on = True
         else:
            if x[0] == 'off':
               light_cmd = setLightOff
               light_on = False
            else:
               logging.error('ERROR. Illegal value ({}) for light command.'.format(x[0]))
               return {'error':True, 'light_on':light_state['light_on'], 'last_update':this_update_time}

         logger.info('{:%Y-%m-%d %H:%M:%S} Turning light {}.'.format(datetime.now(), x[0])) 
         light_cmd()
         return {'error':False, 'light_on':light_on, 'last_update':this_update_time}

   #At this point you haven't 'fired' on any commands.
   return {'error':False, 'light_on':light_state['light_on'], 'last_update':this_update_time}
 

def start_light_controller(mqtt_client, app_state):

   logger.info('Starting light controller.')

   # light_state
   setLightOff()
   light_state = {'error':False, 'light_on':False, 'last_update':datetime.now().time()}

   while not app_state['stop']:

      light_state = run_controller(light_state, light_controller_program)

      sleep(1)
