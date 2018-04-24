# MVP Configuration

# MQTT Settings
enable_mqtt = True
mqtt_publish_sensor_readings = True 

# If you are going to send data to an MVP cloud then ask your MVP cloud provider
# to provide the following two ids which are uuid's:
mqtt_client_id = ""

# TBD - need to rename mqtt_sys_id to system_id.  This parameter is not specific to mqtt.
mqtt_sys_id = ""

# Note that the MVP only supports TLS (aka SSL) communication to the MQTT broker .  If your broker
# does not support HTTPS then it can't be used with the MVP.
#
mqtt_url = ""
mqtt_port = 

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
