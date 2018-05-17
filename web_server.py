""" I don't know what this shebang is needed?
#- !/usr/bin/python
"""

from sys import path 
from os import chdir, getcwd
from http.server import SimpleHTTPRequestHandler
from socketserver import  TCPServer

#- import SimpleHTTPServer
#- import mimetypes
#- import sys
path.append(getcwd() + '/config')
from web_server_config import local_server_port_number

#- PORT = sys.argv[1]
#- PORT = 8080

# Run the web server against files in the ../web directory.
chdir(getcwd() + '/web')

#- Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
Handler = SimpleHTTPRequestHandler

#Handler for SVG
Handler.extensions_map['.svg']='image/svg+xml'

httpd = TCPServer(('', local_server_port_number), Handler)

print('serving at port {}'.format(local_server_port_number))

#Start the server running
httpd.serve_forever()
