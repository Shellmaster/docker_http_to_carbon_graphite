#! /usr/local/bin/python

import time
import BaseHTTPServer
import datetime
import socket
import os


HOST_NAME = '0.0.0.0' # for docker it doesn't matter, bind to everything
PORT_NUMBER = 12006 # inside the container so doesn't really matter, listen on 12006

# Graphite settings -- IP and PORT to connect to graphite

# set default server if not specified
try:
	SERVER = os.environ['GRAPHITE_IP_ADDR']
except Exception:
	print "Environment Variable GRAPHITE_IP_ADDR is not set , using 127.0.0.1"
	SERVER = "127.0.0.1"

# set default port if not specified
try:
	PORT = os.environ['GRAPHITE_PORT_2003_TCP_ADDR']
except Exception:
	print "Environment Variable GRAPHITE_PORT_2003_TCP_ADDR is not set , using port 2003"
	PORT = 2003
# enable debug mode
try:
	DEBUG = os.environ['DEBUG']
except Exception:
	print "Environment Variable DEBUG is not set DEBUG mode is disabled, to enable it set DEBUG=1"
	DEBUG=0

# set the connection details for graphite
ADDR = (SERVER, PORT)


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.send_header("Wisdom", "Don't be naughty")
        s.end_headers()
    def do_GET(s):
	timestamp = str( datetime.datetime.now().strftime("%s") )
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.send_header("X-Issues-Contact", "rafal@maracje.pl")
        s.end_headers()

	URI=s.path.split("/")
	# get the value
	VALUE=URI[-1]
	# remove it from the array
	URI.pop(-1)
	# join an array with a spacebar then replace spacebar with a dot and remove first character
	PARAMS=' '.join(URI).replace(" " ,".")[1:]
        s.wfile.write("Sending as: ")
	TO_SEND = PARAMS + " " + VALUE + " " + timestamp + "\n"
        s.wfile.write(TO_SEND)
	try:
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ss.connect(ADDR)
		ss.send(TO_SEND)
	except Exception:
		pass
	ss.close()
    def log_message(self, format, *args):
	if DEBUG:
		print "Access log:", format % args
	else:
		return

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    print "Connecting to Graphite: %s:%s" % (SERVER, PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
