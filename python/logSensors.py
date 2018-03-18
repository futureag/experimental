#Check sensors and log to file
from si7021 import *
from logData import logData
from atlasPH import *
from ds18b20 import *

si=si7021()

try:
    temp = si.getTempC()
    logData("si7921_top", "Success", "temperature", "{:10.1f}".format(temp), '')
except Exception as e:
        logData("si7921_top", "Failure", "temperature", '', str(e))

try:
    humid = si.getHumidity()
    logData("si7021_top", "Success", "humidity", "{:10.1f}".format(humid), '')
except Exception as e:
        logData("si7921_top", "Failure", "humidity", '', str(e))

try:
    ph = atlasPH().getPH()
    logData("PH", "Success", "ph", "{:10.2f}".format(ph), '')
except Exception as e:
        logData("PH", "Failure", "ph", '', str(e))

try:
    water_temp = ds18b20().getTempC()
    logData("ds18b20_1", "Success", "water temperature", "{:10.1f}".format(water_temp), '')
except Exception as e:
        logData("ds18b20_1", "Failure", "water temperature", '', str(e))
