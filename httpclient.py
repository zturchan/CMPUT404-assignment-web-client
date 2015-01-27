#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error, msg:
		print('Failed to create socket.  Error code: ' + str(msg[0]) + ' Message: ' + msg[1])
		sys.exit()
	try:
		s.connect((host,port))	
	except socket.error, msg:
		print('Socket connect failed! Error code: ' + str(msg[0]) + ' Message: ' + msg[1])
		sys.exit()
        return s

    def get_code(self, data):
	response = data.split("\r\n\r\n", 1)	
	line1 = response[0].split("\r\n", 1)[0]
        return line1.split(" ")[1]

    def get_headers(self,data):
        return None

    def get_body(self, data):
	response = data.split("\r\n\r\n", 1)	
	return response[1]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):	
	print url
	#host = socket.gethostbyname(url)
	try:
		host = url.split("/", 1)[0]
		path = url.split("/", 1)[1]
	except IndexError: 
		path = ""
	port = 80
	s = self.connect(host, port)

	request = "GET /" + path + " HTTP/1.1\r\n"
	request += "User-Agent: httpclient.py\r\n"
	request += "Host: " + host + ":" + str(port)
	if (args):
		request += urllib.urlencode(args)
	request += "\r\n"
	request += "Connection: close\r\n"
	request += "Accept: */*\r\n\r\n"
	#print request
	s.sendall(request)
	data = self.recvall(s)
	#response = data.split("\r\n\r\n", 1)	
	#line1 = response[0].split("\r\n", 1)[0]
        #code = line1.split(" ")[1]
        #body = response[1]
	code = self.get_code(data)
	body = self.get_body(data)
	print code, body	
	s.close()
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
	#strip the http://
	url = url.replace("http://", "")
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
