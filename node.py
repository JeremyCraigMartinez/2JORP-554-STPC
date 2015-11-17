#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
from router import *
import socket
import select

def listen(links, sockets):
	while True:
		print 'listening...'
		readable, writable, exceptional = select.select([sockets[s] for s in sockets], [], [])
		print readable, writable, exceptional

		if readable:
			updated, links = update(data, links) or links
			if updated:
				broadcast()

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

	return updates, links

def set_sockets(table, links):
	sockets = {}
	for link in links:
		sockets[links[link].locallink] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_address = ('localhost', table[link].baseport)
		sockets[links[link].locallink].bind(server_address)
		#print "socket %s: (%s %s)" % (links[link].locallink, link, server_address)
	return sockets


if __name__ == '__main__':
	table = readrouters(sys.argv[1])
	links = readlinks(sys.argv[1], sys.argv[2])
	sockets = set_sockets(table, links)

	print links
	print sockets

	listen(links, sockets)