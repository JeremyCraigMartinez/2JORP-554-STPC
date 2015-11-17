#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm
import socket
import sys
from readrouters import *
import zmq

def listen(port):
	print port
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://127.0.0.1:"+str(port))

	while True:
		msg = socket.recv()
		print "Got", msg
		socket.send(msg)	
	#start listening on whatever port

	#if connection is made, read
	#after reading, call check_neighbors

	#go back to listening
	pass

#old algorithm
'''
defsoy check_neighbors(home, current, cur_cost, *visited):
	if current:
		paths = current.paths
	else:
		paths = home.paths
	DNE = False #fill this in later
	for each in current.paths:
		if each.cost+cur_cost < home[each].c or DNE:
			#update home
			pass
		elif each in visited or each is home:
			pass
		else:
			call(home, each, cur_cost+each.cost, visited+each)
	return
'''

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
         
     

    if "-s" in sys.argv:
        listen(table[sys.argv[2]].baseport)
    else:
        pass
        broadcast()
     
     
  
  
  
  