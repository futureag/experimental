from os import getcwd
from datetime import datetime
from time import sleep
from subprocess import check_call, CalledProcessError
from sys import path, exc_info
from shutil import copyfile
from logging import getLogger

from config import camera_controller_program, copy_current_image 

logger = getLogger('mvp.' + __name__)

def is_picture_minute(this_instant):

   if camera_controller_program[0] == 'hourly':
      if this_instant.time().minute == camera_controller_program[1]:
         return True
     
   return False


def start_camera_controller(app_state):

   logger.info('Starting camera controller.')

   state = {'hour_of_last_picture':None, 'startup':True}

   while not app_state['stop']:

      current_state = state

      this_instant = datetime.now() 

      if state['startup'] == True or \
         ((state['hour_of_last_picture'] != this_instant.time().hour) and is_picture_minute(this_instant)):

         file_name = '{:%Y%m%d_%H_%M_%S}.jpg'.format(datetime.utcnow())
         file_location = '{}{}'.format(getcwd() + '/pictures', file_name) 

         # TBD - Need to figure out where to store fswebcam output. Right now it goes to syslog.  Think
         # about a better way to integrate the logging into the mvp's logging infrastructure.
         camera_shell_command = 'fswebcam -r 1280x720 --no-banner --log syslog {}'.format(file_location)

         try:
            #TBD - At some point upgrade to the new Python (3.5 or newer) and use the .run commmand.
            # Take the picture
            # Figure out if you can suppress fswebcam's output or take the picture using native python code.
            picture_results = check_call(camera_shell_command, shell=True)

            logger.info('Created image file at {}'.format(file_location))
            #- print('{:%Y-%m-%d %H:%M:%S} Camera Controller: Created image file at {}'.format(\
            #-      datetime.now(), file_location))

            # Copy the picture to the web directory
            if copy_current_image == True:
               copyfile(file_location, os.getcwd() + '/web/image.jpg')
               logger.info('Copied latest image file to {}'.format(current_image_copy_location))
               #- print('{:%Y-%m-%d %H:%M:%S} Camera Controller: Copied latest image file to {}'.format(\
               #-      datetime.now(), current_image_copy_location))

            # Update your current state
            state['hour_of_last_picture'] = this_instant.time().hour
            state['startup'] = False

         except CalledProcessError as e:
            logger.error('fswebcam call failed with the following results: {}'.format(exc_info()[0]))
            #- print('ERROR. fswebcam call failed with the following results:')
            #- print(picture_results)

      sleep(1)  
