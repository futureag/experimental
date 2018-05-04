# MVP Configuration

# This file is expected to be placed somewhere such as %APP_DATA%/mvp/config (on Windows) or
# or /opt/mvp/config (on Linux).  In order to generate this file for a new installation do the 
# following 2 things:
# 1. Edit config_file_location.py and set the value of TBD to the path where the config file
#    will be stored.
# 2. Run TBD to generate the config file. this program will ask for certain information and then
#    create and store the file in the place that you designate.
#

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

# ######## Fan Controller #########
# Speciy the target max chamber air temperature in Celsius.
# The fan will be turned on when the temperature exceeds this value.
#
max_air_temperature = 30

# ######## Camera Controller #########
# You must include a slash after the last subdirectory - TBD: clean this up. 
image_directory = '/home/pi/openag-mvp/pictures/'
camera_controller_program = ('hourly', 0)
copy_current_image = True
current_image_copy_location = '/home/pi/MVP/web/image.jpg'

# ######## Device Ids ############
# Use the settings below to define the system composition. Once things are working then
# figure out a better way to configure systems.
#
#
#
organization_guid = ""

system = {'name':'',
          'device_id':''}

device_1 = {'name':'si7021',
            'device_id':'',
            'subject_location':'chamber',
            'subject_location_id':'',
            'attributes':[{'name':'temperature', 'id':'b794687a-9970-4d12-a890-3aba98332ab8'},
                          {'name':'humidity', 'id':'3c36bae6-ec85-4898-9ab4-187dcd8c91f2'}]}

device_2 = {'name':'ds18b20',
            'device_id':'',
            'subject_location':'resevoir',
            'subject_location_id':'',
            'attributes': [{'name':"temperature", 'id':'b794687a-9970-4d12-a890-3aba98332ab8'}]}

system_composition = [system, device_1, device_2]

# ######## Local Data Logging ########
# Specify the sensor sampling interval in seconds.
local_data_logger_sample_interval = 5

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

# Need a way to dynamically create this setting when the user is setting up their MVP
chart_list = (temp_chart, humidity_chart, water_temp_chart)
