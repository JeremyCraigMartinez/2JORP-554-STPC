#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
from node import *
import socket

this_router = sys.argv[2]

def broadcast(connected_sockets, links, table=None):
  message = this_router + '\n'
  for link in links:
    message = message + link + ' ' + str(links[link]) + '\n'
  message = message

  for conn in connected_sockets:
    sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.connect(conn)
    sockets.send(message)

if __name__ == '__main__':
  offset = 1
  if sys.argv[1] == '-p':
    offset = offset + 1
    #poison bitch
    pass
  dirname = sys.argv[offset]
  router = sys.argv[offset+1]

  table = readrouters(dirname)
  links = readlinks(dirname, router)

  connected_sockets = fill_connected_sockets(table, links)

  broadcast(connected_sockets, links)