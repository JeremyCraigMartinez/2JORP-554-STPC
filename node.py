#!/usr/bin/python

import sys
from readrouters import *
from router import *
import socket
import select
import Queue

connected_sockets = []

def listen(table, links, server):
	inputs = [server]
	outputs = []
	queue = []
	while True:
		readable, writable, exceptional = select.select(inputs, outputs, [])

		for s in readable:
			if s is server:
				connection, client_address = s.accept()
				connection.setblocking(0)
				inputs.append(connection)

			else:
				data = s.recv(1024)
				print data
				if data == 'P':
					printTable(links)
				else:
					updated, links = update(data, links)
					if updated:
						broadcast(connected_sockets, links)
				inputs.remove(s)
				s.close()

def printTable(links):
	print_links(links, status="current links")

def update(data, links):
	updates = False

	rows = data.split('\n')
	from_node = rows[0]

	hop_off_node = links[from_node]

	rows = rows[1:]
	rows = filter(None, rows)

	old = links.copy()

	for row in rows:
		tmp = row.split(' ')
		if this_router == tmp[0]:
			pass
		elif tmp[0] in links:
			if int(tmp[1])+hop_off_node.cost < links[tmp[0]].cost:
				links[tmp[0]].cost = int(tmp[1])+hop_off_node.cost
				links[tmp[0]].locallink = hop_off_node.locallink
				links[tmp[0]].remotelink = int(tmp[2]) #next hop locallink
				updates = True
		else:
			links[tmp[0]] = LinkInfo(int(tmp[1])+hop_off_node.cost, hop_off_node.locallink, tmp[2])
			updates = True

	if updates:
		status = "old links: %s" % this_router
		print_links(links, from_node, status=status, rows=rows)
		print_links(links, status="new links: ")

	return updates, links

def print_links(links, from_node=None, rows=None, status=""):
	print status
	if rows:
		for link in links:
			print "{0} {1}".format(link, links[link])
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		print 'imported links: '+from_node
		for row in rows:
			print row
	else:
		for link in links:
			print "{0} {1}".format(link, links[link])
		print '---------------------------'
	print '---------------------------'

def set_sockets(table, links):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.setblocking(0)

	# Bind the socket to the port
	server_address = ('localhost', table[sys.argv[2]].baseport)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	server.bind(server_address)

	# Listen for incoming connections
	server.listen(5)

	return server

def fill_connected_sockets(table, links):
	connected = []
	for t in table:
		if t in links:
			connected.append((table[t].host, table[t].baseport))
	return connected

this_router = sys.argv[2]

if __name__ == '__main__':
	table = readrouters(sys.argv[1])
	links = readlinks(sys.argv[1], sys.argv[2])
	server = set_sockets(table, links)
	connected_sockets = fill_connected_sockets(table, links)

	listen(table, links, server)