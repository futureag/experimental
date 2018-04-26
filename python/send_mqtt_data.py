from sys import path
import datetime

path.append('/opt/mvp/config')
from config import organization_guid

def send_sensor_data_via_mqtt(device, mqtt_client, sensor_name, attribute_name, subject_name, value, units, date_time):

   # Need to find the attribute id.  Things may fail here.
   # attribute_id = list(filter(lambda attribute: attribute['name'] == attribute_name, device['attributes']))
   if 'attributes' in device:
      attribute_name_matches = [i for i in device['attributes'] if i['name'] == attribute_name]
      if len(attribute_name_matches) == 0:
         print('Error in send_sensor_data_via_mqtt: Attribute {0} not found in device attribute list'.format(attribute_name))
         return 0
      else:
         if len(attribute_name_matches) > 1:
            print('Error in send_sensor_data_via_mqtt: Attribute {0} found more than one in the device attribute list'.format(attribute_name))
            return 0
   else:
      print('Error in send_sensor_data_via_mqtt: Attributes list is missing from device.')
      return 0

   #If you have gotten this far then the attribute_name has been found. Now look for the attriburte id.
   #
   if 'id' in attribute_name_matches[0]:
      attribute_id = attribute_name_matches[0]['id']
   else:
      print('Error in send_sensor_data_via_mqtt: Attribute id is missing.')
      return 0

   payload_value = '{"sensor":"' + device['name'] + '", '\
                    '"device_id":"'        + device['device_id'] + '", '\
                    '"attribute":"'        + attribute_name + '", '\
                    '"subject":"'          + subject_name + '", '\
                    '"value":"'            + value + '", '\
                    '"units":"'            + units + '", '\
                    '"time":"'             + date_time.isoformat() + '"}'
  
   pub_response = mqtt_client.publish("data/v1/" + organization_guid, payload=payload_value, qos=2) 

   return 1
