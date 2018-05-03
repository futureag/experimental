"""
# Render the data for the website
#*/10 * * * * $MVP_SCRIPTS/render.sh >> $CRON_LOG 2>&1
"""

from subprocess import check_call, CalledProcessError
from datetime import datetime
from time import sleep, time
from sys import path
from generate_chart import generate_chart

path.append('/opt/mvp/config')
from config import charting_interval, chart_output_folder, couchdb_location_url, chart_list


def start_web_chart_controller():

   # Set the intial timestamp to 0 thus forcing a web chart generation at start up.
   state = {'last_charting_ts':0, 'last_chart_generation_date':None}

   while True:

      this_ts = time()

      if (this_ts - state['last_charting_ts'])/60 > charting_interval:

         # Generate the charts
         # Figure out how the script directory is getting put in the path. Or in other words
         # how does the system find this command file.
         # Need to make location of the render.sh script a config file setting.
         #- charting_shell_command = '~/openag-mvp/scripts/render.sh'

         try:
            #TBD - At some point upgrade to the new Python (3.5 or newer) and use the .run commmand.
            #- charting_results = check_call(charting_shell_command, shell=True)

            for chart_info in chart_list:

               generate_chart(couchdb_location_url, chart_output_folder, chart_info)
               #-getTempChart('/home/pi/MVP/web/temp_chart.svg')

            state['last_charting_ts'] = this_ts
            state['last_chart_generation_date'] = datetime.now()

            print('{:%Y-%m-%d %H:%M:%S} Web Chart Generator: created charts at {:%Y-%m-%d %H:%M:%S}'.format(datetime.now(),\
                  state['last_chart_generation_date']))

         except CalledProcessError as e:
            print('ERROR. render.sh call failed with the following results:')
            #print(charting_results)

      else:
         print('{:%Y-%m-%d %H:%M:%S} Web Chart Generator: last charts generated at {:%Y-%m-%d %H:%M:%S}'.format(datetime.now(),\
                state['last_chart_generation_date']))

      sleep(5)
