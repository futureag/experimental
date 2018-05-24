import RPi.GPIO as GPIO
from datetime import datetime
from logging import getLogger

from python.logData import logData
#- from saveGlobals import setVariable

#thermostat.py
#controlls the exhaust fan, turns it on when temperature is over the target temperature
#Fan is assumed to be wired to Pin 33 (GPIO 13)
#Pin 30 may control a relay or be a transistor switch, assumes HIGH means ON

logger = getLogger('mvp.' + __name__)

def fan_state(on_flag):

   if on_flag == True:
      return 'on'
   if on_flag == False:
      return 'off'

   return 'unknown'

def adjustThermostat(thermostat_state, temp):

    #Turn the fan on or off in relationship to target temperature

    _fanPin = 35
    priorFanOn = thermostat_state['fan_on']
    targetTemp = thermostat_state['target_temp']
    
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    #avoid switching pin state and messing up condition    
    #    GPIO.setup(fanPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #    fanOn = GPIO.input(fanPin)
    
    # TBD - should we add some hysteresous?
    if temp > targetTemp:
        GPIO.setup(_fanPin, GPIO.OUT)
        GPIO.output(_fanPin, GPIO.HIGH)
        currentFanOn = True
    else:
        GPIO.setup(_fanPin, GPIO.OUT)
        GPIO.output(_fanPin, GPIO.LOW)    
        currentFanOn = False

    # if the fan state has change then log a message. 
    if thermostat_state['fan_on'] != currentFanOn: 
       logger.info('Target Temp {}, Current Temp {:.2f}, fan was {}, fan now {}'.format(\
                   thermostat_state['target_temp'], temp,\
                   fan_state(thermostat_state['fan_on']), fan_state(currentFanOn)))
       logData('fan', 'Success', 'state', 'fan', '{}'.format(fan_state(currentFanOn), '', ''))

    thermostate_state['fan_on'] = currentFanOn

    #- return currentFanOn
