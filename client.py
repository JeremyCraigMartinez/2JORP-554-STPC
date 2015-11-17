import socket
import sys
import select
import Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 20020)
print >>sys.stderr, 'starting up on %s port %s' % server_address
server.bind(server_address)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 20040)
sock.connect(server_address)

# Listen for incoming connections
server.listen(5)

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('localhost', 20040)
#sock.connect(server_address)

messages = {
  "A": "A\nB 7 1 1\nE 1 2 2",
  "B": "B\nC 1 2 1\nE 8 3 3\nA 7 1 1",
  "C": "C\nB 1 1 2\nD 2 2 1",
  "D": "D\nC 2 1 2\nE 2 2 1",
  "E": "E\nB 8 3 3\nD 2 1 2\nA 1 2 2"
}

inputs = [server]
outputs = [sock]
mqs = {}
while True:
  readable, writable, exceptional = select.select(inputs, outputs, [])

  for s in readable:
    if s is server:
      connection, client_address = s.accept()
      connection.setblocking(0)
      inputs.append(connection)

      mqs[connection] = Queue.Queue()
    else:
      data = s.recv(1024)
      print data
      if data:
        if s not in outputs:
          outputs = outputs + [s]
      else:
        if s in outputs:
          outputs.remove(s)
        inputs.remove(s)
        s.close()

        del mqs[s]

  for w in writable:
    try: 
      next_msg = messages[sys.argv[1]]
    except Queue.Empty:
      outputs.remove(w)
    else:
      w.send(next_msg)
    outputs.remove(w)
    exit()

  for e in exceptional:
    inputs.remove(e)
    if e in outputs:
      outputs.remove(e)
    e.close()

    del mqs[e]



'''
# Connect the socket to the port where the server is listening
print >>sys.stderr, 'connecting to %s port %s' % server_address
for s in socks:
    s.connect(server_address)

for message in messages:

    # Send messages on both sockets
    for s in socks:
        print >>sys.stderr, '%s: sending "%s"' % (s.getsockname(), message)
        s.send(message)

    # Read responses on both sockets
    for s in socks:
        data = s.recv(1024)
        print >>sys.stderr, '%s: received "%s"' % (s.getsockname(), data)
        if not data:
            print >>sys.stderr, 'closing socket', s.getsockname()
            s.close()    '''