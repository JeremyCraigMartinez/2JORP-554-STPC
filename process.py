#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
import time #until implementation

def listen():
	raw_input("listenin...")
	#start listening on whatever port

	#if connection is made, read
	#after reading, call check_neighbors

	#go back to listening
	pass

def call():
	#patient side of UDP communication
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
	print("broadcasting...")
	time.sleep(2)
	pass

if __name__ == '__main__':
	if len(sys.argv) < 3:
		exit("missing arguments")

	table = readrouters(sys.argv[1])

	links = readlinks(sys.argv[1], sys.argv[2])

	if "-s" in sys.argv:
		listen()
	else:
		pass
		broadcast()