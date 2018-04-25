#Check sensors and log to file
from sys import path
import time
import datetime
from si7021 import *
from logData import logData
from atlasPH import *
from ds18b20 import *

path.append('/opt/mvp/config')
from config import device_1, device_2

def start_sensor_data_logger(mqtt, mqtt_sys_id):

   si=si7021()

   while True:

      try:
         date_time = datetime.datetime.utcnow()
         temp = si.getTempC()
         logData(device_1, mqtt, "si7021_top", "Success", "temperature", "air", "{:+.1f}".format(temp), "celsius", date_time, '')
      except Exception as e:
         logData(device_1, mqtt, "si7021_top", "Failure", "temperature", "air", '', "celsius", date_time, str(e))

      try:
         humid = si.getHumidity()
         logData(device_1, mqtt, "si7021_top", "Success", "humidity", "air", "{:+.1f}".format(humid), "percentage", date_time,  '')
      except Exception as e:
         logData(device_1, mqtt, "si7921_top", "Failure", "humidity", "air", '', "percentage", date_time, str(e))

      try:
         ph = atlasPH().getPH()
         logData(device_1, mqtt, "PH", "Success", "ph", "water", "{:+.2f}".format(ph), "scalar", date_time, '')
      except Exception as e:
         logData(device_1, mqtt, "PH", "Failure", "ph", "water", '', "scalar", date_time, str(e))

      try:
         water_temp = ds18b20().getTempC()
         logData(device_2, mqtt, "ds18b20_1", "Success", "temperature", "water", "{:+.1f}".format(water_temp), "celsius", date_time, '')
      except Exception as e:
         logData(device_2, mqtt, "ds18b20_1", "Failure", "temperature", "water", '', "celsius", date_time, str(e))
      
      time.sleep(5)
