from datetime import datetime
from time import sleep
from subprocess import check_call, CalledProcessError
from sys import path

path.append('/opt/mvp/config')
from config import image_directory, camera_controller_program

def is_picture_minute(this_instance):

   if camera_controller_program[0] == 'hourly':
      if this_instance.time().minute == camera_controller_program[1]:
         return True
     
   return False


def start_camera_controller(mqtt_client):

   this_hour = datetime.now().time().hour
   if  this_hour == 0:
      initial_hour = 23
   else:
      initial_hour = this_hour - 1

   state = {'hour_of_last_picture':initial_hour}

   while True:
      print('@@@@@@ camera controller {:%Y-%m-%d %H:%M:%S} Camera Controller Awakened'.format(datetime.utcnow()))
      current_state = state

      this_instance = datetime.now() 

      if is_picture_minute(this_instance):

         if state['hour_of_last_picture'] != this_instance.time().hour:

            camera_shell_command = 'fswebcam -r 1280x720 --no-banner {}'.format(image_directory)\
                                 + '{:%Y%m%d_%H_%M_%S}.jpg'.format(datetime.utcnow())

            try:
               #TBD - At some point upgrade to the new Python (3.5 or newer) and use the .run commmand.
               picture_results = check_call(camera_shell_command, shell=True)
               state['hour_of_last_picture'] = this_instance.time().hour
            except CalledProcessError as e:
               print('ERROR. fswebcam call failed with the following results:')
               print(picture_results)

      print('{:%Y-%m-%d %H:%M:%S} Current State {}, New State {}'.format(datetime.utcnow(), current_state['hour_of_last_picture'], state['hour_of_last_picture']))

      sleep(5)  
