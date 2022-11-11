# Jacob Coomer
# This is a server application to simulate reliable data transfer over UDP.
# Python3.10.1 Dependencies: socket, argparse, servPacket.py
# To run, use 'python3 server.py <flags>'. Flags can be viewed by running with -h.

from socket import *
import argparse
from servPacket import *

parser = argparse.ArgumentParser("Server Program", description="This program runs the server portion of the application.")
parser.add_argument('-p', dest='port', help='Sets the connection port', type=int)
args = parser.parse_args()
print(args.port)

serverPort = args.port if args.port != None else 8000

server = servPacket(serverPort)


