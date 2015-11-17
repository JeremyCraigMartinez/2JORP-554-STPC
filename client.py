import socket
import sys

# Create a UDP socket
print socket.AF_INET
print socket.SOCK_DGRAM

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 20040)

messages = ["B 7 1 1\nE 1 2 2",
						"C 1 2 1\nE 8 3 3\nA 7 1 1",
						"B 1 1 2\nD 2 2 1",
						"C 2 1 2\nE 2 2 1",
						"B 8 3 3\nD 2 1 2\nA 1 2 2"]

message = messages[int(sys.argv[1])]

try:

    # Send data
    print >>sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message, server_address)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()