#Check sensors and log to file
from sys import path
import time
import datetime
#- from si7021 import *
from logData import logData, need_to_log_locally
#- from atlasPH import *
#- from ds18b20 import *
from send_mqtt_data import send_sensor_data_via_mqtt
from logging import getLogger

from config import data_logger_sample_interval, logging_devices, log_data_to_local_file,\
                   log_data_to_local_couchdb, log_data_via_mqtt

logger = getLogger('mvp.' + __name__)

# Set state so that a sample is taken on startup.
#
state = {'next_sample_time':datetime.datetime.now().time(), 'sample_taken':False}

def time_to_sample():

   if data_logger_sample_interval <= 0 or data_logger_sample_interval > 86400:
      logger.error('The data_logger_sample_interval must be '
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

def start_sensor_data_logger(mqtt_client, app_state):

   logger.info('Starting sensor controller.')

   while not app_state['stop']:

      if time_to_sample():

         logger.debug('Need to log locally: {}, mqtt logging enabled: {}'\
                      .format(need_to_log_locally(), log_data_via_mqtt))

         if need_to_log_locally() == True or log_data_via_mqtt == True:
            logger.info('Logging sensor readings')
            for x in logging_devices:
               for y in x['attributes']:
                  logger.debug('Logging sensor reading for sensor {} and attribute {}'.format(x['name'], y['name']))                  
                  #Get the current value
                  date_time = datetime.datetime.utcnow()
                  attribute_val = x['instance'].Get(y['name'])

                  #Log the value locally
                  logData(x['name'], "Success", y['name'],\
                          y['subject'], "{:+.1f}".format(attribute_val), y['units'], '')

                  #Log the value remotely.
                  if log_data_via_mqtt:
                     send_sensor_data_via_mqtt(x, mqtt_client, x['name'], y['name'], y['subject'], 
                                               '{:+.1f}'.format(attribute_val), y['units'], date_time)
         else:
            logger.info('skipping sensor logging because no logging is turned off')

      time.sleep(1)
