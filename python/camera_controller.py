from datetime import datetime
from time import sleep
from subprocess import check_call, CalledProcessError
from sys import path
from shutil import copyfile

path.append('/opt/mvp/config')
from config import image_directory, camera_controller_program, copy_current_image, current_image_copy_location

def is_picture_minute(this_instance):

   if camera_controller_program[0] == 'hourly':
      if this_instance.time().minute == camera_controller_program[1]:
         return True
     
   return False


def start_camera_controller(mqtt_client):

   #- this_hour = datetime.now().time().hour
   #- if  this_hour == 0:
   #-    initial_hour = 23
   #- else:
   #-    initial_hour = this_hour - 1

   state = {'hour_of_last_picture':None, 'startup':True}

   while True:

      current_state = state

      this_instance = datetime.now() 

      if state['startup'] == True or \
         ((state['hour_of_last_picture'] != this_instance.time().hour) and is_picture_minute(this_instance)):

         #if state['hour_of_last_picture'] != this_instance.time().hour:

         file_name = '{:%Y%m%d_%H_%M_%S}.jpg'.format(datetime.utcnow())
         file_location = '{}{}'.format(image_directory, file_name) 

         camera_shell_command = 'fswebcam -r 1280x720 --no-banner {}'.format(file_location)

         try:
            #TBD - At some point upgrade to the new Python (3.5 or newer) and use the .run commmand.
            # Take the picture
            # Figure out if you can suppress fswebcam's output or take the picture using native python code.
            picture_results = check_call(camera_shell_command, shell=True)

            print('{:%Y-%m-%d %H:%M:%S} Camera Controller: Created image file at {}'.format(\
                  datetime.now(), file_location))

            # Copy the picture to the web directory
            if copy_current_image == True:
               copyfile(file_location, current_image_copy_location)
               print('{:%Y-%m-%d %H:%M:%S} Camera Controller: Copied latest image file to {}'.format(\
                     datetime.now(), current_image_copy_location))

            # Update your current state
            state['hour_of_last_picture'] = this_instance.time().hour
            state['startup'] = False

         except CalledProcessError as e:
            print('ERROR. fswebcam call failed with the following results:')
            print(picture_results)

      #- print('{:%Y-%m-%d %H:%M:%S} Camera Controller: '.format(datetime.now())
      #-       + 'current hour: {}, '.format(this_instance.time().hour) 
      #-      + 'last picture taken during hour: {}'.format(current_state['hour_of_last_picture']))

      sleep(5)  
