#!/usr/bin/env python3

from sys import path 
from os import chdir, getcwd
from http.server import SimpleHTTPRequestHandler
from socketserver import  TCPServer

path.append(getcwd() + '/config')
from web_server_config import local_server_port_number

# Run the web server against files in the ../web directory.
chdir(getcwd() + '/web')

Handler = SimpleHTTPRequestHandler

# Handler for SVG
Handler.extensions_map['.svg']='image/svg+xml'

httpd = TCPServer(('', local_server_port_number), Handler)

print('serving at port {}'.format(local_server_port_number))

#Start the server running
httpd.serve_forever()
