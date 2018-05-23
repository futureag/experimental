from shutil import copyfile
from os import path, getcwd
from logging import getLogger
from sys import exc_info

logger = getLogger('mvp.' + __name__)

def verify_config_file():

   try:

      config_defaultfile_path = getcwd() + '/python/config_default.py'
      config_livefile_path = getcwd() + '/config/config.py'

      if not path.isfile(config_livefile_path):
         logger.warning('No configuration file was found. Reverting to the default configuration file.')
         copyfile(config_defaultfile_path, config_livefile_path)

   except:
       logger.error('Could not verify configuration file: {}, {}'.format(exc_info()[0], exc_info()[1]))
       exit(2)

def verify_web_config_file():

      try:

         web_server_config_default_file_path = getcwd() + '/python/web_server_config_default.py'
         web_server_config_livefile_path = getcwd() + '/config/web_server_config.py'

         if not path.isfile(web_server_config_livefile_path):
            logger.warning('No web configuration file was found. Reverting to the default configuration file.')
            copyfile(web_server_config_default_file_path,web_server_config_livefile_path)

      except:
         logger.error('Could not verify web configuration file: {}, {}'.format(exc_info()[0], exc_info()[1]))
         exit(3)
