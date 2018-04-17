import paho.mqtt.client as mqtt

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

#TODO  need to open secure_configuration.py, ask the user for the passphrase and then get the mqtt connection info.
#
   client.username_pw_set("ferguman", mqtt_password)

   client.connect("fop1.urbanspacefarms.com", 8883, 60)

   # Start the MQTT client
   client.loop_forever()
