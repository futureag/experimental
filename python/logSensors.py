#Check sensors and log to file
from sys import path
import time
import datetime
from si7021 import *
from logData import logData
from atlasPH import *
from ds18b20 import *
from send_mqtt_data import send_sensor_data_via_mqtt

path.append('/opt/mvp/config')
from config import device_1, device_2, data_logger_sample_interval

# Set state so that a sample is taken on startup.
#
state = {'next_sample_time':datetime.datetime.now().time(), 'sample_taken':False}

def time_to_sample():

   if data_logger_sample_interval <= 0 or data_logger_sample_interval > 86400:
      print('{:%Y-%m-%d %H:%M:%S} ERROR. The data_logger_sample_interval must be '.format(datetime.datetime.now())
            + 'set to a value between 1 and 86400. 86400 seconds is 24 hours.')
      return False

   global state

   if state['next_sample_time'] <= datetime.datetime.now().time() and state['sample_taken'] == False:
      state = {'next_sample_time':(datetime.datetime.now() +\
                                   datetime.timedelta(seconds=data_logger_sample_interval)).time(),
               'sample_taken':False}      
      return True
   else:
      return False

def start_sensor_data_logger(mqtt_client):


   while True:

      if time_to_sample():
      #if local logging enabled or mqtt logging enabled:
      #   for x in device list:
      #      for y in device attribute list:
      #        print(######## sampling log data = take sample
         print('{:%Y-%m-%d %H:%M:%S} ######## taking a sample.'.format(datetime.datetime.now()))
      #         if local loggin enabled:
      #            logData(log data)
      #         if mqtt enabled:
      #            send data via mqtt(log data, mqtt_client)
      #See this reference for calling a method by name: https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string

         si=si7021()

         date_time = datetime.datetime.utcnow()

         try:
            temp = si.getTempC()
            logData("si7021", "Success", "temperature", "air", "{:+.1f}".format(temp), "celsius", '')
            send_sensor_data_via_mqtt(device_1, mqtt_client, "si7021", "temperature", "air", 
                                      "{:+.1f}".format(temp), "celsius", date_time)
         except Exception as e:
            logData("si7021", "Failure", "temperature", "air", '', "celsius", str(e))

         try:
            humid = si.getHumidity()
            logData("si7021", "Success", "humidity", "air", "{:+.1f}".format(humid), 
                    "percentage", '')
            send_sensor_data_via_mqtt(device_1, mqtt_client, "si7021", "humidity", "air", 
                                      "{:+.1f}".format(temp), "percentage", date_time)
         except Exception as e:
            logData("si7021", "Failure", "humidity", "air", '', "percentage", str(e))

         try:
            ph = atlasPH().getPH()
            logData("PH", "Success", "ph", "water", "{:+.2f}".format(ph), "scalar", '')
            send_sensor_data_via_mqtt(device_1, mqtt_client, "PH", "ph", "water", 
                                      "{:+.1f}".format(temp), "none", date_time)
         except Exception as e:
            logData("PH", "Failure", "ph", "water", '', "scalar", str(e))

         try:
            water_temp = ds18b20().getTempC()
            logData("ds18b20", "Success", "temperature", "water", "{:+.1f}".format(water_temp), 
                    "celsius", '')
            send_sensor_data_via_mqtt(device_2, mqtt_client, "ds18b20", "temperature", "water", 
                                      "{:+.1f}".format(temp), "celsius", date_time)
         except Exception as e:
            logData("ds18b20", "Failure", "temperature", "water", '', "celsius", str(e))

      time.sleep(1)
