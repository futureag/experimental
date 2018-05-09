from sys import path
from datetime import tzinfo, datetime
import requests
import json
from logging import getLogger

#- path.append('/opt/mvp/config')
from config import log_data_to_local_couchdb, log_data_to_local_file

logger = getLogger('mvp.' + __name__)

def need_to_log_locally():
   return log_data_to_local_couchdb or log_data_to_local_file


# Log data to couchdb and/or file or neither.
#
def logData(sensor_name, status, attribute, subject, value, units, comment):

   # Need to factor out the next call.    
   timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())

   if log_data_to_local_file == True:
      logFile(timestamp, sensor_name, status, attribute, value, comment)

   if log_data_to_local_couchdb == True:
      logDB(timestamp, sensor_name, status, attribute, value, comment)


def logFile(timestamp, name, status, attribute, value, comment):
    f = open('/home/pi/MVP/data/data.txt', 'a')
    s = name + ", " + status + ", " + attribute + ", " + value + "," + comment
    logger.info('file write: {}'.format(s))
    #- print(s)
    f.write(s + "\n")
    f.close()


def logDB(timestamp, name, status, attribute, value, comment):

    s = name + ", " + status + ", " + attribute + ", " + value + "," + comment
    logger.info('couchd db write: {}'.format(s))

    log_record = {'timestamp' : timestamp,
            'name' : name,
            'status' : status,
            'attribute' : attribute,
            'value' : value,
            'comment' : comment}
    json_data = json.dumps(log_record)
    #- print(json.dumps(log_record, indent=4, sort_keys=True))
    headers = {'content-type': 'application/json'}
    r = requests.post('http://localhost:5984/mvp_sensor_data', data = json_data, headers=headers)
    #- print(r.json())
