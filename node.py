#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

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
				updated, links = update(data, links)
				if updated:
					broadcast(connected_sockets)
					#outputs = outputs + connected_sockets
					#queue.append(str(links))
					pass
				else:
					if s in outputs:
						outputs.remove(s)
				inputs.remove(s)
				s.close()

		'''was_writable = False					
		for w in writable:
			was_writable = True
			try: 
				next_msg = queue[0]
			except Queue.Empty:
				outputs.remove(w)
			else:
				w.send(next_msg)
		if was_writable:
			queue.pop(0)

		for e in exceptional:
			inputs.remove(e)
			if e in outputs:
				outputs.remove(e)
			e.close()'''

def is_cheaper(new, old):
	return int(new[2]) < old.cost

def update(data, links):
	updates = False

	rows = data.split('\n')
	from_node = rows[0]

	hop_off_node = links[from_node]

	rows = rows[1:]
	print_links(links, rows=rows)

	for row in rows:
		if this_router == row[0]:
			pass
		elif row[0] in links:
			if int(row[2])+hop_off_node.cost < links[row[0]].cost:
				links[row[0]].cost = int(row[2])+hop_off_node.cost
				links[row[0]].locallink = hop_off_node.locallink
				links[row[0]].cost = row[4] #next hop locallink
				updates = True
		else:
			links[row[0]] = LinkInfo(int(row[2])+hop_off_node.cost, hop_off_node.locallink, row[4])
			updates = True

	print_links(links, status="new links: ")

	return updates, links

def print_links(links, rows=None, status="old links: "):
	print status
	if rows:
		for link in links:
			print "{0} {1}".format(link, links[link])
		print '~~~~~~~~~~~~~~~~~~~~~~~~~~~'
		for row in rows:
			print row
	else:
		for link in links:
			print "{0} {1}".format(link, links[link])
	print '---------------------------'

def set_sockets(table, links):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0)

	# Bind the socket to the port
	server_address = ('localhost', table[sys.argv[2]].baseport)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	server.bind(server_address)

	# Listen for incoming connections
	server.listen(5)

	return server

def fill_connected_sockets(table):
	for t in table:
		connected_sockets.append((table[t].host, table[t].baseport))

this_router = sys.argv[2]

if __name__ == '__main__':
	table = readrouters(sys.argv[1])
	links = readlinks(sys.argv[1], sys.argv[2])
	server = set_sockets(table, links)

	listen(table, links, server)