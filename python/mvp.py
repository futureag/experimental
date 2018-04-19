import paho.mqtt.client
import threading
from mqtt_client import start_mqtt_client 
from logSensors import start_sensor_data_logger
from mvp_configuration import *
from subprocess import * 
from sys import *
import getpass

# If mqtt is enabled in mvp_configuration then ask the user for the passphrase.
# Note: Need to create a python application that allows the user to add secure
# configuration information to mvp_configuration.py
#
if enable_mqtt == True:

   aes_passphrase = getpass.getpass("Enter your passphrase: ")
  
   # call open SSL to decrypt the encrypted password.
   open_ssl_decrypt_command = 'echo "' + encrypted_mqtt_password + '" | openssl enc -d -k "' +  aes_passphrase + '" -a -aes-256-cbc'
   
   try:
      #TBD - At some point upgrade to the new Python (3.5 or newer) and use the .run commmand.
      password_decrypt_results = check_output(open_ssl_decrypt_command, shell=True) 
      mqtt_password = password_decrypt_results.decode("utf-8")[0:-1]
      # print("MQTT password: " + mqtt_password + "\n") 
   except CalledProcessError as e:
      print("Execution of openssl failed with return code:{}.\n".format(e.returncode))
      exit()
         
   mqtt_client = paho.mqtt.client.Client(mqtt_client_id)

   # Create the MQTT client thread 
   #
   t1 = threading.Thread(target=start_mqtt_client, name="mqtt_client", args=(mqtt_client, mqtt_password))
   
   # Start the MQTT client
   t1.start()
   # TBD - add code here to wait for the mqtt connection to complete before proceeding.
else:
   mqtt_client = None

# Start the fan controller

# Start the light controller 

# Start the sensor data logger
t2 = threading.Thread(target=start_sensor_data_logger, name="sensor_logger", args=(mqtt_client, mqtt_sys_id))

# Start the camera controller

# Start the website chart geneator


t2.start()

# Wait till all the threads finish
if enable_mqtt == True:
   t1.join()

t2.join()
