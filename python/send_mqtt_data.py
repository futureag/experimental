from mvp_configuration import mqtt_sys_id
import datetime

def send_sensor_data_via_mqtt(mqtt_client, measurement_name, value, units, date_time):

   payload_value = '{"name":"' + measurement_name + '" "value":"' + value + '" "units":"' + units + '" "time":"' + date_time.isoformat() + '"}'
  
   pub_response = mqtt_client.publish("data/" + mqtt_sys_id, payload=payload_value, qos=2) 
