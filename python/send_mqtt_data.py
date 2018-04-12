from mvp_configuration import mqtt_sys_id
import datetime

def send_sensor_data_via_mqtt(mqtt_client, measurement_name, status, value, units, mt):

   payload_value = '{"name":"' + measurement_name +  '" "status":"' + status + '" "value":"' + value + '" "units":"' + units + '" "time":"' + mt.isoformat() + '"}'
  
   pub_response = mqtt_client.publish("sensor_reading/" + mqtt_sys_id, payload=payload_value, qos=2) 
