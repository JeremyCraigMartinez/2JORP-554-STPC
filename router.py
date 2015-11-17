#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
from node import *
import socket

def broadcast():
	#patient side of UDP communication

    if __name__ == '__main__':
        if len(sys.argv) < 3:
            exit("missing arguments")
           

    table = readrouters(sys.argv[1])
    print table

    links = readlinks(sys.argv[1], sys.argv[2])
    i = 0
    
    sock = {}
    for link in links:
        data = data + "{0} {1} {2} {3}\n".format(link, links[link].cost, links[link].locallink, links[link].remotelink)
    
    print 'Start Broadcast'
     
    for i in table:
         sock[i] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         server_address = (table[i].host, table[i].baseport)
         sock.sendto(data, server_address)


if __name__ == '__main__':
	table = readrouters(sys.argv[1])
	links = readlinks(sys.argv[1], sys.argv[2])

	if "-p" == sys.argv[1]:
		#poisen shit
		pass
	broadcast()
	listen(table[sys.argv[2]].baseport, links)