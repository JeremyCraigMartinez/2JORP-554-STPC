#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
from node import *
import socket

this_router = sys.argv[2]

# broadcast sends to all connected links their own information on their connectivity and cost inside the network
# when called from __main__:
#   this only broadcasts the links found in <testdir>/*.cfg
# when called from node.py:
#   this will broadcast the current links (initial and updated) too all of its connected links
def broadcast(connected_sockets, links, table=None):
  message = this_router + '\n'
  for link in links:
    message = message + link + ' ' + str(links[link]) + '\n'
  message = message[:len(message)-1]
  # example broadcast might look like: "A\nB 7 1 1\nE 1 2 2"

  # connect and send too all connected nodes and watch the magic unfold!
  for conn in connected_sockets:
    sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.connect(conn)
    sockets.send(message)

# __main__ is invoked when we initially broadcast from a specific node starting the chain reaction of communication between all nodes
if __name__ == '__main__':
  offset = 1
  if sys.argv[1] == '-p':
    offset = offset + 1
    #poison
    pass
  dirname = sys.argv[offset]
  router = sys.argv[offset+1]

  # imported from readrouters.py
  table = readrouters(dirname)
  links = readlinks(dirname, router)

  # imported from node.py
  connected_sockets = fill_connected_sockets(table, links)

  broadcast(connected_sockets, links)