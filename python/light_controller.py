import RPi.GPIO as GPIO
from logData import logData
from time import sleep 
from datetime import datetime
import sys

sys.path.append('/opt/mvp/config')
from config import light_controller_program

#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

def setLightOff():
    "Check the time and determine if the lights need to be changed"
    lightPin = 29
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    print ("Turn lights Off")
    GPIO.setup(lightPin, GPIO.OUT)
    # For the relaly board, use the first line
    # For the Sparkfun PowerSwitch tail (https://www.sparkfun.com/products/10747)
    # Uncomment the second line, and comment out the first
    GPIO.output(lightPin, GPIO.LOW)
    #    GPIO.output(lightPin, GPIO.HIGH)
    logData("Light_Switch", "Success", "light", None, "Off", None, '')

def setLightOn():
    "Check the time and determine if the lights need to be changed"
    lightPin = 29
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    print ("Turn lights On")
    GPIO.setup(lightPin, GPIO.OUT)
    # For the relaly board, use the first line
    # For the Sparkfun PowerSwitch tail (https://www.sparkfun.com/products/10747)
    # Uncomment the second line, and comment out the first    
    GPIO.output(lightPin, GPIO.HIGH)
    #    GPIO.output(lightPin, GPIO.LOW)    
    logData("LightChange", "Success", "light", None, "On", None, '')

#- # YYYY-MM-DD HH:MM AM/PM -> '%Y-%m-%d %I:%M %p' 
#- light_controller_program = (('on', '2:18 PM'), ('off', '2:19 PM'))

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

      # print(x)
      set_time = datetime.strptime(x[1],  '%I:%M %p').time()
      print('last update time: {}, set time: {}, this update time: {}.'.format(light_state['last_update'], set_time, this_update_time))

      if light_state['last_update'] <= set_time and this_update_time >= set_time:

         if x[0] == 'on':
            light_cmd = setLightOn
            light_on = True
         else:
            if x[0] == 'off':
               light_cmd = setLightOff
               light_on = False
            else:
               print('ERROR. Illegal value ({}) for light command.'.format(x[0]))
               return {'error':True, 'light_on':light_state['light_on'], 'last_update':this_update_time}

         print('{:%Y-%m-%d %H:%M:%S} Turning light {}.'.format(datetime.utcnow(), x[0])) 
         light_cmd()
         return {'error':False, 'light_on':light_on, 'last_update':this_update_time}

   #At this point you haven't 'fired' on any commands.
   return {'error':False, 'light_on':light_state['light_on'], 'last_update':this_update_time}
 

def start_light_controller(mqtt_client):

   # light_state
   setLightOff()
   light_state = {'error':False, 'light_on':False, 'last_update':datetime.now().time()}

   while True:
      print('{:%Y-%m-%d %H:%M:%S} Light Controller Awakened'.format(datetime.utcnow()))

      light_state = run_controller(light_state, light_controller_program)

      sleep(5)
