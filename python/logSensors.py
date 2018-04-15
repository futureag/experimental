#Check sensors and log to file
import time
import datetime
from si7021 import *
from logData import logData
from atlasPH import *
from ds18b20 import *

def start_sensor_data_logger(mqtt, mqtt_sys_id):

   si=si7021()

   while True:

      try:
         date_time = datetime.datetime.utcnow()
         temp = si.getTempC()

         logData(mqtt, "si7021_top", "Success", "temperature", "{:+.1f}".format(temp), "celsius", date_time, '')

      except Exception as e:
         logData(mqtt, "si7021_top", "Failure", "temperature", '', "celsius", date_time, str(e))

      try:
         humid = si.getHumidity()
         logData(mqtt, "si7021_top", "Success", "humidity", "{:+.1f}".format(humid), "percentage", date_time,  '')
      except Exception as e:
         logData(mqtt, "si7921_top", "Failure", "humidity", '', "percentage", date_time, str(e))

      try:
         ph = atlasPH().getPH()
         logData(mqtt, "PH", "Success", "ph", "{:+.2f}".format(ph), "scalar", date_time, '')
      except Exception as e:
         logData(mqtt, "PH", "Failure", "ph", '', "scalar", date_time, str(e))

      try:
         water_temp = ds18b20().getTempC()
         logData(mqtt, "ds18b20_1", "Success", "water temperature", "{:+.1f}".format(water_temp), "celsius", date_time, '')
      except Exception as e:
         logData(mqtt, "ds18b20_1", "Failure", "water temperature", '', "celsius", date_time, str(e))
      
      time.sleep(5)
