# Jacob Coomer
# This is a server application to simulate reliable data transfer over UDP.
# Python3.10.1 Dependencies: socket, argparse, servPacket.py
# To run, use 'python3 server.py <flags>'. Flags can be viewed by running with -h.


from socket import *
import argparse
from clientPacket import *

parser = argparse.ArgumentParser("Client Program", description="Runs the client portion of the program.")
parser.add_argument('-i', dest='ip', help='Sets the IP for the connection', type=str)
parser.add_argument('-p', dest='port', help='Sets the PORT to be sent', type=int)
parser.add_argument('-m', dest='message', help='Sets the PORT to be sent', type=str)
args = parser.parse_args()

serverIP = args.ip if args.ip != None else '127.0.0.1'
serverPort = args.port if args.port != None else 8000

packetManager = clientPacket(serverIP, serverPort, args.message)
packetManager.sendMessage()
#clientSocket.close  close udp