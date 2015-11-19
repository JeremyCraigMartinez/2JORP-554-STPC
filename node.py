#!/usr/bin/python

import sys
from readrouters import *
from router import *
import socket
import select
import Queue

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
				# recv data up to 1024 bytes
				data = s.recv(1024)
				if data == 'P':
					printTable(links)
				elif data[0] == 'L':
					# update links locally and then broadcast that to all other nodes it is linked to
					links = changeLink(links, data)
					broadcast(connected_sockets, links) # imported from router.py
				else:
					# call update; if links WAS updated, broadcast new changes to linked nodes
					updated, links = update(data, links)
					if updated:
						broadcast(connected_sockets, links) # imported from router.py
				# remove inputs so next select call does not read it again
				inputs.remove(s)
				# close socket that select intercepted and that we were reading from
				s.close()

def printTable(links):
	print_links(links, status="current links")

def changeLink(links, data):
	data = data.split(' ')
	# only update cost of link to what changelink sent us
	links[data[1]].cost = data[2]
	return links

# update returns a tuple (boolean, class<LinkInfo>)
# boolean says whether <links> was changed at all in this function
# <links> is updated and returned so that it can be updated in the calling function (listen())
def update(data, links):
	updates = False

	rows = data.split('\n')
	# read first character in packet to see who sent the packet
	from_node = rows[0]

	# set the node the packet came from to the node in the links class
	hop_off_node = links[from_node]

	# remove leading character so that we can loop through <hop_off_node>'s links for comparison
	rows = rows[1:]

	old = links.copy() # deep copy for comparison later between old links and new links

	# loop links
	for row in rows:
		# split string by spaces in order to pick up multi-digit cost's
		tmp = row.split(' ')
		# if we're looking at ourselves, pass
		if this_router == tmp[0]:
			pass
		# if we already have a cost for reaching this node
		elif tmp[0] in links:
			# if the combined cost of the connecting link and the <hop_off_node>'s link is less then our current cost, update our link
			if int(tmp[1])+int(hop_off_node.cost) < links[tmp[0]].cost:
				links[tmp[0]].cost = int(tmp[1])+int(hop_off_node.cost)
				links[tmp[0]].locallink = int(hop_off_node.locallink)
				links[tmp[0]].remotelink = int(tmp[2]) #next hop locallink
				updates = True
		# if we currently cannot reach this node, create a link for it
		else:
			links[tmp[0]] = LinkInfo(int(tmp[1])+int(hop_off_node.cost), int(hop_off_node.locallink), int(tmp[2]))
			updates = True

	# compare deep copy from before to <links> here. If they're different, print the old, imported, and new <links>
	if updates:
		status = "old links: %s" % this_router
		print_links(links, from_node, status=status, rows=rows)
		print_links(links, status="new links: ")

	return updates, links

# print old links, the links being sent to us, and the new links as a result of analyzing those
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

# set socket for the server to listen on
def set_sockets(table, links):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.setblocking(0)

	server_address = ('localhost', table[sys.argv[2]].baseport)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	server.bind(server_address)

	server.listen(5)

	return server

#find all nodes we are connected to initially
def fill_connected_sockets(table, links):
	connected = []
	for t in table:
		if t in links:
			connected.append((table[t].host, table[t].baseport))
	return connected

this_router = sys.argv[2]
connected_sockets = []

if __name__ == '__main__':
	table = readrouters(sys.argv[1])
	links = readlinks(sys.argv[1], sys.argv[2])
	server = set_sockets(table, links)
	connected_sockets = fill_connected_sockets(table, links)

	listen(table, links, server)