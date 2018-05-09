# mvp blossum

This is a fork of the [MVP II](https://github.com/webbhm/OpenAg-MVP-II).

Many thanks to the folks who created the MVP II project.  On the shoulders of giants!

## Background 

Code and instructions for building a 'brain' for a controlled environment hydroponics unit.
It is mostly a collection of python code that runs on a Raspberry Pi (or similar device).  See the OpenAg [forums](http://forum.openag.media.mit.edu/) for discussion and issues:

## Changes made to this fork: 

  - Persistent variables are now in a configuration file named config.py.
  - Cron is not needed to operate the system.
  - MQTT has been added.  This allows sensor readings to be sent to a cloud MQTT broker.
  - Data logging has been changed to use the Python logging facility

## Architecture:

The main program (mvp.py) starts threads that handle the following tasks:
  - MQTT client
  - Image capture
  - Log Sensors
  - Light Controller
  - Fan Controller
  - Refresh charts and picture for the UI (render.sh)

Local data storage is in a csv formatted (without header) flat file (/home/pi/MVP/data/data.txt) - this will likely be deprected in the future.
CouchDB is the main data storage system, and will provide easy replication to the cloud in the future.

## Hardware Build:

Refer to [MVP II](https://github.com/webbhm/OpenAg-MVP-II) for the details on the hardware build of an MVP. The goal of this project is break 
dependencies between the brain code and the hardware that it will be used on.  Of course at the end of the day everything needs to be compatible bbut we hope to provide configuration flexiblity so that this code can be used with any grow environment that contains compatible sensors and
actuators.

## Build Activities
### Assumptions:
1. NOOB install of Raspbian on Raspberry Pi
2. The Raspbian system has been configured 
    - for localization (time, timezone)
    - wifi is established and connected
    - I2C has been enabled
2. 32G SD card to hold data

### Software Build
TBD

## Future Development (in no priority):
- GUI interface for setting persistent variables (could be local)
- Receive commands via MQTT
- Send pictures to cloud (such as an Amazon S3 bucket)
- Allow headless configuration of new mvp installations
