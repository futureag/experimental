#Check sensors and log to file
from si7021 import *
from atlasPH import * 
from atlasEC import *
from logData import logData

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
    ec = atlasEC().getEC()
    logData("EC", "Success", "ec", "{:10.2f}".format(ec), '')
except Exception as e:
        logData("EC", "Failure", "ec", '', str(e))
