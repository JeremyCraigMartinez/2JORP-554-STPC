#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
from node import *
import socket

this_router = ""

# broadcast sends to all connected links their own information on their connectivity and cost inside the network
# when called from __main__:
#   this only broadcasts the links found in <testdir>/*.cfg
# when called from node.py:
#   this will broadcast the current links (initial and updated) too all of its connected links
def broadcast(connected_sockets, links, poison, table, original_links, myself=None):
  if myself:
    this_router = myself

  if poison:
    matches = match_ports_to_nodes(table, connected_sockets)
    # connect and send too all connected nodes and watch the magic unfold!
    for conn in matches:
      tmplink = deepcopy(links) # need to deep copy inorder to get a fresh list of linked each iteration
      sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sockets.connect(matches[conn])
      m = set_to_infinity(tmplink, conn, original_links, this_router)
      sockets.send(m)
  else:
    message = create_message(links, this_router)

    # connect and send too all connected nodes and watch the magic unfold!
    for conn in connected_sockets:
      sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sockets.connect(conn)
      sockets.send(message)

# sets reverse links (poison reverse) to 64
def set_to_infinity(links, conn, original_links, this_router):
  dest_nodes_original_locallink = original_links[conn].locallink
  for link in links:
    if conn == link:
      pass
    elif links[link].locallink == dest_nodes_original_locallink:
      links[link].cost = 64
  return create_message(links, this_router)

def create_message(links, this_router):
  message = this_router + '\n'
  for link in links:
    message = message + link + ' ' + str(links[link]) + '\n'
  message = message[:len(message)-1]
  # example broadcast might look like: "A\nB 7 1 1\nE 1 2 2"
  return message

# too easier relate the ports to nodes that we are connected to
def match_ports_to_nodes(table, connected_sockets):
  matches = {}
  for t in table:
    for conn in connected_sockets:
      if table[t].host == conn[0] and table[t].baseport == conn[1]:
        matches[t] = conn
  return matches

this_router = ""

# __main__ is invoked when we initially broadcast from a specific node starting the chain reaction of communication between all nodes
if __name__ == '__main__':
  offset = 1
  poison = False
  if sys.argv[1] == '-p':
    offset = offset + 1
    poison = True
    pass

  dirname = sys.argv[offset]
  this_router = sys.argv[offset+1]
  this_router
  router = sys.argv[offset+1]

  # imported from readrouters.py
  table = readrouters(dirname)
  links = readlinks(dirname, router)

  # imported from node.py
  connected_sockets = fill_connected_sockets(table, links)

  broadcast(connected_sockets, links, poison, table, links, this_router)