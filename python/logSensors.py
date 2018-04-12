#Check sensors and log to file
import time
import datetime
from si7021 import *
from logData import logData
from atlasPH import *
from ds18b20 import *
from send_mqtt_data import send_sensor_data_via_mqtt

def start_sensor_data_logger(mqtt_client, mqtt_sys_id):

   si=si7021()

   while True:

      try:
         timestamp = datetime.datetime.utcnow()
         temp = si.getTempC()
         logData("si7021_top", "Success", "temperature", "{:10.1f}".format(temp), '')
         send_sensor_data_via_mqtt(mqtt_client, "air temperature", "Success", "{:+.1f}".format(temp), "celsius", timestamp)
      except Exception as e:
         logData("si7021_top", "Failure", "temperature", '', str(e))

      try:
         humid = si.getHumidity()
         logData("si7021_top", "Success", "humidity", "{:10.1f}".format(humid), '')
      except Exception as e:
         logData("si7921_top", "Failure", "humidity", '', str(e))

      try:
         ph = atlasPH().getPH()
         logData("PH", "Success", "ph", "{:10.2f}".format(ph), '')
      except Exception as e:
         logData("PH", "Failure", "ph", '', str(e))

      try:
         water_temp = ds18b20().getTempC()
         logData("ds18b20_1", "Success", "water temperature", "{:10.1f}".format(water_temp), '')
      except Exception as e:
         logData("ds18b20_1", "Failure", "water temperature", '', str(e))

      # Spit out an MQTT message
                                       

      time.sleep(5)
