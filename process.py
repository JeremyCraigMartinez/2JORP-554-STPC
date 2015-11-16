#Socket Server that listens for connections and runs the algorithm

import sys

def listen():
	#start listening on whatever port

	#if connection is made, read
	#after reading, call check_neighbors

	#go back to listening
	pass

def check_neighbors(home, current, cur_cost, *visited):
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

if __name__ == '__main__':
	router = sys.argv[1]

	#fill router information
	listen()