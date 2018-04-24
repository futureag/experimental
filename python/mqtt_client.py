import sys
import paho.mqtt.client as mqtt

sys.path.append('/home/pi/openag-mvp-configuration')
#sys.path.append('~/openag-mvp-configuration/')
from mvp_configuration import *

def on_connect(client, userdata, flags, rc):
   print("Connected: " + str(rc))
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
