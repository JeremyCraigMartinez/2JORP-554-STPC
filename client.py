import socket
import sys
import select
import Queue

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 20030)
sock.connect(server_address)

messages = {
  "A": "A\nB 7 1 1\nE 1 2 2",
  "B": "B\nC 1 2 1\nE 8 3 3\nA 7 1 1",
  "C": "C\nB 1 1 2\nD 2 2 1",
  "D": "D\nC 2 1 2\nE 2 2 1",
  "E": "E\nB 8 3 3\nD 2 1 2\nA 1 2 2"
}


next_msg = messages[sys.argv[1]]
sock.send(next_msg)