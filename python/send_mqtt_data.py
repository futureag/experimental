from mvp_configuration import mqtt_sys_id
import datetime

def send_sensor_data_via_mqtt(mqtt_client, sensor_name, data_name, value, units, date_time):

   payload_value = '{"sensor":' + sensor_name + '" "sensor_data":"' + data_name + '" "value":"' + value + '" "units":"' + units + '" "time":"' + date_time.isoformat() + '"}'
  
   pub_response = mqtt_client.publish("data/v1/" + mqtt_sys_id, payload=payload_value, qos=2) 
