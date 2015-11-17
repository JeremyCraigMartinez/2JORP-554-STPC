#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
import socket

def broadcast():
	#patient side of UDP communication
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://127.0.0.1:50001")

	for i in range(100):
		msg = "msg %s" % i
		socket.send(msg)
		print "Sending", msg
		msg_in = socket.recv()	
	pass

if __name__ == '__main__':
	table = readrouters(sys.argv[1])
	links = readlinks(sys.argv[1], sys.argv[2])

	if "-p" == sys.argv[1]:
		#poisen shit
		pass
	broadcast()
	listen(table[sys.argv[2]].baseport, links)