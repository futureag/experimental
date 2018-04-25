from sys import path
import paho.mqtt.client as mqtt

path.append('/opt/mvp/config')
from config import *

def on_connect(client, userdata, flags, rc):
   print("############ MQTT client Connected: #################" + str(rc))
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
