#!/bin/bash

#Script to start up the web server
#This should be placed in a startup directory so it runs every time the Pi is booted
#There are several ways to do this, but the following is one
#https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
#Author: Howard Webb
#Date: 7/15/2017

# Start the server
/home/pi/MVP/scripts/startServer.sh

# Start CouchDB
/home/pi/MVP/scripts/startCouchDB.sh
