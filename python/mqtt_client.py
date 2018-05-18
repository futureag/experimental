from subprocess import * 
import threading
import paho.mqtt.client
from sys import path
import paho.mqtt.client as mqtt
from datetime import datetime
from logging import getLogger

from config import *

logger = getLogger('mvp' + '.' + __name__)

def on_connect(client, userdata, flags, rc):
   #- print('{:%Y-%m-%d %H:%M:%S} MQTT client Connected with return code: {}'.format(datetime.utcnow(), str(rc)))
   # TBD instead of displaying the return code (e.g. 0) display the meaning of the code (e.g. success).
   logger.info('MQTT client Connected with return code: {}'.format(str(rc)))

def on_message(client, userdata, message):
   logger.error('MQTT message received. This version of the mvp code does not support incoming MQTT messages.')

def on_publish(mqttc, obj, mid):
   logger.debug('MQTT message published, mid={}'.format(mid))

def on_disconnect(mqtt, userdata, rc):
   logger.warning('MQTT Disconnected.')

#- def on_log(client, userdata, level, buf):
#-   print('WARNING: MQTT log at {:%Y-%m-%d %H:%M:%S}:{}'.format(datetime.now(), buf))


# TBD - Need to figure out how to time it out
# after a configurable period of time.
#
def start_mqtt_client(config_file_passphrase, encrypted_mqtt_password):

   # call open SSL to decrypt the encrypted MQTT password.
   open_ssl_decrypt_command = 'echo "' + encrypted_mqtt_password + '" | openssl enc -d -k "'\
                                 + config_file_passphrase + '" -a -aes-256-cbc'
   
   try:
      #TBD - At some point upgrade to the new Python (3.5 or newer) and use the .run commmand.
      password_decrypt_results = check_output(open_ssl_decrypt_command, shell=True) 
      # print("MQTT password: " + mqtt_password + "\n") 
      mqtt_password = password_decrypt_results.decode("utf-8")[0:-1]
   except CalledProcessError as e:
      logger.error('Execution of openssl failed with return code:{}.'.format(e.returncode))
      return [False]

   mqtt_client = paho.mqtt.client.Client(mqtt_client_id)

   # Configure the client callback functions
   mqtt_client.on_connect = on_connect
   mqtt_client.on_message = on_message
   mqtt_client.on_publish = on_publish
   mqtt_client.on_disconnect = on_disconnect
   #- mqtt_client.on_log = on_log

   mqtt_client.enable_logger(logger)

   mqtt_client.tls_set()

   mqtt_client.username_pw_set(mqtt_username, mqtt_password)

   mqtt_client.connect(mqtt_url, mqtt_port, 60)

   # Start the MQTT client
   mqtt_client.loop_start()

   # TBD - add code here to wait for the mqtt connection to complete before proceeding.

   return [True, mqtt_client]
