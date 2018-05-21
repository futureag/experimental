#!/bin/bash

pushd /home/pi/openag-mvp

echo 'starting couchd'
su couchdb -c '/home/couchdb/bin/couchdb' &

echo 'waiting for couchdb to start up'
sleep 5

echo 'starting the python web server'
su pi -c 'python3 web_server.py' &

echo 'starting the mvp system'
su pi -c 'python3 mvp.py' &

popd

