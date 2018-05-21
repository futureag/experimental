from sys import path 
from os import chdir, getcwd
from http.server import SimpleHTTPRequestHandler
from socketserver import  TCPServer

# Run from the command line as per:
# cd /home/pi/openag-mvp
# python3 web_server.py
#
# or run as a systemd service using the following service file content:
#
#   [Unit]
#   Description=mvp web server
#   Wants=network-online.target
#   After=network-online.target
#   
#   [Service]
#   RuntimeDirectory=/home/pi/openag-mvp
#   WorkingDirectory=/home/pi/openag-mvp
#   User=pi
#   ExecStart=/usr/bin/python3 /home/pi/openag-mvp/web_server.py
#   Restart=on-failure
#   
#   [Install]
#   WantedBy=multi-user.target
#
# path.append(getcwd() + '/config')
from config.web_server_config import local_server_port_number

# Run the web server against files in the ../web directory.
chdir(getcwd() + '/web')

Handler = SimpleHTTPRequestHandler

# Handler for SVG
Handler.extensions_map['.svg']='image/svg+xml'

httpd = TCPServer(('', local_server_port_number), Handler)

print('serving at port {}'.format(local_server_port_number))

#Start the server running
httpd.serve_forever()
