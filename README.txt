The program is split into two parts:

1. node.py is the file that is run on a router acting as a server (all of them)
2. router.py contains a function (broadcast) that is used by node.py whenever a change to its links is made. Broadcast can also be called via command line to manually broadcast a routers links

How to run it:

#!/bin/bash
python node.py testdir A &
python node.py testdir B &
...
python node.py testdir Y &
python node.py testdir Z &

python router [-p] testdir {A..Z}