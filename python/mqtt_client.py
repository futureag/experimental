from subprocess import * 
import threading
import paho.mqtt.client
from sys import path
import paho.mqtt.client as mqtt
from datetime import datetime

path.append('/opt/mvp/config')
from config import *

def on_connect(client, userdata, flags, rc):
   #- print("############ MQTT client Connected: #################" + str(rc))
   print('{:%Y-%m-%d %H:%M:%S} MQTT client Connected with return code: {}'.format(datetime.utcnow(), str(rc)))
   # Subscribe to everthing.
   # client.subscribe("#", 2)

def on_message(client, userdata, message):
   print("messaged")

def on_publish(mqttc, obj, mid):
   print("published")

def start_mqtt_client(client, mqtt_password):

   # Configure the client
   client.on_connect = on_connect
   client.on_message = on_message

   client.tls_set()

   client.username_pw_set(mqtt_username, mqtt_password)

   client.connect(mqtt_url, mqtt_port, 60)

   # Start the MQTT client
   client.loop_forever()

# TBD - Need to figure out how to securely keep the config_file_passphrase and also to time it out
# after a configurable period of time.
#
def start_mqtt_client_thread(config_file_passphrase, encrypted_mqtt_password):

   # call open SSL to decrypt the encrypted MQTT password.
   open_ssl_decrypt_command = 'echo "' + encrypted_mqtt_password + '" | openssl enc -d -k "'\
                                 + config_file_passphrase + '" -a -aes-256-cbc'
   
   try:
      #TBD - At some point upgrade to the new Python (3.5 or newer) and use the .run commmand.
      password_decrypt_results = check_output(open_ssl_decrypt_command, shell=True) 
      # print("MQTT password: " + mqtt_password + "\n") 
      mqtt_password = password_decrypt_results.decode("utf-8")[0:-1]
   except CalledProcessError as e:
      print("Execution of openssl failed with return code:{}.\n".format(e.returncode))
      return [False]

   mqtt_client = paho.mqtt.client.Client(mqtt_client_id)

   # Create the MQTT client thread 
   #
   t1 = threading.Thread(target=start_mqtt_client, name="mqtt_client", args=(mqtt_client, mqtt_password))
   
   # Start the MQTT client
   t1.start()
   # TBD - add code here to wait for the mqtt connection to complete before proceeding.

   return [True, mqtt_client, t1]

