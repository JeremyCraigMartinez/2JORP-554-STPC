#!/usr/bin/python

#Socket Server that listens for connections and runs the algorithm

import sys
from readrouters import *
from node import *
import socket

this_router = sys.argv[2]

def broadcast(connected_sockets, links):
  message = this_router + '\n'
  for link in links:
    message = message + link + ' ' + str(links[link]) + '\n'
  message = message

  sockets = []

  for conn in connected_sockets:
    sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    sockets[len(sockets)-1].connect(conn)
    sockets[len(sockets)-1].send(message)