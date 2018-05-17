# MVP Configuration

# This file is expected to be placed somewhere such as %APP_DATA%/mvp/config (on Windows) or
# or /opt/mvp/config (on Linux).  In order to generate this file for a new installation do the 
# following 2 things:
# 1. Edit config_file_location.py and set the value of TBD to the path where the config file
#    will be stored.
# 2. Run TBD to generate the config file. this program will ask for certain information and then
#    create and store the file in the place that you designate.
#

organization_guid = ""

# You can give your device a custom name. The name will used at terminal prompts and other
# places where it seems useful to display the name of this device.  
device_name = 'mvp'

# ########### MQTT Settings #############
enable_mqtt = True
mqtt_publish_sensor_readings = True 

# If you are going to send data to an MVP cloud then the ask your MVP cloud provider
# to provide the following two ids:
mqtt_client_id = ""

# Note that the MVP only supports TLS (aka SSL) communication to the MQTT broker .  If your broker
# does not support HTTPS then it can't be used with the MVP.
#
mqtt_url = ""
mqtt_port = 8883

# MQTT account credentials -> username and password
# The MVP client needs to know the username and password of the MQTT broker to which the client 
# should connect for sending data and receiving commands.  The password is stored here as an
# AES encrypted string.
#
# You will need to know the username and password for your account on the MQTT broker.
# Use the following command in order to encrypt the MQTT password.
# echo "put the password here" | openssl enc -e  -k "put your passphrase here" -a -aes-256-cbc
#
# Remember the passphrase and keep it secure. The mvp system will prompt you for the passphrase
# when it is started and use it to decrypt the MQTT password.
# 
# After you generate the encrypted password then modify the value for "encrypted_mqtt_password"
# to be the value that you generated.
#
mqtt_username = ""
encrypted_mqtt_password = "" 

# ######## Light Controller #########
#
# Specify as many on/off times as you like.  Resolution is 1 minute so all light events
# occur on the minute.  Specify the times relative to the time zone of the system that the
# MVP is running on.
#
light_controller_program = (('on', '2:28 PM'), ('off', '2:29 PM'))
#TBD Need to enable MQTT logging.
log_light_state_vai_mqtt = False
log_light_state_to_local_couchdb = True
log_light_state_to_local_file = True


# ######## Fan Controller #########
# Speciy the target max chamber air temperature in Celsius.
# The fan will be turned on when the temperature exceeds this value.
#
max_air_temperature = 30

# ######## Camera Controller #########
# You must include a slash after the last subdirectory - TBD: clean this up. 
#- image_directory = '/home/pi/openag-mvp/pictures/'
camera_controller_program = ('hourly', 0)
copy_current_image = True
# current_image_copy_location = '/home/pi/MVP/web/image.jpg'

# ######## Device Ids ############
# Use the settings below to define the system composition. Once things are working then
# figure out a better way to configure systems.
#
#
#

from si7021 import si7021
from ds18b20 import ds18b20

system = {'name':'germinator',
          'device_id':'4399c2d8-ed0d-4feb-97fa-eb0dc869bf38'}

device_1 = {'name':'si7021',
            'instance':si7021(),
            'device_id':'c6bc257e-2d18-41f0-b9f4-d0ca1f1224df',
            'subject_location':'chamber',
            'subject_location_id':'c0b1d0dc-66a4-46da-8aec-cc308a3359a1',
            'attributes':[{'name':'temperature', 'subject':'air', 'units': 'celsius',
                           'id':'b794687a-9970-4d12-a890-3aba98332ab8'},
                          {'name':'humidity', 'subject':'air', 'units':'percentage', 
                           'id':'3c36bae6-ec85-4898-9ab4-187dcd8c91f2'}]}

device_2 = {'name':'ds18b20',
            'instance':ds18b20(),
            'device_id':'f4682ae0-601b-402e-ba98-5aa1a46cb2b2',
            'subject_location':'resevoir',
            'subject_location_id':'309e865b-f996-44ba-8893-8d5ac3b2d747',
            'attributes': [{'name':'temperature', 'subject':'air', 'units':'celsius',
                            'id':'b794687a-9970-4d12-a890-3aba98332ab8'}]}


# ######## Data Logging ########
# Specify the sensor sampling interval in seconds.
#
data_logger_sample_interval = 5
logging_devices = (device_1, device_2)

# Specify logging of data (e.g. sensors, actuator settings etc.)
#
log_data_to_local_couchdb = True
log_data_to_local_file = True
log_data_via_mqtt = True


# ######## Web Charting Controller #########
# charting_interval (in minutes) sets the refresh time for the web charts.
# TBD: The chart configuration data accesses device data, so will need
# to create a compiler to create configuration files. 
#
charting_interval = 10
chart_output_folder = '/home/pi/MVP/web/'
couchdb_location_url = 'http://127.0.0.1:5984/mvp_sensor_data/'

temp_chart = {'device':device_1,
              'attribute_index':0,
              'chart_title':'Air Temperature',
              'y_axis_title':'Degrees C',
              'x_axis_title':'Timestamp (hover over to display date)',
              'data_stream_name':'Air Temp.',
              'chart_file_name':'temp_chart.svg'}

humidity_chart = {'device':device_1,
              'attribute_index':1,
              'chart_title':'Humidity',
              'y_axis_title':'Percent',
              'x_axis_title':'Timestamp (hover over to display date)',
              'data_stream_name':'Humidity',
              'chart_file_name':'humidity_chart.svg'}

water_temp_chart = {'device':device_2,
              'attribute_index':0,
              'chart_title':'Water Temperature',
              'y_axis_title':'Degrees C',
              'x_axis_title':'Timestamp (hover over to display date)',
              'data_stream_name':'Water Temp',
              'chart_file_name':'water_temp_chart.svg'}

# TBD: Need a way to dynamically create this setting when the user is setting up their MVP
chart_list = (temp_chart, humidity_chart, water_temp_chart)
