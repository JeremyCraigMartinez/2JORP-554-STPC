#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
from router import *
import socket

def listen(port, links):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Bind the socket to the port
	server_address = ('localhost', port)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	sock.bind(server_address)

	while True:
		print >>sys.stderr, '\nwaiting to receive message'
		data, address = sock.recvfrom(4096)
		
		print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
		
		updated, links = update(data, links) or links
		if updated:
			for link in links:
				print links[link]
			#broadcast()

def is_cheaper(new, old):
	return int(new[2]) < old.cost

def update(data, links):
	updates = False
	rows = data.split('\n')
	for row in rows:
		try:
			if is_cheaper(row, links[row[0]]):
				links[row[0]].cost = int(row[2])
				updates = True
		except:
			links[row[0]] = LinkInfo(int(row[2]), int(row[4]), int(row[6]))
			updates = True

	#logic
	return updates, links

if __name__ == '__main__':
	table = readrouters(sys.argv[1])
	links = readlinks(sys.argv[1], sys.argv[2])
	listen(table[sys.argv[2]].baseport, links)