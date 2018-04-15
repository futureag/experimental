import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
   print("Connected: " + str(rc))
   # Subscribe to everthing.
   # client.subscribe("#", 2)

def on_message(client, userdata, message):
   print("messaged")

def on_publish(mqttc, obj, mid):
   print("published")

def start_mqtt_client(client):

   # Configure the client
   client.on_connect = on_connect
   client.on_message = on_message

   client.tls_set()

#TODO Need to source credentials from secure enclave.
   client.username_pw_set("ferguman", "")

   client.connect("fop1.urbanspacefarms.com", 8883, 60)

   # Start the MQTT client
   client.loop_forever()
